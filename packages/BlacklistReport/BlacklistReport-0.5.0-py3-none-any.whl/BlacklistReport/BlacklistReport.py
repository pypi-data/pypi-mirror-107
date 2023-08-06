import csv
import logging
from datetime import timedelta
from typing import TypeVar, List, Dict, Optional

import inflect
from GuardiPy import Centra, CentraEntity, CentraApiPayload
from GuardiPy.CentraObject import Incident, LabelMinimal

from BlacklistReport.BlacklistEntry import BlacklistEntry
from BlacklistReport.__threat_data import ThreatData
from BlacklistReport.schema import GC_CSV_SCHEMA, CENTRA_SCHEMA, is_valid_format

AnyCentraEntity = TypeVar("AnyCentraEntity", bound=CentraEntity)


def deduplicate_incidents(incidents: list) -> list:
    unique_incidents = dict()
    for i in incidents:
        if f"{i['source']['ip']}-{i['destination']['ip']}" not in unique_incidents:
            unique_incidents[f"{i['source']['ip']}-{i['destination']['ip']}"] = i
    return list(unique_incidents.values())


def generate_blacklist_report(gc_host: Dict, hours: int, opswat_key: str, greynoise_key: str,
                              gc_customer_name: str, severity: List[str] = None, incidents: List[Dict] = None):
    if is_valid_format(gc_host, CENTRA_SCHEMA):

        gc = Centra(username=gc_host['username'],
                    hostname=gc_host['dev_host'],
                    password=gc_host['password'])

        converter = inflect.engine()

        ThreatData.set_opswat_key(opswat_key=opswat_key)
        ThreatData.set_greynoise_key(greynoise_key=greynoise_key)

        blr = BlacklistReport(gc=gc, gc_customer_name=gc_customer_name, incidents=incidents)
        incident_count = blr.fetch_incidents(hours, severity=severity)
        incident_count_str = converter.number_to_words(incident_count)
        blr.build_report()

        source_ip_count = len(blr.report.keys())
        source_ip_count_str = converter.number_to_words(source_ip_count)

        return dict(
            hours=hours,
            incident_count=incident_count,
            incident_count_str=incident_count_str,
            report=blr.build_report_str(incident_count_str, incident_count, source_ip_count_str, source_ip_count)
        )

    else:
        logging.error("Failed to instantiate Centra instance.", exc_info=True)


class BlacklistReport:
    def __init__(self, gc: Centra, gc_customer_name: str, incidents: List[Dict] = None):
        self.gc: Centra = gc
        self.incidents: List[Dict] = deduplicate_incidents(incidents) if incidents else list()
        self.report: Dict = dict()
        self.hours: int = -1
        self.shared_instance, self.customer_label = self.fetch_customer_label(gc_customer_name)

    def fetch_customer_label(self, gc_customer_name: str) -> (bool, Optional[str]):
        shared_instance = False
        customer_label = None
        query: CentraApiPayload = LabelMinimal.list(
            assets='on,off',
            find_matches=True,
            dynamic_criteria_limit=500,
            key='Customers'
        )
        res = self.gc.execute(query)
        if res:
            shared_instance = True
            for i in res:
                if i.value == gc_customer_name:
                    customer_label = i.id
        return shared_instance, customer_label

    def fetch_incidents(self, hours: int = 24, severity: List[str] = None) -> int:
        self.hours = abs(hours)
        if not self.incidents and (not self.shared_instance or self.customer_label):
            query = Incident.list(
                from_time=timedelta(hours=-self.hours),
                incident_type='Reveal',
                tags_include='Reputation',
                severity=severity or ["Medium", "High"],
                prefixed_filter='bad_reputation'
            )
            if self.customer_label:
                query.params['any_side'] = self.customer_label
            result = self.gc.export_to_csv(query).splitlines()
            csv_reader = csv.DictReader(result, delimiter=',')
            self.incidents = [_parse_reported_fields(row) for row in csv_reader]
        for incident in self.incidents:
            self._enrich_incident_data(incident)
        logging.debug("Number of blacklisted IP incidents: %d", len(self.incidents))
        return len(self.incidents)

    def build_report(self):
        for incident in self.incidents:
            source = incident['source']
            destination = incident['destination']
            if source['ip'] in self.report:
                self.report[source['ip']].add_destination(destination=destination)
            else:
                self.report[source['ip']] = BlacklistEntry(source=source, destination=destination)
        return self.report.copy()

    def _enrich_incident_data(self, incident: dict) -> None:
        if not (all([k in incident['source'] for k in ['ip']])
                and all([k in incident['destination'] for k in ['ip', 'ports']])):
            info: Incident = self.gc.execute(Incident.get_all_info(id=incident['id']))
            if info:
                source = incident['source']
                destination = incident['destination']
                if not source.get('ip'):
                    source['ip'] = info.source_asset.ip
                if not source.get('domain'):
                    source['domain'] = info.source_asset.vm.name if info.source_asset.vm else None
                if not source.get('country'):
                    source['country'] = info.source_asset.country
                if not destination.get('ip'):
                    destination['ip'] = info.destination_asset.ip
                if not destination.get('domain'):
                    destination['domain'] = info.destination_asset.vm.name \
                        if info.destination_asset.vm else None
                if not destination.get('ports'):
                    destination['ports'] = list(set([e.destination_port for e in info.events
                                                     if e.destination_port is not None and e.destination_port >= 0]))

    def build_report_str(self, incident_count_str: str, incident_count: int, source_ip_count_str: str,
                         source_ip_count: int):
        report_summary = self._plaintext_header(incident_count_str, incident_count, source_ip_count_str,
                                                source_ip_count)
        report_summary += ''.join([_plaintext_entry(entry) for ip, entry in self.report.items()])
        return report_summary

    def _plaintext_header(self, incident_count_str, incident_count, source_ip_count_str, source_ip_count) -> str:
        return f"In the past {self.hours} hours, we have seen {incident_count_str} ({incident_count}) " \
               f"reputation incidents from {source_ip_count_str} ({source_ip_count}) sources.\n\n"


def _parse_reported_fields(entity: Dict) -> Dict:
    parsed_entity = dict()
    if is_valid_format(entity, GC_CSV_SCHEMA):
        affected_assets = [asset.strip() for asset in entity.get('affected_assets', '').split('),')]
        source_ip = affected_assets[0].split(' ')[0]
        destination_ip = affected_assets[1].split(' ')[0]
        if "\\" in destination_ip:
            destination_ip = destination_ip.split("\\")[1]
        parsed_entity = dict(id=entity['id'], source=dict(ip=source_ip), destination=dict(ip=destination_ip))
    return parsed_entity


def _plaintext_entry(ip_entry: BlacklistEntry) -> str:
    text = ""
    src_location = f"{ip_entry.source.ip} "
    if ip_entry.source.domain and ip_entry.source.domain != ip_entry.source.domain:
        src_location += f"- {ip_entry.source.domain} "
    text += f"Source: {src_location}({ip_entry.source.country})\n"
    if ip_entry.source.country != 'Internal':
        text += f"\tOPSWAT: {ip_entry.source.opswat}\n"
        text += f"\tGreyNoise: {ip_entry.source.greynoise}\n"
    text += f"Destination(s):\n"
    for destination in ip_entry.destinations:
        dst_location = f"{destination.ip} "
        if destination.domain and destination.domain != destination.ip:
            dst_location += f"- {destination.domain} "
        text += f"\tDestination: {dst_location}({destination.country})\n"
        text += f"\tDestination Port(s): {destination.ports}"
        if destination.country != 'Internal':
            text += f"\n\tOPSWAT: {destination.opswat}"
            text += f"\n\tGreyNoise: {ip_entry.source.greynoise}\n"
        else:
            text += "\n"
        text += "\n"
    text += "\n"
    return text

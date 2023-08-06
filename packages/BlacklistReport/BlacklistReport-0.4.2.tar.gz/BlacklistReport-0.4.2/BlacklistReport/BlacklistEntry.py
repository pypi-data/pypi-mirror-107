from typing import List, Union
from ipaddress import ip_address, IPv4Address, IPv6Address

from BlacklistReport.__threat_data import ThreatData


class BlacklistEntry:
    def __init__(self, source: dict, destination: dict):
        self.source = self.IpEntry(**source)
        self.__destinations: List = [self.IpEntry(**destination)]

    def add_destination(self, destination: dict):
        for entry in self.__destinations:
            if entry.ip == destination['ip']:
                return
        self.__destinations.append(self.IpEntry(**destination))

    def to_dict(self):
        return dict(source=self.source.to_dict(), destinations=[d.to_dict() for d in self.destinations])

    @property
    def destinations(self):
        return self.__destinations.copy()

    class IpEntry:

        def __init__(
                self,
                ip: str,
                ports: List[int] = None,
                domain: str = None,
                country: str = None,
                opswat_scans: List[str] = None,
                opswat_tags: List[str] = None,
                gn_classification: str = None,
                gn_organization: str = None,
                gn_tags: List[str] = None
        ):
            try:
                self.__ip: Union[IPv4Address, IPv6Address] = ip_address(address=ip)
            except ValueError:
                self.__ip = ip
            finally:
                self.__ports = ports or list()
                self.domain = domain
                self.__country = country
                self.opswat_scans = opswat_scans
                self.opswat_tags = opswat_tags
                self.gn_classification = gn_classification
                self.gn_organization = gn_organization
                self.gn_tags = gn_tags
                if type(self.__ip) in [IPv4Address, IPv6Address] and self.__ip.is_global:
                    if not self.__country:
                        self.__country = ThreatData.fetch_country(ip)
                    if not any([self.opswat_tags, self.opswat_scans]):
                        self.opswat_tags, self.opswat_scans = ThreatData.fetch_OPSWAT_summary(ip)
                    if not any([self.gn_classification, self.gn_organization, self.gn_tags]):
                        self.gn_classification, self.gn_organization, self.gn_tags = ThreatData.fetch_GREYNOISE_summary(ip)
                else:
                    self.__country = 'Internal'

        def to_dict(self) -> dict:
            return dict(
                ip=self.ip,
                domain=self.domain,
                ports=self.ports,
                origin_country=self.country,
                opswat=self.opswat,
                greynoise=self.greynoise
            )

        @property
        def ip(self) -> str:
            return str(self.__ip)

        @property
        def ports(self) -> str:
            return ', '.join(list(set([str(port) for port in self.__ports])))

        @property
        def country(self):
            return self.__country or 'Unavailable'

        @property
        def opswat(self):
            summary = None
            detected = [scan for scan in self.opswat_scans if str(scan) not in ("0", "5")]
            if any([self.opswat_scans, self.opswat_tags]):
                summary = f"{len(detected)}/{len(self.opswat_scans)} Score"
                if len(self.opswat_tags) > 0:
                    summary += " - " + (', '.join(self.opswat_tags)).title()
            return summary or 'Unavailable'

        @property
        def greynoise(self):
            summary_data = list()
            if self.gn_organization:
                summary_data.append(f"Organization - {self.gn_organization}")
            if self.gn_classification:
                summary_data.append(f"Classification - {self.gn_classification.upper()}")
            if self.gn_tags:
                summary_data.append(f"Tags - {self.gn_tags}")
            return ', '.join(summary_data) or 'Unavailable'

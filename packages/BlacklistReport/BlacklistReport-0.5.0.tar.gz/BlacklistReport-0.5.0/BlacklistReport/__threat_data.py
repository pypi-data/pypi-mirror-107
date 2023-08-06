import logging
from typing import Optional

import requests
from greynoise import GreyNoise


class ThreatData:
    __OPSWAT_KEY = None
    __OPSWAT_URL = "https://api.metadefender.com/v4/ip/"
    __GREYNOISE_KEY = None

    @staticmethod
    def set_opswat_key(opswat_key: str):
        ThreatData.__OPSWAT_KEY = opswat_key

    @staticmethod
    def set_greynoise_key(greynoise_key: str):
        ThreatData.__GREYNOISE_KEY = greynoise_key

    @staticmethod
    def fetch_country(ip: str):
        url = ThreatData.__OPSWAT_URL + ip
        headers = dict(apikey=ThreatData.__OPSWAT_KEY)
        res = requests.get(url=url, headers=headers)
        if res.status_code == 200:
            res = res.json()
            geo_info = res.get('geo_info', {})
            country = geo_info.get('country', {})
            country = country.get('name')
        else:
            country = None
        return country

    @staticmethod
    def fetch_OPSWAT_summary(ip: str) -> (list, list):
        tags, scans = list(), list()
        url = ThreatData.__OPSWAT_URL + ip
        headers = {'apikey': ThreatData.__OPSWAT_KEY}
        res = requests.get(url=url, headers=headers)
        if res.status_code == 200:
            res = res.json()
            res = res.get('lookup_results', {})
            sources = res.get('sources', [])
            for source in sources:
                scans.append(source['status'])
                if source['status'] not in [0, 5]:
                    tags.append(source['assessment'])
        else:
            logging.warning('Failed to fetch OPSWAT summary for ip {}'.format(ip))
        return tags, scans

    @staticmethod
    def fetch_TALOS_summary(ip: str) -> str:
        url = 'https://talosintelligence.com/sb_api/query_lookup'
        headers = {
            'referer': 'https://talosintelligence.com/reputation_center/lookup?search=%s' % ip,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        params = {
            'query': '/api/v2/details/ip/',
            'query_entry': ip
        }
        res = requests.get(url=url, headers=headers, params=params)
        if res.status_code == 201:
            res_json = res.json()
            email_rep: str = res_json.get('email_score_name', 'Missing')
            web_rep: str = res_json.get('web_score_name', 'Missing')
            summary = f"Email Reputation - {email_rep.upper()}, Web Reputation - {web_rep.upper()}"
        else:
            logging.warning('Failed to fetch Talos summary for ip {}'.format(ip))
            summary = None
        return summary

    @staticmethod
    def fetch_GREYNOISE_summary(ip: str) -> (Optional[str], Optional[str], Optional[list]):
        gn = GreyNoise(api_key=ThreatData.__GREYNOISE_KEY, timeout=30)
        gn_ip_data = gn.ip(ip)
        
        organization = gn_ip_data.get('metadata', {}).get('organization')
        classification = gn_ip_data['classification'].upper() if 'classification' in gn_ip_data \
                                                                 and gn_ip_data['classification'] != 'unknown' else None
        tags = gn_ip_data.get('tags')
        
        return classification, organization, tags

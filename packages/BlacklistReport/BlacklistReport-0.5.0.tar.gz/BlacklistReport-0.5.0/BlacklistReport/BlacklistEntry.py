from typing import List
from BlacklistReport.IpEntryPool import IpEntryPool


class BlacklistEntry:
    ip_pool = None

    def __init__(self, source: dict, destination: dict):
        if not BlacklistEntry.ip_pool:
            BlacklistEntry.ip_pool = IpEntryPool()
        self.source = BlacklistEntry.ip_pool.find_or_create(source)
        self.__destinations: List = [BlacklistEntry.ip_pool.find_or_create(destination)]

    def add_destination(self, destination: dict):
        for entry in self.__destinations:
            if entry.ip == destination['ip']:
                return
        self.__destinations.append(BlacklistEntry.ip_pool.find_or_create(destination))

    def to_dict(self):
        return dict(source=self.source.to_dict(), destinations=[d.to_dict() for d in self.destinations])

    @property
    def destinations(self):
        return self.__destinations.copy()

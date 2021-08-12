
class ParserClass:
    domain_resolving = {}

    @staticmethod
    def __handle_address(record, address: str) -> bool:
        if record["type"] != "link":
            return True

        if "https" in address:
            for url in record["urls"]:
                if "https" in url:
                    return True
            return False
        else:
            return address in record["urls"]

    @staticmethod
    def __handle_ip(record, address: str) -> bool:
        if record["type"] == "ip" or record["type"] == "domain":
            return True

        return record["type"] == "link" and address in record["urls"]

    def __cyclic_parser(self, domain: str):
        items = domain.split(".")
        while len(items) > 1:
            search = ".".join(items)
            record = self.domain_resolving.get(search)
            if record and (len(search) == len(domain) or record["type"] == "mask"):
                return record
            items.pop(0)
        return None

    def process_data(self, record):
        ips, domain, urls, initiator = record
        self_resolving = len(domain) == 0
        keys = ips if self_resolving else [domain]
        for key in keys:
            cleared_key = key.replace("*.", "")
            record = self.domain_resolving.get(cleared_key)
            if not record:
                url_set = set(urls)
                lock = {"initiator": initiator, "type": "link", "urls": url_set} if len(url_set) > 0 \
                    else {"initiator": initiator, "type": "mask"} if "*." in domain else \
                    {"initiator": initiator, "type": "ip" if self_resolving else "domain"}
                self.domain_resolving[cleared_key] = lock
                return

            if record["type"] != "link":
                return

            for url in urls:
                record["urls"].add(url)

    def get(self, key: str, deep=False):
        if deep:
            return self.__cyclic_parser(key)
        else:
            try:
                return self.domain_resolving[key]
            except KeyError:
                return None

    def handle(self, record, value: str, is_ip=False):
        if is_ip:
            return ParserClass.__handle_ip(record, value)
        else:
            return ParserClass.__handle_address(record, value)


import logging
import ipaddress
import tldextract

from Parser import ParserClass
from utils.files import get_sha, get_content
from CSVparser import CSVParserClass


class StorageClass:
    sha = None
    parser = ParserClass()
    is_ready = False

    def get_latest(self):
        is_first = self.sha is None
        if is_first:
            logging.info("first run")

        sha = get_sha()
        if not sha:
            logging.error("An error occurred while fetching")
            return
        if sha == self.sha:
            logging.info("Data has not been updated")
            return

        content = get_content()
        if not content:
            logging.error("An error occurred while fetching")
            return

        logging.info("updating data")
        self.sha = sha
        result = CSVParserClass.parse(content)
        for record in result:
            self.parser.process_data(record)
        if is_first:
            self.is_ready = True

    def check(self, value: str) -> bool:
        ext = tldextract.extract(value)
        host_name = f"{ext.subdomain}.{ext.domain}.{ext.suffix}" \
            if ext.subdomain else f"{ext.domain}.{ext.suffix}" if ext.suffix else ext.domain
        try:
            ipaddress.ip_address(host_name)
            is_ip = True
        except ValueError:
            is_ip = False

        if not host_name:
            logging.warning("Invalid hostname")
            return False

        record = self.parser.get(host_name, deep=not is_ip)
        if not record:
            return False
        return self.parser.handle(record, value)


storage_instance = StorageClass()


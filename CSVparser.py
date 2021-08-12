import csv
import ctypes
import logging
from typing import List

csv.field_size_limit(int(ctypes.c_ulong(-1).value // 2))
csv.field_size_limit()


class CSVParserClass:
    SOURCE_ENCODING = "cp1251"
    SOURCE_DECODING = "utf8"
    DELIMITER = ";"

    @staticmethod
    def split_str(string: str, separator="|") -> List[str]:
        items = string.split(separator)
        items = list(map(lambda s: s.strip(), items))
        items = list(filter(lambda s: len(s) > 0, items))
        return items

    @staticmethod
    def parse(data: bytes):
        logging.info('Parsing started')
        data_stack = []

        decoded_bytes = data.decode(CSVParserClass.SOURCE_ENCODING)
        decoded_list = csv.reader(decoded_bytes.splitlines(), quotechar=CSVParserClass.DELIMITER)

        for item in decoded_list:
            try:
                # обходим случай, когда список состоит из менее чем 3 значений
                ips_str, domain_str, urls_str, initiator_str = "".join(item).split(";")[0:4]

                ips = CSVParserClass.split_str(ips_str)
                domain = domain_str.strip()
                urls = CSVParserClass.split_str(urls_str)
                initiator = initiator_str.strip()
                record = ips, domain, urls, initiator

                data_stack.append(record)
            except ValueError:
                continue

        logging.info(f"Parsing finished. Parsed {len(data_stack)} records")
        return data_stack


import logging

import requests


GIT_URL = "https://api.github.com/repos/zapret-info/z-i/contents"

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
           "Referer": "https://api.github.com/repos/zapret-info/z-i/contents",
           "Accept": "application/vnd.github.v3+json"}


def get_sha():
    """
    :return: response object

    """
    logging.info('Receiving SHA')
    with requests.session() as s:
        response = s.get(GIT_URL, headers=HEADERS)
        if response.status_code == 200:
            json_rsp = response.json()
            dump = next(filter(lambda x: x["name"] == "dump.csv", json_rsp))
            sha_dump = dump.get("sha")
            logging.info('SHA received')
        else:
            logging.error('SHA has not been received')
            return None
    return sha_dump


def get_content():
    logging.info('Receiving content')
    with requests.session() as s:
        res = s.get("https://raw.githubusercontent.com/zapret-info/z-i/master/dump.csv")
        if res.status_code == 200:
            file_content = res.content
            logging.info('Content received')
        else:
            logging.error('Content has not been received')
            return None

    return file_content


# def download_file(url: str):
#     """
#     :param url: str -> https://raw.githubusercontent.com/zapret-info/z-i/master/dump.csv
#     :return: response object
#
#     """
#     with requests.Session() as s:
#         download_response = ResponseStatus()
#         res = s.get(url)
#
#         if res.status_code == 200:
#             download_response.content = res.content
#         else:
#             download_response.status = res.status_code
#
#     return download_response


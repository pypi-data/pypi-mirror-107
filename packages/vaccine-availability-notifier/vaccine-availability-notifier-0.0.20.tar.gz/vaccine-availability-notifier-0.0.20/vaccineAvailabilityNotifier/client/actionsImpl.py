import time

import requests

from vaccineAvailabilityNotifier.client.actions import Actions


def get_headers(params=None):
    # 'accept': 'application/json',
    # 'Accept-Language': 'hi_IN'
    return {
        "user-agent": "Mozilla/5.0 (Linux; Android 9; Redmi Note 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.93 Mobile Safari/537.36",
        'Accept-Language': 'hi_IN',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    }


class ActionsImpl(Actions):

    def get(self, url, params={}):
        r = None
        try:
            r = requests.get(url, {}, headers=get_headers())
        except Exception as e:
            # if there is any exception print that and wait for 100 sec
            print(e)
            time.sleep(10)
        return r

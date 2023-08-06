import json

from vaccineAvailabilityNotifier.client.actionsImpl import ActionsImpl


def get_url():
    return 'https://cdn-api.co-vin.in/api/v2/admin/location/states'


class StateIdProcessor:
    __action_processor = ActionsImpl()

    def __init__(self, state_name, all):
        self.state_name = state_name
        self.all = all

    def process(self):
        response = self.__action_processor.get(
            url=get_url()
        )
        if response is not None and response.status_code is not None and response.status_code == 200:
            states = json.loads(response.content.decode('utf-8'))
            if self.all:
                return states['states']
            else:
                states = list(filter(lambda x: x.get("state_name") == self.state_name, states['states']))
                if len(states) == 0:
                    print('unable to find state: ' + self.state_name)
                    exit()
                return states[0]

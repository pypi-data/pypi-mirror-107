import json

from vaccineAvailabilityNotifier.client.actionsImpl import ActionsImpl
from vaccineAvailabilityNotifier.processors.state_info_processor import StateIdProcessor


def get_url(state_id):
    return 'https://cdn-api.co-vin.in/api/v2/admin/location/districts/' + str(state_id)


class DistrictIdProcessor:
    __action_processor = ActionsImpl()

    def __init__(self, state_name, district_name, all):
        self.state_name = state_name
        self.district_name = district_name
        self.all = all

    def process(self):

        state_id = StateIdProcessor(state_name=self.state_name, all=False) \
            .process()["state_id"]
        print("state id: " + str(state_id))
        print("state name: " + str(self.state_name))

        response = self.__action_processor.get(
            url=get_url(state_id)
        )
        if response is not None and response.status_code is not None and response.status_code == 200:
            dists = json.loads(response.content.decode('utf-8'))

            if self.all:
                return dists
            else:
                districts = list(filter(lambda x: x.get("district_name") == self.district_name, dists['districts']))
                if len(districts) == 0:
                    print('unable to find district: ' + self.state_name)
                    exit()
                return districts[0]

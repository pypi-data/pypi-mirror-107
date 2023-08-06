from datetime import datetime

from vaccineAvailabilityNotifier.client.actionsImpl import ActionsImpl
from vaccineAvailabilityNotifier.util import response_processor_utils


def get_url(params={}):
    return 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=' + params[
        "district_id"] + '&date=' + \
           params["date"]


class ProcessByDistrictId:
    __action_processor = ActionsImpl()

    def __init__(self, state_name, district_name, sender_email_id, sender_email_password, receiver_email, include_45,
                 district_id):
        self.sender_email_id = sender_email_id
        self.sender_email_password = sender_email_password
        self.receiver_email = receiver_email
        self.include_45 = include_45
        self.state_name = state_name
        self.district_name = district_name
        self.district_id = district_id

    def process(self):
        print('sender\'s email : ' + self.sender_email_id)
        print(self.receiver_email)
        print("\n\n\n")
        response = self.__action_processor.get(
            url=get_url({
                'district_id': self.district_id,
                'date': datetime.today().strftime('%d-%m-%Y')
            })
        )

        response_processor_utils.process(response=response, include_45=self.include_45,
                                         receiver_email=self.receiver_email,
                                         sender_email_id=self.sender_email_id,
                                         sender_email_password=self.sender_email_password)

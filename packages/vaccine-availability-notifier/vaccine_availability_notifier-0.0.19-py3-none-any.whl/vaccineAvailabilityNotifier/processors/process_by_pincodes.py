from datetime import datetime

from vaccineAvailabilityNotifier.client.actionsImpl import ActionsImpl
from vaccineAvailabilityNotifier.util import response_processor_utils


def get_url(params={}):
    return 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=' + params[
        "pincode"] + '&date=' + \
           params["date"]


class ProcessByPinCodes:
    __action_processor = ActionsImpl()

    def __init__(self, sender_email_id, sender_email_password, pincodes, receiver_email, include_45):
        self.sender_email_id = sender_email_id
        self.sender_email_password = sender_email_password
        self.pincodes = pincodes
        self.receiver_email = receiver_email
        self.include_45 = include_45

    def process(self):
        print('sender\'s email : ' + self.sender_email_id)
        print(self.receiver_email)
        print(self.pincodes)
        print("\n\n\n")
        responses = []
        for pincode in self.pincodes:
            responses.append(self.__action_processor.get(
                url=get_url({
                    'pincode': pincode,
                    'date': datetime.today().strftime('%d-%m-%Y')
                })
            ))

        print(responses)

        for response in responses:
            response_processor_utils.process(response=response, include_45=self.include_45,
                                             receiver_email=self.receiver_email,
                                             sender_email_id=self.sender_email_id,
                                             sender_email_password=self.sender_email_password)

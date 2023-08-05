import time

import schedule

from vaccineAvailabilityNotifier.processors.district_info_processor import DistrictIdProcessor
from vaccineAvailabilityNotifier.processors.process_by_district_id import ProcessByDistrictId
from vaccineAvailabilityNotifier.processors.process_by_pincodes import ProcessByPinCodes


def execute_run():
    print("executing !!!")


class ScheduleJob:

    def __init__(self, sender_email_id, sender_email_password, pincodes, receiver_email, include_45, state_name,
                 district_name):
        self.sender_email_id = sender_email_id
        self.sender_email_password = sender_email_password
        self.pincodes = pincodes
        self.receiver_email = receiver_email
        self.include_45 = include_45
        self.state_name = state_name
        self.district_name = district_name
        self.district_id = None

    def schedule(self, time_in_seconds):
        schedule.every(time_in_seconds).seconds.do(execute_run)

        while True:
            try:
                if self.state_name is not None and self.district_name is not None:
                    self.district_id = str(
                        DistrictIdProcessor(state_name=self.state_name, district_name=self.district_name, all=False) \
                            .process()["district_id"])
                    ProcessByDistrictId(state_name=self.state_name, district_name=self.district_name,
                                        sender_email_id=self.sender_email_id,
                                        sender_email_password=self.sender_email_password,
                                        receiver_email=self.receiver_email,
                                        include_45=self.include_45, district_id=self.district_id) \
                        .process()
                else:
                    ProcessByPinCodes(sender_email_id=self.sender_email_id,
                                      sender_email_password=self.sender_email_password,
                                      pincodes=self.pincodes, receiver_email=self.receiver_email,
                                      include_45=self.include_45) \
                        .process()
                time.sleep(time_in_seconds)
            except Exception as e:
                print(e)

        print("running !!!")

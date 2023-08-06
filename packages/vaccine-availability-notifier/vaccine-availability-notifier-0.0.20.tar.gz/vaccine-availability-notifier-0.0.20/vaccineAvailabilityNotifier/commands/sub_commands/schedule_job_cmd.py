import click

from vaccineAvailabilityNotifier.processors.district_info_processor import DistrictIdProcessor
from vaccineAvailabilityNotifier.processors.jobs.schedule_job import ScheduleJob
from vaccineAvailabilityNotifier.processors.state_info_processor import StateIdProcessor


@click.command("schedule", help='schedule vaccine availability task')
@click.pass_context
@click.option('--include-45', '-i45', required=False, default=False, type=bool)
@click.option('--scheduler-time', '-st', required=False, default=5, type=int)
@click.option('--gmail-id', '-gid', required=True, default="bhasker.nandkishortest01@gmail.com", type=str)
@click.option('--gmail-password', '-gpass', required=False, default="System*#541", type=str)
@click.option('--receiver-email', '-re', required=False, default=["bhasker.nandkishor@gmail.com"], type=str,
              multiple=True)
@click.option('--state', '-s', required=False, default=None, type=str)
@click.option('--district', '-d', required=False, default=None, type=str)
@click.option('--pincodes', '-pcodes', nargs=0, required=False)
@click.argument('pincodes', nargs=-1)
def cmd(ctx, scheduler_time, gmail_id, gmail_password, pincodes, receiver_email, include_45, state, district):
    if state is None and district is None:
        if len(pincodes) > 0:
            print('processing by pincodes')
            ScheduleJob(sender_email_id=gmail_id, sender_email_password=gmail_password,
                        pincodes=pincodes, receiver_email=receiver_email, include_45=include_45, state_name=state,
                        district_name=district) \
                .schedule(scheduler_time)
        else:
            print("pincodes or district combination is not correct.please check and process again")
            exit()

    elif len(pincodes) == 0:
        if state is not None and district is not None:
            print('processing by districts')
            ScheduleJob(sender_email_id=gmail_id, sender_email_password=gmail_password,
                        pincodes=pincodes, receiver_email=receiver_email, include_45=include_45, state_name=state,
                        district_name=district) \
                .schedule(scheduler_time)
        else:
            print("pincodes or district combination is not correct.please check and process again")
            exit()

    else:
        print("pincodes or district combination is not correct.please check and process again")
        exit()


@click.command("get_state", help='get state id')
@click.pass_context
@click.option('--state-name', '-sn', required=False, type=str)
@click.option('--all', '-a', required=False, default=False, type=bool)
def cmd_get_state_id(ctx, state_name, all):
    print(StateIdProcessor(state_name=state_name, all=all) \
          .process())


@click.command("get_district", help='get district id')
@click.pass_context
@click.option('--state-name', '-sn', required=False, type=str)
@click.option('--district-name', '-dn', required=False, type=str)
@click.option('--all', '-a', required=False, default=False, type=bool)
def cmd_get_district_id(ctx, state_name, district_name, all):
    print(DistrictIdProcessor(state_name=state_name, district_name=district_name, all=all) \
          .process())

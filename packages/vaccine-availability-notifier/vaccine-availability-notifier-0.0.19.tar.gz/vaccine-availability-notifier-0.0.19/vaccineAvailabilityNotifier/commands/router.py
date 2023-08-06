import click

from .sub_commands import schedule_job_cmd


def safe_entry_point():
    entry_point()


# except Exception as e:
#     print(Fore.RED, '------------------------------------------')
#     print(Fore.RED, 'unable to process../ COMMAND NOT NOT FOUND',e)
#     print(Fore.RED, '------------------------------------------')
#     exit(0)

def get_cmd_help():
    return "------------------------------------------------------------------------\nnotify yourself when vaccine is " \
           "available 	" \
           "\n-------------------------------------------------------------------------- "


@click.group(help=get_cmd_help())
@click.pass_context
def entry_point(ctx):
    """notify yourself when vaccine is available"""


# info cmd
@entry_point.command("info")
@click.pass_context
def info(ctx):
    """notify yourself when vaccine is available"""


# feedback command
@entry_point.command("feedback", help='provide the feedback')
@click.pass_context
@click.option("--output-format", "-of", default='table', type=str, required=False)
def feedback(ctx, output_format):
    """provide the feedback"""


entry_point.add_command(schedule_job_cmd.cmd)
entry_point.add_command(schedule_job_cmd.cmd_get_state_id)
entry_point.add_command(schedule_job_cmd.cmd_get_district_id)

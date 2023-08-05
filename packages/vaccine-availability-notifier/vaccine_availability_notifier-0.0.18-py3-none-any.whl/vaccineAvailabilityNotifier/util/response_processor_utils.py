import json

from vaccineAvailabilityNotifier.email.email_sender import send_email, send_email_switch


def process(response, include_45, receiver_email, sender_email_id, sender_email_password):
    if response is not None and response.status_code is not None and response.status_code == 200:
        res = json.loads(response.content.decode('utf-8'))
        for center in res['centers']:

            if include_45:
                available_centers = list(
                    filter(lambda x: x.get("available_capacity") > 0, center["sessions"]))
            else:
                available_centers = list(
                    filter(lambda x: x.get("available_capacity") > 0 and x.get("min_age_limit") == 18,
                           center["sessions"]))

            print(available_centers)

            if len(available_centers) > 0:
                for r_id_individual in receiver_email:
                    send_email(json.dumps(center, indent=3), sender_email_id=sender_email_id,
                               sender_email_password=sender_email_password,
                               receiver_email_id=r_id_individual)

            else:
                print('slot is not available')

    elif response is not None and response.status_code is not None and response.status_code == 403:
        send_email_switch(sender_email_id=sender_email_id,
                          sender_email_password=sender_email_password,
                          receiver_email_id="bhasker.nandkishor@gmail.com")
        print('switch network')

    print("run completed !!")

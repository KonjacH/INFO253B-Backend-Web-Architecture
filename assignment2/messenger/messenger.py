import requests

def send_message(notify, title):
    if ( not notify):
        return
    else:
        return requests.post(
            "https://api.mailgun.net/v3/sandboxe7c138557d514740bfe3629053b22026.mailgun.org/messages",
            auth=("api", "83420333282117142014370b008b017a-38029a9d-be2efed9"),
            data={
                "from": "Excited User <Konjac@sandboxe7c138557d514740bfe3629053b22026.mailgun.org>",
                "to": [notify, "Konjac@sandboxe7c138557d514740bfe3629053b22026.mailgun.org"],
                "subject": "Hello from todoapp",
                "text": "The task %s is completed" % title
            }
        )
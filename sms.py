from twilio.rest import Client

def send_sms(to, body):
    account_sid = 'ACfba30dd9675eb5d5fe64aafb7e67e8b0'
    auth_token = 'da42c519aae1638404df25bb74fe4a02'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=body,
        from_='+18148041711',
        to=to
    )

    print(f"Sent to {to}: {message.sid}")

from twilio.rest import Client

def send_sms(to, body):
    account_sid = 'AC59a008f29fd2057524c9d2ffa49d0bc2'
    auth_token = '927f256a959560ec89a342495717786d'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=body,
        from_='+18148041711',
        to=to
    )

    print(f"Sent to {to}: {message.sid}")
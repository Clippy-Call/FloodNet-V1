from twilio.rest import Client

def send_sms(to, body):
    account_sid = 'AC59a008f29fd2057524c9d2ffa49d0bc2'
    auth_token = '0bf99c49ad49f5c130805670391d2e6d'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=body,
        from_='+18148041711',
        to=to
    )

    print(f"Sent to {to}: {message.sid}")

import random
import smtplib
from email.message import EmailMessage

def send_otp(to_email, otp):
    sender_email = "elyaschaal974@gmail.com"
    sender_password = 'dbqq vmfw tgxh wlon'

    # Set up the server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    print('Server set up')
    # login to the server
    server.login(sender_email, sender_password)
    # Create the email message
    msg = EmailMessage()
    msg['Subject'] = 'Your OTP'
    msg['From'] = sender_email
    msg['To'] = to_email
    # write the OTP in the email message
    msg.set_content(f'Your OTP is {otp}')
    # Send the email
    server.send_message(msg)
    print('Message sent')





if __name__ == "__main__":
    recipient_email = "kostispapd@gmail.com"
    send_otp(recipient_email)

    #resp = requests.post('https://textbelt.com/text', {
    #    'phone': '5555555555',
    #    'message': 'Hello world',
    #    'key': 'textbelt',
    #})
    #print(resp.json())
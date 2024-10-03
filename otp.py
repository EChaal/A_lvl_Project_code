import random
import smtplib
from email.message import EmailMessage

def generate_otp():
    # Generate a random 6 digit number
    return random.randint(100000, 999999)

def send_otp(to_email):
    sender_email = "elyaschaal974@gmail.com"
    sender_password = 'dbqq vmfw tgxh wlon'

    # Set up the server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # login to the server
    server.login(sender_email, sender_password)
    # Create the email message
    msg = EmailMessage()
    msg['Subject'] = 'Random code for you my bro :)'
    msg['From'] = sender_email
    msg['To'] = to_email
    # create the OTP
    otp = generate_otp()
    # write the OTP in the email message
    msg.set_content(f'Your OTP is {otp}')
    # Send the email
    server.send_message(msg)
    print('Message sent')



recipient_email = "prestonwhiteman07@gmail.com"

send_otp(recipient_email)
from flask import Flask, request
from tropo import Tropo, Session
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import re
import os
import html2text

def sendEmail(recipient, subject, body):
    # Define variables
    username = os.environ["EMAIL_USER"]
    password = os.environ["EMAIL_PW"]
    server = os.environ["EMAIL_SERVER"]
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = username
    msg['To'] = recipient

    part1 = MIMEText(html2text.html2text(body), 'plain')
    part2 = MIMEText(body, 'html')

    msg.attach(part1)
    msg.attach(part2)

    mailsvr = smtplib.SMTP()
    mailsvr.connect(server,587)
    mailsvr._host = server
    mailsvr.ehlo()
    mailsvr.starttls()
    mailsvr.login(username, password)
    mailsvr.sendmail(msg['From'], msg['To'], msg.as_string())
    return True

def buildBody():
    html = """
    <html>
    <body>
    <h2>Cisco DevNet Happenings</h2>
    <p>Thank you for your interest in Cisco DevNet! Please check out <a href="http://developer.cisco.com">developer.cisco.com</a> for all things Cisco DevNet.</p>
    <p>Wondering what you can accomplish with DevNet? View some <a href="https://www.youtube.com/playlist?list=PL2k86RlAekM-k0Xez2X5Jl6v4-07C1T0j">innovator videos</a> on Youtube!</p>
    <p>Have questions? <a href="">Join a Spark Room</a> to talk directly with the DevNet team!</p>
    </body>
    </html>
    """
    return html


app = Flask(__name__)

@app.route("/devnet", methods=['POST'])
def devnet():
    s = Session(request.get_data().decode('utf-8'))
    text = str.strip(s.initialText)
    t = Tropo()
    if(re.fullmatch("[^@ ]+@[^ ]+\.[^@ ]+",text)):
        t.say("Thanks, sending email sent to " + text)
        htmlbody = buildBody()
        sendEmail(text, "Thanks for Visiting Cisco DevNet!", htmlbody)
    else:
        t.say("Text me your email address to receive info about DevNet!")
    return t.RenderJson()

@app.route("/")
def hello():
    return "Hello World"


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')

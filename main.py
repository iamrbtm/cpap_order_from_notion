import requests
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def check_for_orderables():
    url = "https://api.notion.com/v1/databases/ac64bba17a8e4a3aa696543024c86206/query"

    payload = json.dumps({
    "filter": {
        "property": "OrderNow",
        "checkbox": {
        "equals": True
        }
    }
    })
    headers = {
    'Content-Type': 'application/json',
    'Notion-Version': '2021-05-13',
    'Authorization': 'Bearer secret_E56vtGLhJHUK1o7WerXlnUaZHcbHnnlyFiMuPPwU1bz'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text

def send_email():
    
    # me == my email address
    # you == recipient's email address
    me = "rbtm2006@gmail.com"
    you = "rbtm2006@me.com"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Link"
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
    html = """\
    <html>
    <head></head>
    <body>
        <p>Hi!<br>
        How are you?<br>
        Here is the <a href="http://www.python.org">link</a> you wanted.
        </p>
    </body>
    </html>
    """

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()

    mail.starttls()

    mail.login('rbtm2006@gmail.com', 'password')
    mail.sendmail(me, you, msg.as_string())
    mail.quit()

items = json.loads(check_for_orderables())

file = open ('json.json', 'w')
file.write(items)
file.close()
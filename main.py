import requests
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

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

def send_email(items):
    
    # me == my email address
    # you == recipient's email address
    me = "ilyajlyadyfi@gmail.com"
    you = "rbtm2006@me.com"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Link"
    msg['From'] = me
    msg['To'] = you
    
    listofitems = ""
    for item in items:
        listofitems = listofitems + item + "\n"

    # Create the body of the message (a plain-text and an HTML version).
    text = listofitems
    html = """
    <html>
    <head></head>
    <body>
        <p>"""+listofitems+"""
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

    mail.login('ilyajlyadyfi@gmail.com', 'Braces10/')
    mail.sendmail(me, you, msg.as_string())
    mail.quit()

rawdata = check_for_orderables()

file = open ('json.json', 'w')
file.write(rawdata)
file.close()

items = json.loads(rawdata)
orderLineItems = []
for i in range(len(items['results'])):
    item = items['results'][i]['properties']['Item']['title'][0]['text']['content']
    itemNumber = items['results'][i]['properties']["Item#"]['rich_text'][0]['text']['content']
    lastOrdered = datetime.strptime(items['results'][i]['properties']["Last Ordered"]['date']['start'], '%Y-%m-%d')
    order = item + " (" + itemNumber + ") - Last Ordered: " + str(lastOrdered.strftime('%m/%d/%Y'))
    orderLineItems.append(order)

send_email(orderLineItems)

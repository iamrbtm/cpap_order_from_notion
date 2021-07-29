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
        listofitems = listofitems + item + "<br>"
    # Create the body of the message (a plain-text and an HTML version).
    text = listofitems
    html1 = """<!DOCTYPE html><html lang="en"><head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script> <script> $(document).ready(function () { $.ajax({ url: 'https://dailyverses.net/get/verse?language=niv&isdirect=1&url=' + window.location .hostname, dataType: 'JSONP', success: function (json) { $(".dailyVersesWrapper").prepend(json.html); } }); }); </script> <title>CPAP Supply Request </title> <style> .container { font-family: Verdana, Geneva, Tahoma, sans-serif; display: grid; grid-template-columns: 100%; grid-template-rows: auto auto auto auto; gap: 0px 0px; grid-auto-flow: row; grid-template-areas: "header" "order" "shipping" "footer"; } .order { grid-area: order; background-color: white; } .shipping { background-color: #eeeeee; display: grid; grid-template-columns: auto auto; grid-template-rows: auto; gap: 0px 0px; grid-template-areas: "customer ship"; grid-area: shipping; color: black; } .customer { grid-area: customer; font-size: 14px; text-align: center; } .ship { grid-area: ship; font-size: 14px; text-align: center; } .footer { grid-area: footer; background-color: black; color: #eeeeee; font-size: 10px; text-align: center; } .header { grid-area: header; background-color: #ffcc99; color: #242424; font-size: 30px; text-align: center; padding-top: 20px; padding-bottom: 20px; } .left { grid-area: left; } .right { grid-area: right; } </style></head><body> <div class="container"> <div class="order">"""
    html2 = """</div> <div class="shipping"> <div class="customer"> <table width="50%" border="0" align="center" cellpadding="5" cellspacing="0" style="border-collapse:collapse;background-color:#eeeeee;border:3px solid black;color:black;font-size:16px;font-family:Verdana, Geneva, Tahoma, sans-serif;"> <tbody> <tr> <td colspan="1" style="padding:5px;background-color:black;color:white;font-size:150%;text-align:center;"> Customer</td> </tr> <tr> <td style="background-color:white;">Jeremy Guill<br>dob:05/31/1978</td> </tr> </tbody> </table> </div> <div class="ship"> <table width="50%" border="0" align="center" cellpadding="5" cellspacing="0" style="border-collapse:collapse;background-color:#eeeeee;border:3px solid black;color:black;font-size:16px;font-family:Verdana, Geneva, Tahoma, sans-serif;"> <tbody> <tr> <td colspan="1" style="padding:5px;background-color:black;color:white;font-size:150%;text-align:center;"> Shipping</td> </tr> <tr> <td style="background-color:white;">Jeremy Guill<br>2408 SW Oakwood Drive<br>Dallas, Oregon 97338</td> </tr> </tbody> </table> </div> </div> <div class="footer"> <div class="dailyVersesWrapper"></div> </div> <div class="header"> CPAP Supply Request </div> <div class="left"></div> <div class="right"></div> </div></body></html>"""
    html = html1 + listofitems + html2
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

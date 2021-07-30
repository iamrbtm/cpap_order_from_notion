import requests
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, date

def auth(auth_name):
        with open("key.txt") as file:
            data = file.read()
            keys = json.loads(data)
        return keys[auth_name]

def update_lastordered_notion (pageid):
    url = "https://api.notion.com/v1/pages/"+ pageid

    payload = json.dumps({
    "properties": {
        "Last Ordered": {
        "date": {
            "start": date.today().strftime('%Y-%m-%d'),
            "end": None
        }
        }
    }
    })
    headers = {
    'Content-Type': 'application/json',
    'Notion-Version': '2021-05-13',
    'Authorization': 'Bearer ' + auth('notion')
    }

    response = requests.request("PATCH", url, headers=headers, data=payload)
    
    if response.status_code == 200:
        return
    else:
        print("Could not write to notion page" + str(pageid))
        comp_log.write("Could not write to notion page" + str(pageid)+"\n"+"\n")
        comp_log.close()
        quit()

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
    'Authorization': 'Bearer ' + auth('notion')
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    jsonResponse = json.loads(response.text)
    
    if response.status_code == 200:
        if len(jsonResponse['results']) > 0:
            return jsonResponse
        else:
            print("No Notion items to order.")
            comp_log.write("No Notion items to order."+"\n"+"\n")
            comp_log.close()
            quit()
    else:
        print("Problem getting info from Notion.  Try again")
        comp_log.write("Problem getting info from Notion.  Try again"+"\n"+"\n")
        comp_log.close()
        quit()

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
    
    listofitemshtml = ""
    listofitemstext = ""
    for item in items:
        listofitemshtml = listofitemshtml + "<li>" + item + "</li>"
        listofitemstext = listofitemstext + item + "\n"
    # Create the body of the message (a plain-text and an HTML version).
    html1 = """<!DOCTYPE html><html lang="en"><head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <style> @import url('https://fonts.googleapis.com/css2?family=Baloo+Chettan+2:wght@400;500;800&family=Nunito:wght@400;900&family=Poppins:ital,wght@0,400;1,700&family=Staatliches&display=swap'); </style> <title>CPAP Supply Request </title> <style> .container { font-family: Verdana, Geneva, Tahoma, sans-serif; display: grid; grid-template-columns: 100%; grid-template-rows: auto auto auto auto; gap: 0px 0px; grid-auto-flow: row; grid-template-areas: "header" "subheader" "shipping"; border-left: 2px solid #000000; border-right: 2px solid #000000; border-top: 2px solid #000000; border-bottom: 2px solid #000000; } .shipping { background-color: #eeeeee; display:grid; grid-template-columns: 60% 5% 35%; grid-template-rows: auto; gap: 0px 0px; grid-template-areas: "order . customer" "order . ship"; grid-area: shipping; color: black; padding-top: 20px; padding-bottom: 20px; padding-left: 20px;padding-right: 20px; } .order { grid-area: order; font-size: 14px; text-align: left; list-style: decimal; } .customer { grid-area: customer; font-size: 14px; text-align: center; } .ship { grid-area: ship; font-size: 14px; text-align: center; } .subheader { grid-area: subheader; background-color: #FFFFFF; color: #242424; font-size: 14px; text-align: left; padding-left: 20px; } .header { grid-area: header; background-color: #ffcc99; color: #242424; font-size: 30px; text-align: center; padding-top: 20px; padding-bottom: 20px; } .tableinfo { background-color: #FFFFFF; color: #242424; font-size: 14px; } .tableinfo_title { padding: 5px; background-color: #99CCFF; color: black; font-size: 150%; text-align: center; font-family: 'Baloo Chettan 2', cursive; } .tablestyle { background-color: #eeeeee; border: 2px solid black; font-family: 'Baloo Chettan 2', cursive; } </style></head><body> <div class="container"> <div class="shipping"> <div class="order"> <table width="100%" border="0" align="left" cellpadding="5" cellspacing="0" class="tablestyle"> <tbody> <tr> <td colspan="1" class="tableinfo_title"> Order </td> </tr> <tr> <td class="tableinfo">"""
    html2 = """</td> </tr> </tbody> </table> </div> <div class="customer"> <table width="75%" border="0" align="center" cellpadding="5" cellspacing="0" class="tablestyle"> <tbody> <tr> <td colspan="1" class="tableinfo_title""> Customer </td> </tr> <tr> <td class=" tableinfo"> Jeremy Guill<br>dob:05/31/1978<br>rbtm2006@me.com </td> </tr> </tbody> </table> </div> <div class="ship"> <table width="75%" border="0" align="center" cellpadding="5" cellspacing="0" class="tablestyle"> <tbody> <tr> <td colspan="1" class="tableinfo_title"> Shipping </td> </tr> <tr> <td class="tableinfo"> Jeremy Guill<br>2408 SW Oakwood Dr<br>Dallas, Oregon 97338 </td> </tr> </tbody> </table> </div> </div> <div class="header"> CPAP Supply Request </div> <div class="subheader"> Please fulfill the following request for CPAP supplies. </div> </div></body></html>"""
    html = html1 + listofitemshtml + html2
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(listofitemstext, 'plain')
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
comp_log = open ('completion log.txt', 'a')
comp_log.write(date.today().strftime('%m-%d-%Y')+"\n")
items = check_for_orderables()
count = len(items['results'])
print (str(count) + " items were found for re-order")
comp_log.write(str(count) + " items were found for re-order"+"\n")
print (90*"-")
comp_log.write(90*"-"+"\n")

orderLineItems = []

for i in range(count):
    item = items['results'][i]['properties']['Item']['title'][0]['text']['content']
    itemNumber = items['results'][i]['properties']["Item#"]['rich_text'][0]['text']['content']
    lastOrdered = datetime.strptime(items['results'][i]['properties']["Last Ordered"]['date']['start'], '%Y-%m-%d')
    order = item + " (" + itemNumber + ") - Last Ordered: " + str(lastOrdered.strftime('%m/%d/%Y'))
    orderLineItems.append(order)
    update_lastordered_notion(pageid=items['results'][i]['id'])
    print("Last Order field updated for item: " + str(item))
    comp_log.write("Last Order field updated for item: " + str(item)+"\n")

print (90*"-")
comp_log.write(90*"-"+"\n")
send_email(orderLineItems)
print("Email Sent Sucessfully")
comp_log.write("Email Sent Sucessfully"+"\n"+"\n")
comp_log.close()


import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import datetime
import os
from os.path import basename
from email.mime.application import MIMEApplication
from email.utils import COMMASPACE, formatdate

date_today = str(datetime.date.today())
server = "googlerelay.corp.endurance.com"
port = 25

emailfrom = "alan.jackson@endurance.com"
emailto = "alan.jackson@endurance.com"
fileToSend = str('C:/Users/aljackson/Documents/Environments/crypto_api/crypto_report_' + date_today + '.csv')
#username = "alan.jackson"
#password = "--x--"

msg = MIMEMultipart()
msg["From"] = emailfrom
msg["To"] = emailto
msg["Subject"] = str("Crypto Report for " + date_today)
msg.preamble = "See attached CSV for updated price movement."

ctype, encoding = mimetypes.guess_type(fileToSend)
if ctype is None or encoding is not None:
    ctype = "application/octet-stream"

maintype, subtype = ctype.split("/", 1)

if maintype == "text":
    fp = open(fileToSend)
    # Note: we should handle calculating the charset
    attachment = MIMEText(fp.read(), _subtype=subtype)
    fp.close()
elif maintype == "image":
    fp = open(fileToSend, "rb")
    attachment = MIMEImage(fp.read(), _subtype=subtype)
    fp.close()
elif maintype == "audio":
    fp = open(fileToSend, "rb")
    attachment = MIMEAudio(fp.read(), _subtype=subtype)
    fp.close()
else:
    fp = open(fileToSend, "rb")
    attachment = MIMEBase(maintype, subtype)
    attachment.set_payload(fp.read())
    fp.close()
    encoders.encode_base64(attachment)
attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
msg.attach(attachment)

server = smtplib.SMTP(server, port)
server.starttls()
server.sendmail(emailfrom, emailto, msg.as_string())
server.quit()

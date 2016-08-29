#!/usr/bin/python2.7

import sys
import os.path
# For guessing MIME type based on file name extension
import mimetypes
# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

# Command line argument handling.
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--address", help="smtp server address")
parser.add_argument("-s", "--sender", help="sender's address (from)", default="test_sender@wgproxy.org")
parser.add_argument("-r", "--recipient", help="recipient's address (to)", default="wyi@wgproxy.org")
parser.add_argument("-f", "--file", help="file path to attach in the email")
args = parser.parse_args()

if not args.address or not args.file:
	print "Error: Not enough arguments. Program aborted.\n"
	parser.print_help()
	sys.exit(1)

# Global debugging option
DEBUG = 1

outer = MIMEMultipart()
outer['From'] = args.sender
outer['To'] = args.recipient
outer['Subject'] = "SMTP Multipart Test message"
outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

body = "This is a test mail body."
outer.attach(MIMEText(body, 'plain'))

path = args.file
filename = os.path.basename(path)
# Guess the content type based on the file's extension.  Encoding
# will be ignored, although we should check for simple things like
# gzip'd or compressed files.
ctype, encoding = mimetypes.guess_type(path)
if ctype is None or encoding is not None:
    # No guess could be made, or the file is encoded (compressed), so
    # use a generic bag-of-bits type.
    ctype = 'application/octet-stream'
maintype, subtype = ctype.split('/', 1)
if maintype == 'text':
    fp = open(path)
    # Note: we should handle calculating the charset
    msg = MIMEText(fp.read(), _subtype=subtype)
    fp.close()
elif maintype == 'image':
    fp = open(path, 'rb')
    msg = MIMEImage(fp.read(), _subtype=subtype)
    fp.close()
elif maintype == 'audio':
    fp = open(path, 'rb')
    msg = MIMEAudio(fp.read(), _subtype=subtype)
    fp.close()
else:
    fp = open(path, 'rb')
    msg = MIMEBase(maintype, subtype)
    msg.set_payload(fp.read())
    fp.close()
    # Encode the payload using Base64
    encoders.encode_base64(msg)
# Set the filename parameter
msg.add_header('Content-Disposition', 'attachment', filename=filename)
outer.attach(msg)

# Now send or store the message
s = smtplib.SMTP(args.address)
s.set_debuglevel(DEBUG)
s.sendmail(args.sender, [args.recipient], outer.as_string())
s.quit()
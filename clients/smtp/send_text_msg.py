#!/usr/bin/python2.7

import sys
# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText

# Command line argument handling.
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--address", help="smtp server address")
parser.add_argument("-s", "--sender", help="sender's address (from)", default="test_sender@wgproxy.org")
parser.add_argument("-r", "--recipient", help="recipient's address (to)", default="wyi@wgproxy.org")
args = parser.parse_args()

if not args.address:
	print "Error: SMTP server address not specified. Program aborted.\n"
	parser.print_help()
	sys.exit(1)

# Global debugging option
DEBUG = 0

body = "This is a test mail body."
msg = MIMEText(body, 'plain')
msg['From'] = args.sender
msg['To'] = args.recipient
msg['Subject'] = "SMTP Simple Text Test message"

# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP(args.address)
s.set_debuglevel(DEBUG)
s.sendmail(args.sender, [args.recipient], msg.as_string())
s.quit()
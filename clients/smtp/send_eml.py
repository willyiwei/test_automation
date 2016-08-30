#!/usr/bin/python2.7

import sys
import os.path
# Import smtplib for the actual sending function
import smtplib

# Command line argument handling.
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--address", help="smtp server address")
parser.add_argument("-s", "--sender", help="sender's address (from)", default="test_sender@wgproxy.org")
parser.add_argument("-r", "--recipient", help="recipient's address (to)", default="wyi@wgproxy.org")
parser.add_argument("-f", "--file", help="file path the eml file")
args = parser.parse_args()

if not args.address or not args.file:
	print "Error: Not enough arguments. Program aborted.\n"
	parser.print_help()
	sys.exit(1)

# Global debugging option
DEBUG = 0

path = args.file
# Sanity check
if not os.path.isfile(path):
	print (path + 'not found.')
	sys.exit(1)

with open(path) as f:
	msg = f.read()
	f.close()

# Send the message via our own SMTP server, but don't include the
# envelope header.
try:
	s = smtplib.SMTP(args.address)
	s.set_debuglevel(DEBUG)
	s.sendmail(args.sender, [args.recipient], msg)
except Exception as e:
	print "Failed to send email, str(e)\n"
else:
	print "Email sent."
finally:
    s.quit()
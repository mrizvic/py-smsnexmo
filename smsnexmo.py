#!/usr/bin/python

import sys
import urllib
import urllib2
import json
import re
import argparse

def read_message():
	while True:
		print "Type your message in one line:"
		msg = sys.stdin.readline().strip()
		if (len(msg) < 1):
			print "message too short"
			continue
		return msg

def read_recipient(args):
	if (args.rcpt != "NULL"):
		print "Searching: " + args.rcpt
		i={}
		try:
			with open(args.file) as f:
				for line in f:
					if ( len(line)<2 or line[0] == ';'):
						continue
					(key,val) = re.split('\t+',line)
					i[key] = val
				f.close()
		except IOError as e:
			print "I/O error({0}): {1}".format(e.errno, e.strerror)+": "+args.file
		for k,v in i.items():
			if (k.find(args.rcpt) > -1):
				gsm = i[k].strip()
				print "Found: " +  k + " -> " + gsm
				if (gsm.isdigit() and len(gsm) == 9):
					return gsm
				print "check your number: " + gsm
				break
		print "Not found!"
		
	while True:
		print "Enter recipient's GSM number:"
		gsm = sys.stdin.readline().strip()
		if (gsm.isdigit() and len(gsm) == 9):
			return gsm
		print "check your number"
		continue

def send_sms(gsm,msg):
	#url	=	'https://rest.nexmo.com/sms/json'
	url		=	'dummy'
	values	=	{
			'username'	:	'CHANGEME',
			'password'	:	'CHANGEME',
			'from'		:	'CHANGEME',
			'type'		:	'text',
			'to'		:	gsm,
			'text'		:	msg
			}

	try:
		data = urllib.urlencode(values)
		req = urllib2.Request(url,data)
		response = urllib2.urlopen(req)
		the_page = response.read()
		d = json.loads(the_page)
		print json.dumps(d, indent=2)
		return 0
	except urllib2.HTTPError, e:
		print "HTTPError caught: ", e
		return 1
	except urllib2.URLError, e:
		print "URLError caught:", e
		return 1
	except ValueError, e:
		print "ValueError caught:", e
		return 1

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', action='store', dest='file', default='phonebook.txt', help='file containing tab delimited phonebook entries (default: phonebook.txt)')
	parser.add_argument('-r', '--recipient', action='store', dest='rcpt', default='NULL', help='lookup recipient in phonebook, if not specified you are asked to enter number manually')

	args = parser.parse_args()

	try:
		gsm = read_recipient(args)
		msg = read_message()
		print
		print gsm+ ":"+msg
		print
	except KeyboardInterrupt:
		print "CTRL+C caught... byebye"
		return 1

	print "Send? (yes/NO)"
	try:
		send = sys.stdin.readline()
	except KeyboardInterrupt:
		print "CTRL+C caught... byebye"
		return 1

	if (send.strip() == "yes"):
		print "sending..."
		return send_sms(gsm,msg)
	else:
		print "Aborted..."
		return 0
	

if __name__ == '__main__':
	main()

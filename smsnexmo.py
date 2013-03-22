#!/usr/bin/python

import sys
import urllib
import urllib2
import json
import re
import argparse

def read_message(text):
	if (text != 'NULL'):
		return text

	while True:
		print "Type your message in one line:"
		msg = sys.stdin.readline().strip()
		msglen = len(msg)
		if (msglen < 1):
			print "message too short"
			continue

		elif (msglen > 160):
			print "message too long:",msglen
			continue

		return msg

def read_recipient(args):
	if (args.rcpt != "NULL"):
		print "Searching: " + args.rcpt
		i={}
		try:
			with open(args.phonebook) as f:
				for line in f:
					if (len(line)<2 or line[0] == ';'):
						continue
					(key,val) = re.split('\t+',line)
					i[key] = val
				f.close()
		except IOError as e:
			print "I/O error({0}): {1}".format(e.errno, e.strerror)+": "+args.phonebook
		for k,v in i.items():
			if (k.find(args.rcpt) > -1):
				gsm = i[k].strip()
				print "Found: " +  k + " -> " + gsm
				if (gsm[1:].isdigit() and len(gsm) >= 12):
					return gsm
				print "check your number: " + gsm
				break
		
	while True:
		print "Enter recipient's GSM number:"
		gsm = sys.stdin.readline().strip()
		if (gsm[1:].isdigit() and len(gsm) >= 12):
			return gsm
		print "check your number"
		continue

def send_sms(sender,gsm,msg):
	url	=	'https://rest.nexmo.com/sms/json'

	u	=	'CHANGEME'
	p	=	'CHANGEME'

	if (u == p == 'CHANGEME'):
		print "you should change username and password"
		return 1

	values	=	{
			'username'	:	u,
			'password'	:	p,
			'from'		:	sender,
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

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--sender', action='store', dest='sender', default='NULL', help='From: SENDER')
	parser.add_argument('-p', '--phonebook', action='store', dest='phonebook', default='phonebook.txt', help='file containing tab delimited phonebook entries, default: ~/.talifonske.txt')
	parser.add_argument('-r', '--recipient', action='store', dest='rcpt', default='NULL', help='lookup recipient in phonebook')
	parser.add_argument('-t', '--text', action='store', dest='text', default='NULL', help='message for the recipient (example: -t \'hello world\')')
	parser.add_argument('-y', '--yes', action='store_true', dest='yes', default='no', help='answer yes to all questions')

	args = parser.parse_args()

	sender = args.sender
	text = args.text

	if (sender == 'NULL'):
		sender = 'CHANGEME'

	if (sender == 'CHANGEME'):
		print "you should change sender variable in source or specify --sender option "
		return 1

	try:
		msg = read_message(text)
		gsm = read_recipient(args)
		print
		print "From:",sender,"\n","To:",gsm,"\n","Text:",msg
		print
	except KeyboardInterrupt:
		print "CTRL+C caught... byebye"
		return 1

	if (args.yes == 'no'):
		print "Send? (yes/NO)"
		try:
			send = sys.stdin.readline()
		except KeyboardInterrupt:
			print "CTRL+C caught... byebye"
			return 1

	if (args.yes == True):
		send = 'yes'

	if (send.strip() == "yes"):
		print "sending..."
		return send_sms(sender,gsm,msg)
	else:
		print "Aborted..."
		return 0
	

if __name__ == '__main__':
	main()

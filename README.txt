ABOUT:
I wrote that for my personal use with SMS API provider http://www.nexmo.com

It reads a line that should contain GSM number of recipient followed by another single line of text message.
After user confirms his/her message by typing 'yes' the HTTP request is generated and executed against SMS API provider.

USAGE:
$ ./smsnexmo.py -h
usage: smsnexmo.py [-h] [-f FILE] [-r RCPT]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  file containing tab delimited phonebook entries
                        (default: phonebook.txt)
  -r RCPT, --recipient RCPT
                        lookup recipient in phonebook, if not specified you
                        are asked to enter number manually
$ cat phonebook.txt
;create entries in following order:
;<name>\tab<number>
;examples:
;john doe               080555123
;black smith    080555999
foo                             1
bar                             2
john                    090111222

$ ./smsnexmo.py
Enter recipient's GSM number:
090111222
Type your message in one line:
the answer is 42

090111222:the answer is 42

Send? (yes/NO)
yes
sending...

$ ./smsnexmo.py -r john
Searching: john
Found: john -> 090111222
Type your message in one line:
call me asap

090111222:call me asap

Send? (yes/NO)
yes
sending...

DISCLAIMER:
Before using this code please read documentation for your SMS API provider. This code is not universal and is provided "as is" without any warranty. I am not responsible for any damage that can be done by using this code.

import re

## The "INBOX" file is the file that contains all the emails data.
## I use Mozilla Thunderbird, so this file is located in
## "%APPDATA%\Thunderbird\Profiles\myprofilename\ImapMail\imap.gmail.com\INBOX".
## This file doesn't have extension in my case.
## Search where your email client software stores the file with all emails data,
## because it might be different for each software.

## Note: the inbox file should be saved with utf-8 encoding. If you want
## to use a different encoding, then change the encoding argument value accordingly on fhandle.


while True:
	mode = input("\n!# How do you want to group the emails count:\n1) 'complete email' (username@domain.com)" \
		"\n2) 'domain' (domain.com)\n\nType 'help' for more info. Type 'exit' to leave.\n>> ")
	valid_options = ['1', '2', 'help', 'exit']
	if mode not in valid_options:
		print("Invalid input. Type one of the numerical options")
		continue
	elif mode == 'help':
		print("You could have emails sent from different people, but same domain, for example: " \
			"Sarah sent you 3 emails, her email is sarah@company.com; Eddy sent you 1 email, his " \
			"email is eddy@company.com. In this case, if you choose 'domain', you will get the total " \
			"count of all emails received from 'company.com' (4 emails).\n")
		print("However, if you choose 'complete email', you will get a separate count for Sarah (3 emails) and " \
			" a separate count for Eddy (1 email).\n\n")
		continue
	elif mode == 'exit':
		print("Goodbye.")
		exit()
	break
	
print("\nProcessing...")

path_to_inbox = None
path_to_allMail = None

fhandle = open("./path_to_inbox.txt", "r")
for line in fhandle:
	path_to_inbox = line.strip()
fhandle.close()

fhandle = open("./path_to_allMail.txt", "r")
for line in fhandle:
	path_to_allMail = line.strip()
fhandle.close()

fhandle = open(path_to_allMail, 'r', encoding='latin-1')
emails = {}
lines = fhandle.readlines()
fhandle.close()
for n in range(len(lines)):
	lines[n] = lines[n].strip()

for line in lines:
	if line.startswith('From: ') == False:
		continue

	## Parenthesis in Regular Expressions findall() function arg value define which part of the string to extract.
	if mode == "1":
		email = re.findall("From: [\S\s]*<(\S+@\S+)>", line)
	elif mode == "2":
		email = re.findall("From: [\S\s]*<\S+(@\S+)>", line)
	if len(email) == 0:
		continue
	email = email[0]
	emails[email] = emails.get(email, 0) + 1

## This is so that we can count which emails have the highest email count and
## order them in descending order for an organized printing.
sorted_emails = sorted(list((v, k) for k, v in emails.items()), reverse=True)

## Compute possible exceptions for bad input and print out the results according
## to user input.
while True:
	top_count = input("\n!# How many entrances you want to see? Type 'exit' to leave. \n>> ")

	## If user types a number and doesn't intend to exit - top_count.lower() will return SyntaxError exception.
	try:
		if top_count.lower() == 'exit':
			print("Goodbye.")
			exit()
	except SyntaxError:
		pass

	## Checks if user typed a number.
	try:
		top_count = int(top_count)
	except ValueError:
		print("\nInvalid Input. Please enter a number.")
		continue

	## Input has to be bigger than 0; it refers to the length of sorted_emails list, which is expected to be > 1.
	if top_count <= 0:
		print('\nInvalid Input. Enter a number bigger than 0.')
		continue

	if top_count > len(sorted_emails):
		print("\nYour input is bigger than the amount of results, so" \
			" I'll just show all the results.")
		top_count = len(sorted_emails)

	for n in range(top_count):
		print("\n#########################")
		print("Top " + str(n + 1))
		print("sender: " + sorted_emails[n][1])
		print("emails count: " + str(sorted_emails[n][0]))

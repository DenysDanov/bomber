from email.mime.application import MIMEApplication
from posixpath import basename
from colorama import Fore
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import randint

import os
import smtplib
import argparse


'''
Example string
python main.py --header "exapmle header" --content content.txt --targetlist targets.txt -u userlist.txt
'''

class User:
    def __init__(self,mail_address,password) -> None:
        self.mail_address = mail_address
        self.password = password

# Argument parser
parser = argparse.ArgumentParser(description="gmail autosend")
parser.add_argument(
    '-u',
    '--user',
    type=str,
    required=True,
    help='''
    -u email_adress@example.com:password or
    -u file.txt
    '''
)
parser.add_argument(
    '--targetlist',
    type=str,
    required=True,
    help='''file with email@example.com'''
)
parser.add_argument(
    '--mode',
    type=str,
    default="every",
    help='''
    Modes:
    random — send mails from random account from list 
    every — send mail from every account to every target (default)
    '''
)
parser.add_argument(
    '--verbose',
    '-v',
    type=bool,
    default=False,
    help='''
    Print success and errors, you know
    '''
)
parser.add_argument(
    '-a',
    '--attachment',
    type=str,
    help='''
    Add attachment to your email
    '''
)
parser.add_argument(
    '--header',
    type=str,
    required=True,
    help='''
    Sets header text
    '''
)
parser.add_argument(
    '--content',
    type=str,
    required=True,
    help='''
    Sets content of email
    '''
)
parser.add_argument(
    '-t',
    '--timer',
    type=int,
    default=5,
    help='''
    Sets timer between <counter> emails
    '''
)
parser.add_argument(
    '--counter',
    default=100,
    type=int,
    help='''
    Sets count of email loadout
    '''
)

idx = 0
args = parser.parse_args()

COUNTER = args.counter
TIMER = args.timer
USERLIST = [args.user] if not os.path.isfile(args.user) else open(args.user).read().split('\n') 
VERBOSE = args.verbose
TARGETS = [i for i in open(args.targetlist,'rt').read().split('\n')]
USERS = [User(el.split(':')[0],el.split(':')[1]) for el in USERLIST]


mail_content = open(args.content).read() if os.path.isfile(args.content) else args.content
mail_header = open(args.header).read() if os.path.isfile(args.header) else args.header


def add_attachment(message, filename):
    try:
        attach_file = open(filename, 'rb')
        part = MIMEApplication(
                    attach_file.read(),
                    Name=basename(filename)
                )
            # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(filename)
        message.attach(part)
    except Exception as e:
        if VERBOSE: print(Fore.RED + f'[Err] {e} occured')
        pass

def send_mail(user,password,target,header,content):
    try:
        if VERBOSE: print(Fore.CYAN + f'{USER.mail_address}:', end=' ')
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = user
        message['To'] = target
        message['Subject'] = header

        #The body and the attachments for the mail
        message.attach(MIMEText(content, 'plain'))
        if args.attachment:
            add_attachment(message,args.attachment)

        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(user, password) #login with mail_id and password
        
        text = message.as_string()
        session.sendmail(user, target, text)
        session.quit()
    except Exception as e:
        if VERBOSE: print(Fore.RED + f'Error [{e}] occured')
        pass
    else:
        global idx
        idx += 1
        if VERBOSE: print(Fore.GREEN + f'{target} — mail sent successfully')
        
if __name__ == '__main__':
    for target in TARGETS:
        if args.mode == 'every':
            for USER in USERS:
                send_mail(USER.mail_address,USER.password, target,mail_header,mail_content)
        elif args.mode == 'random':
            USER = USERS[randint(0,len(USERS))]
            send_mail(USER.mail_address,USER.password, target,mail_header,mail_content)
        else:
            if VERBOSE: print(Fore.RED + '[ERROR] Unexpected --mode argument')
            pass

print(Fore.RESET+ f'{idx} emails sent')
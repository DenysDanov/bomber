from colorama import Fore
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import randint

import smtplib
import argparse


'''
Example string
python main.py --header header.txt --content content.txt --targetlist targets.txt -U userlist.txt
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
    help='''
    -u email_adress@example.com:password or
    --user email_adress@example.com:password
    '''
)
parser.add_argument(
    '-U',
    '--userlist',
    type=str,
    help='users.txt'
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
print(args)

if not args.userlist and not args.user:
    print(Fore.RED + '[ERROR] -u or -U required!')
if args.attachment:
    print("Attacments will be added later")

COUNTER = args.counter

TIMER = args.timer
USERLIST = [args.user] if args.user else open(args.userlist).read().split('\n') 
VERBOSE = args.verbose
TARGETS = [i for i in open(args.targetlist,'rt').read().split('\n')]

USERS = [User(el.split(':')[0],el.split(':')[1]) for el in USERLIST]
print([(el.mail_address,el.password) for el in USERS])
mail_content = open(args.content).read()
mail_header = open(args.header).read()

def send_mail(user,password,target,header,content):
    try:
        print(Fore.CYAN + f'{USER.mail_address}:')
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = user
        message['To'] = target
        message['Subject'] = header

        #The body and the attachments for the mail
        message.attach(MIMEText(content, 'plain'))

        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(user, password) #login with mail_id and password
        
        text = message.as_string()
        session.sendmail(user, target, text)
        session.quit()
    except Exception as e:
        print(Fore.RED + f'Error [{e}] occured')
    else:
        global idx
        idx += 1
        print(Fore.GREEN + f'{target} — mail sent successfully')
        


for target in TARGETS:
    if args.mode == 'every':
        for USER in USERS:
            send_mail(USER.mail_address,USER.password, target,mail_header,mail_content)
    elif args.mode == 'random':
        USER = USERS[randint(0,len(USERS))]
        send_mail(USER.mail_address,USER.password, target,mail_header,mail_content)
    else:
        print(Fore.RED + '[ERROR] Unexpected --mode argument')

print(Fore.RESET+ f'{idx} emails sent')
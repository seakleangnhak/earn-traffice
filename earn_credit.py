import requests
# import sys
import os
import signal
import numpy as np
from fake_useragent import UserAgent

ua = UserAgent()

session = requests.Session()
session.headers = {'User-Agent': ua.random}
cookie = ""
id = ""
token = ""
startBalance = 0.0
currentBalance = 0.0
totalBalance = 0.0
lastIP = ''
isError = False
durations = ['20', '30', '45']
links = [
    'https://rb.gy/zbqejd',
    'https://shorturl.at/bhyHJ',
    'https://tinyurl.com/ynhbhdkv',
    'https://t.ly/QYB3',
    'https://reurl.cc/Y8E8LX'
    ]


def login(email: str):
    global cookie
    global startBalance

    print('Login:', email)
    payload = dict(pochta=email, password='021044136')
    session.post('https://neon.today/welcome/login', data=payload)
    cookie = "neontoday=" + session.cookies.get_dict()['neontoday']
    print('Cookie:', cookie)

    startBalance = balance()
    print('Start Balance:', startBalance)

def earn():
    global id
    global isError

    r = session.post('https://neon.today/dash/earn')
    if ('id = ' in r.text):
        id = r.text.split('id = ')[1].split(';')[0]
        print('id:', id)
    elif ('There is no active ads for this moment' in r.text):
        isError = True
        print("There is no active ads for this moment")
        # sys.exit("There is no active ads for this moment")
    else:
        isError = True
        print(r.text)
        print("can't get start id")
        # sys.exit("can't get start id")

def balance() -> float:
    r = session.get('https://neon.today/index.php/dash/balance/')
    
    if r.text == '':
        return 0
    return float(r.text)

def isItFinished(id: str):
    global token
    global isError

    print('get new token.......')
    r = session.get('https://neon.today/index.php/surfing/isitfinished/' + id)

    if r.text == 'error' or r.text == '':
        isError = True
        print("can't get new token")
        # sys.exit("can't get new token")
    else:
        token = r.text
        print('token:', token)

def finish(token: str):
    global id
    global isError

    print('get new id.......')
    r = session.get('https://neon.today/index.php/surfing/fin/' + token)

    if 'id' in r.text:
        id = r.json()['id']
        print('id:', id)

    else:
        isError = True
        print("can't get new id, " + r.json())
        # sys.exit("can't get new id, " + r.json())

def addLink(link: str) -> bool:
    global durations
    global isError

    print('Add Link:', link)
    dur = np.random.choice(durations)
    payload = dict(url=link, duration=dur) #duration = 20(1), 30(1.5), 45(2), 60(3), 90(4)
    r = session.post('https://neon.today/index.php/surfing/add', data=payload)
    
    if 'Success' in r.text:
        print('add link success')
        return True
    else:
        print('>>>>>>>>>>>>> Add Link Error <<<<<<<<<<<<<<')
        return False

def getLinkID() -> int:
    id: int = None
    r = session.get('https://neon.today/advertise/surfing')

    if ('class="info" data-id="' in r.text):
        id = r.text.split('class="info" data-id="')[1].split('"')[0]
        print('link id:', id)

    return id

def addCredit(id: str, amt: float):

    r = session.get('https://neon.today/index.php/surfing/add_credits/'+id+'/'+str(amt))

    if 'Кредиты успешно добавлены' in r.text:
        print('add Credit success')
    else:
        print('>>>>>>>>>>>>> Add Credit Error <<<<<<<<<<<<<<')

def checkLink():
    global isError
    global link

    linkID = getLinkID()
    
    if linkID == None:
        if addLink(link):
            checkLink()
    
    else:
        amt = balance()
        addCredit(linkID, amt)

def checkIP() -> str:
    return ''
    # r = requests.get('https://api.ipify.org/?format=json')
    # return r.json()['ip']

def changeIP():
    # global lastIP

    vpn = np.random.choice(["CA", "DE", "HK", "GB", "US"])
    # os.system('windscribe disconnect')
    os.system('windscribe connect ' + vpn)

    # ip = checkIP()

    # if lastIP == ip:
    #     changeIP()
    # else:
    #     lastIP = ip


def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        exit(1)
 
signal.signal(signal.SIGINT, handler)


accountNum = input('Account Number: ')
lastIP = checkIP()
f = open('accounts'+accountNum+'.txt', 'r')
emails = f.readlines()
f.close()

# emails = [input('Email:')]
startAt = int(input('Start at:'))

while True:
    for i in range(len(emails)):

        if i < startAt:
            continue
        elif startAt != 0:
            startAt = 0

        email = emails[i]
        link = np.random.choice(links)

        try:
            changeIP()
            login(email.strip())
            earn()

            while isError == False:
                isItFinished(id)
                finish(token)

                print('getting balance......')
                currentBalance = balance()
                print('current balance '+i+':', currentBalance)
                print('total balance:', currentBalance + totalBalance)

        except:
            isError = True
            print('except', i)

        try:
            checkLink()
        except:
            isError = True
            print('except', i)


        totalBalance += currentBalance
        session = requests.Session()
        cookie = ""
        id = ""
        token = ""
        startBalance = 0.0
        currentBalance = 0.0
        isError = False

    print('Fished Total Balance is:', totalBalance)
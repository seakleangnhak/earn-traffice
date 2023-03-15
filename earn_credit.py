import requests
# import sys
import os
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

def checkIP() -> str:
    r = requests.get('https://api.ipify.org/?format=json')
    return r.json()['ip']

def changeIP():
    global lastIP
    
    os.system('windscribe connect')

    ip = checkIP()

    if lastIP == ip:
        changeIP()
    else:
        lastIP = ip






lastIP = checkIP()
f = open("accounts.txt", "r")
emails = f.readlines()
f.close()

startAt = int(input('Start at:'))

while True:
    for i in range(len(emails)):

        if i < startAt:
            continue
        elif startAt != 0:
            startAt = 0

        email = emails[i]

        changeIP()
        # login(input("email:"))
        login(email.strip())
        earn()

        while isError == False:
            try:
                isItFinished(id)
                finish(token)

                print('getting balance......')
                currentBalance = balance()
                print('current balance:', currentBalance)
                print('total balance:', currentBalance + totalBalance)
                
            except:
                isError = True
                print('except')

        totalBalance += currentBalance
        session = requests.Session()
        cookie = ""
        id = ""
        token = ""
        startBalance = 0.0
        currentBalance = 0.0
        isError = False

    print('Fished Total Balance is:', totalBalance)
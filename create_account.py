import numpy as np
import requests
import signal
from faker import Faker
from fake_useragent import UserAgent


fake = Faker()
ua = UserAgent()
accountNum = input('Account Number: ')
qtyAcc = int(input('QTY for new account: '))

def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        exit(1)
 
signal.signal(signal.SIGINT, handler)

for i in range(qtyAcc) :

    gender = np.random.choice(["M", "F"], p=[0.5, 0.5])
    first_name = fake.first_name_male() if gender =="M" else fake.first_name_female()
    last_name = fake.last_name()
    email = f"{first_name}.{last_name}@{fake.domain_name()}".lower()

    print('Register'+str(i)+':', email)

    payload = dict(email=email, password='021044136', read='on')
    r = requests.post('https://neon.today/welcome/register', data=payload, headers = {'User-Agent': ua.random})

    if 'Success' in r.text:
        print('Register Success')

        f = open('accounts'+accountNum+'.txt', 'a')
        f.write(email + '\n')
        f.close()

    else:
        print('Register fail')
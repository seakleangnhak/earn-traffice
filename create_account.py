import numpy as np
import requests
from faker import Faker


fake = Faker()

for i in range(30) :

    gender = np.random.choice(["M", "F"], p=[0.5, 0.5])
    first_name = fake.first_name_male() if gender =="M" else fake.first_name_female()
    last_name = fake.last_name()
    email = f"{first_name}.{last_name}@{fake.domain_name()}".lower()

    print('Register'+str(i)+':', email)

    payload = dict(email=email, password='021044136', read='on')
    r = requests.post('https://neon.today/welcome/register', data=payload)

    if 'Success' in r.text:
        print('Register Success')

        f = open("accounts.txt", "a")
        f.write(email + '\n')
        f.close()

    else:
        print('Register fail')
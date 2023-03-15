# from time import sleep

# count = 0
# while True:
#     count += 1
#     print('count:', count)
#     sleep(1)

i = [0,1]

try:
    j = i.json()
except:
    print('except')
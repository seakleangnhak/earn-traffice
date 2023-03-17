# import pyshorteners

# long_url = input("Enter the URL to shorten: ")

# shortener = pyshorteners.Shortener()

# short_url = shortener.tinyurl.short(long_url)
 
# print("The Shortened URL is: " + short_url)



import signal

def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        exit(1)
 
signal.signal(signal.SIGINT, handler)

count = 1
while True:
    print(count)
    count += 1
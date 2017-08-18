from random import randint

def translate_testserver_to_localhost(url):
    if url.index('testserver'):
        return url.replace('testserver', 'localhost:8000')

def randomNumber(numberLen):
    string = ''
    for i in range(numberLen):
        string+= str(randint(0,9))
    return string
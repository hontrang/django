def translate_testserver_to_localhost(url):
    if url.index('testserver'):
        return url.replace('testserver', 'localhost:8000')
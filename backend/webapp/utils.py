import time
import os
import ast

from django.conf import settings
class FileHandle():
    @staticmethod
    def saveFileLocal(source):
        filesrc = source
        ch = filesrc.chunks()
        filename = "%s-%s" %(str(time.time()).replace('.','_'), filesrc.name)
        with open('%s/%s' %(settings.STATICFILES_DIRS, filename ), 'w+b') as file:
            for d in ch:
                file.write(d)
            file.close()
        return filename
    @staticmethod
    def deleteExistedLocal(source):
        filename = '%s/%s' %(settings.STATICFILES_DIRS, source )
        if os.path.isfile(filename):
            try:
                os.remove(filename)
                return filename
            except OSError as e:
                print ("Error: %s - %s." % (e.filename,e.strerror))
                return e.filename
    @staticmethod
    def convertStringToDict(data):
        if type(data) is str:
            return ast.literal_eval(data)

class HTMLParser():
    @staticmethod
    def is_html_input(dictionary):
        # MultiDict type datastructures are used to represent HTML form input,
        # which may have more than one value for each key.
        return hasattr(dictionary, 'getlist')

    @staticmethod
    def parse_html_list(dictionary, prefix=''):
        """
        Used to support list values in HTML forms.
        Supports lists of primitives and/or dictionaries.
        * List of primitives.
        {
            '[0]': 'abc',
            '[1]': 'def',
            '[2]': 'hij'
        }
            -->
        [
            'abc',
            'def',
            'hij'
        ]
        * List of dictionaries.
        {
            '[0]foo': 'abc',
            '[0]bar': 'def',
            '[1]foo': 'hij',
            '[1]bar': 'klm',
        }
            -->
        [
            {'foo': 'abc', 'bar': 'def'},
            {'foo': 'hij', 'bar': 'klm'}
        ]
        """
        ret = {}
        regex = re.compile(r'^%s\[([0-9]+)\](.*)$' % re.escape(prefix))
        for field, value in dictionary.items():
            match = regex.match(field)
            if not match:
                continue
            index, key = match.groups()
            index = int(index)
            if not key:
                ret[index] = value
            elif isinstance(ret.get(index), dict):
                ret[index][key] = value
            else:
                ret[index] = MultiValueDict({key: [value]})
        return [ret[item] for item in sorted(ret.keys())]

    @staticmethod
    def parse_html_dict(dictionary, prefix=''):
        """
        Used to support dictionary values in HTML forms.
        {
            'profile.username': 'example',
            'profile.email': 'example@example.com',
        }
            -->
        {
            'profile': {
                'username': 'example',
                'email': 'example@example.com'
            }
        }
        """
        ret = MultiValueDict()
        regex = re.compile(r'^%s\.(.+)$' % re.escape(prefix))
        for field in dictionary:
            match = regex.match(field)
            if not match:
                continue
            key = match.groups()[0]
            value = dictionary.getlist(field)
            ret.setlist(key, value)

        return ret
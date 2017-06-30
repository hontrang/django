import time
import os

from django.conf import settings
class FileHandle():
    def saveFileLocal(self, source):
        filesrc = source
        ch = filesrc.chunks()
        filename = "%s-%s" %(str(time.time()).replace('.','_'), filesrc.name)
        with open('%s/%s' %(settings.STATICFILES_DIRS, filename ), 'w+b') as file:
            for d in ch:
                file.write(d)
            file.close()
        return filename
    
    def deleteExistedLocal(self, source):
        filename = '%s/%s' %(settings.STATICFILES_DIRS, source )
        if os.path.isfile(filename):
            try:
                os.remove(filename)
                return filename
            except OSError as e:
                print ("Error: %s - %s." % (e.filename,e.strerror))
                return e.filename


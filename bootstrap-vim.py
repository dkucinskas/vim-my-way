import os
import sys
import subprocess
import urllib2
import zipfile
import re

class Task(object):
    def __init__(self, name):
        self.name = name
        self.success = False
        self.result = None
        self.error = None

    def before(self):
        print "Starting: [{0}]".format(self.name)

    def do(self):
        pass

    def after(self):
        if self.success:
            print "Success [{0}]".format(self.name)
        else:
            print "FAILED [{0}] Error: [{1}]".format(self.name, self.error)

class CopyFile(Task):
    def __init__(self, path_src, path_des):
        super(CopyFile, self).__init__("Copy file src: '%s' des: '%s'" % (path_src, path_des))
        self.path_src = path_src
        self.path_des = path_des

    def do(self):
        if sys.platform.startswith('win32'):
            self.success = subprocess.call('echo f | xcopy /F /Y "{0}" "{1}"'.format(self.path_src, self.path_des), shell=True) == 0
        elif sys.platform.startswith('linux'):
            self.success = subprocess.call('cp {0} {1}'.format(self.path_src, self.path_des), shell=True) == 0

class DownloadFile(Task):
    def __init__(self, url, path):
        super(DownloadFile, self).__init__("Download url: '%s' path: '%s'" % (url, path))
        self.url = url
        self.path = path

    def do(self):
        if not os.path.isfile(self.path):
            u = urllib2.urlopen(self.url)
            file_handle = open(self.path, 'wb')
            meta = u.info()
            file_size = int(meta.getheaders("Content-Length")[0])

            print "Downloading: %s Bytes: %s" % (self.path, file_size)

            file_size_dl = 0
            block_sz = 8192
            while True:
                buff = u.read(block_sz)
                if not buff:
                    break

                file_size_dl += len(buff)
                file_handle.write(buff)
                status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                status += chr(8) * (len(status) + 1)
                print status,\

            file_handle.close()

        self.success = True

class MakeDirectory(Task):
    def __init__(self, path):
        super(MakeDirectory, self).__init__("Make directory: '%s'" % (path, ))
        self.path = path

    def do(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        self.success = True

class AddPlugin(Task):
    def __init__(self, url, path):
        super(AddPlugin, self).__init__("Add plugin from url: '%s' path: '%s'" % (url, path))
        self.url = url
        self.path = path

    def do(self):
        current_dir = os.getcwd()
        os.chdir(self.path)
        
        self.success = subprocess.call("git clone %s" % (self.url,), shell=True) == 0

        os.chdir(current_dir)

class CleanEOL(Task):
    def __init__(self, path, old_eol, new_eol):
        super(CleanEOL, self).__init__("Clean EOL marks in file: '%s'" % (path, ))
        self.path = path
        self.old_eol = old_eol
        self.new_eol = new_eol

    def do(self):
	data = open(self.path, "rb").read()
        newdata = data.replace(self.old_eol, self.new_eol)
        if newdata != data:
            f = open(self.path, "wb")
            f.write(newdata)
            f.close()
        
        self.success = True


if __name__ == "__main__":

    dir_source = os.path.dirname(os.path.abspath(__file__))
    file_src_vimrc = os.path.join(dir_source, '_vimrc')

    dir_output = None
    file_des_vimrc = None
    if sys.platform.startswith('linux'):
        dir_output = os.path.join(os.path.expanduser('~'), '.vim')
        file_des_vimrc = os.path.join(os.path.expanduser('~'), '.vimrc')
    elif sys.platform.startswith('win32'):
        dir_output = os.path.join(os.path.expanduser('~'), 'vimfiles')
        file_des_vimrc = os.path.join(os.path.expanduser('~'), '_vimrc')
    
    dir_bundle = os.path.join(dir_output, 'bundle')
    dir_autoload = os.path.join(dir_output, 'autoload')
    
    url_pathogen = 'https://raw.github.com/tpope/vim-pathogen/master/autoload/pathogen.vim';
    file_pathogen = os.path.join(dir_autoload, 'pathogen.vim')

    tasks = [
        MakeDirectory(dir_output),
        MakeDirectory(dir_autoload),
        MakeDirectory(dir_bundle),
        DownloadFile(url_pathogen, file_pathogen),
        CopyFile(file_src_vimrc, file_des_vimrc),
	CleanEOL(file_des_vimrc, "\r\n", "\n"),
        AddPlugin('https://github.com/scrooloose/nerdtree.git', dir_bundle),
        AddPlugin('https://github.com/endel/vim-github-colorscheme.git', dir_bundle),
        AddPlugin('https://github.com/altercation/vim-colors-solarized.git', dir_bundle),
        AddPlugin('https://github.com/29decibel/codeschool-vim-theme.git', dir_bundle),
        AddPlugin('https://github.com/noahfrederick/vim-hemisu.git', dir_bundle),
        AddPlugin('https://github.com/tomasr/molokai.git', dir_bundle),
        AddPlugin('https://github.com/dkucinskas/vim-javascript.git', dir_bundle)
    ]

    success = True
    for task in tasks:
        task.before()
        task.do()
        task.after()

        if not task.success:
            success = False
            break

    if success:
        print '[SUCCEEDED]'
    else:
        print '[FAILED]'

import os
import sys
import subprocess
import urllib.request
import zipfile


class Task(object):
    def __init__(self, name):
        self.name = name
        self.success = False
        self.result = None
        self.error = None

    def before(self):
        print("Starting: [{0}]".format(self.name))

    def do(self):
        pass

    def after(self):
        if self.success:
            print("Success [{0}]".format(self.name))
        else:
            print("FAILED [{0}] Error: [{1}]".format(self.name, self.error))


class CopyFile(Task):
    def __init__(self, path_src, path_des):
        super(CopyFile, self).__init__("Copy file src: '%s' des: '%s'" % (path_src, path_des))
        self.path_src = path_src
        self.path_des = path_des

    def do(self):
        if sys.platform.startswith('win32'):
            x_copy = 'echo f | xcopy /F /Y "{0}" "{1}"'
            self.success = subprocess.call(x_copy.format(self.path_src, self.path_des), shell=True) == 0
        elif sys.platform.startswith('linux'):
            self.success = subprocess.call('cp {0} {1}'.format(self.path_src, self.path_des), shell=True) == 0


class DownloadFile(Task):
    def __init__(self, url, path):
        super(DownloadFile, self).__init__("Download url: '%s' path: '%s'" % (url, path))
        self.url = url
        self.path = path

    def do(self):
        if not os.path.isfile(self.path):
            response = urllib.request.urlopen(self.url)
            file_handle = open(self.path, 'wb')
            headers = response.info()
            file_size = int(headers["Content-Length"])

            print("Downloading: %s Bytes: %s" % (self.path, file_size))

            file_size_dl = 0
            block_sz = 8192
            while True:
                buff = response.read(block_sz)
                if not buff:
                    break

                file_size_dl += len(buff)
                file_handle.write(buff)
                status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                status += chr(8) * (len(status) + 1)
                print(status)

            file_handle.close()

        self.success = True


class MakeDirectory(Task):
    def __init__(self, path):
        super(MakeDirectory, self).__init__("Make directory: '%s'" % (path,))
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
        super(CleanEOL, self).__init__("Clean EOL marks in file: '%s'" % (path,))
        self.path = path
        self.old_eol = old_eol
        self.new_eol = new_eol

    def do(self):
        data = open(self.path, "rb").read()
        new_data = data.decode('UTF-8').replace(self.old_eol, self.new_eol)
        if new_data != data:
            f = open(self.path, "wb")
            f.write(bytes(new_data, 'UTF-8'))
            f.close()

        self.success = True


class Unzip(Task):
    def __init__(self, archive, out_dir):
        super(Unzip, self).__init__("Unzip file: '%s' into directory: '%s'" % (archive, out_dir))
        self.archive = archive
        self.out_dir = out_dir

    def do(self):
        zfile = zipfile.ZipFile(self.archive)
        for name in zfile.namelist():
            (dirname, filename) = os.path.split(name)
            print("Decompressing filename: '%s' into directory: '%s'" % (filename, dirname))
            full_path = os.path.join(self.out_dir, dirname)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            zfile.extract(name, full_path)

        self.success = True


class WinRunRegFile(Task):
    def __init__(self, path_src):
        super(WinRunRegFile, self).__init__("Run reg file: '%s'" % path_src)
        self.path_src = path_src

    def do(self):
        if sys.platform.startswith('win32'):
            cmd = 'regedit /s "{0}"'
            self.success = subprocess.call(cmd.format(self.path_src), shell=True) == 0
        # elif sys.platform.startswith('linux'):
        #    self.success = subprocess.call('cp {0} {1}'.format(self.path_src, self.path_des), shell=True) == 0


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
    dir_fonts = os.path.join(dir_bundle, 'fonts')
    dir_font_envy = os.path.join(dir_fonts, 'envy-code-r')

    # url_pathogen ='https://raw.github.com/tpope/vim-pathogen/master/autoload/pathogen.vim'
    url_pathogen = 'https://tpo.pe/pathogen.vim'
    file_pathogen = os.path.join(dir_autoload, 'pathogen.vim')

    url_envy_code_r = 'http://download.damieng.com/fonts/original/EnvyCodeR-PR7.zip'
    file_envy_code_r_zip = os.path.join(dir_fonts, 'EnvyCodeR-PR7.zip')
    dir_envy_code_r = os.path.join(dir_fonts, 'Envy Code R PR7', 'Envy Code R PR7')
    file_envy_code_r_font_1 = os.path.join(dir_envy_code_r, 'Envy Code R.ttf')
    file_envy_code_r_font_2 = os.path.join(dir_envy_code_r, 'Envy Code R Bold.ttf')
    file_envy_code_r_font_3 = os.path.join(dir_envy_code_r, 'Envy Code R Italic.ttf')
    file_envy_code_r_reg = os.path.join(dir_envy_code_r, 'Envy Code R Command Prompt.reg')

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
        AddPlugin('https://github.com/dkucinskas/vim-javascript.git', dir_bundle),
        AddPlugin('https://github.com/kien/ctrlp.vim.git', dir_bundle),
        AddPlugin('https://github.com/rust-lang/rust.vim.git', dir_bundle),
    ]

    # windows specific steps
    if sys.platform.startswith('win32'):
        tasks.append(MakeDirectory(dir_fonts))
        tasks.append(DownloadFile(url_envy_code_r, file_envy_code_r_zip))
        tasks.append(Unzip(file_envy_code_r_zip, dir_fonts))
        tasks.append(CopyFile(file_envy_code_r_font_1, '%systemroot%/fonts'))
        tasks.append(CopyFile(file_envy_code_r_font_2, '%systemroot%/fonts'))
        tasks.append(CopyFile(file_envy_code_r_font_3, '%systemroot%/fonts'))
        # this won't work go to font dir and run font install manually
        # tasks.append(WinRunRegFile(file_envy_code_r_reg))

    success = True
    for task in tasks:
        task.before()
        task.do()
        task.after()

        if not task.success:
            success = False
            break

    if success:
        print('[SUCCEEDED]')
    else:
        print('[FAILED]')

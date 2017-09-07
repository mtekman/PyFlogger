#/usr/bin/env python3

from xdg.BaseDirectory import xdg_config_home
from os.path import join as pjoin, exists, sep, expanduser, normpath
from os import mkdir


# Defaults
__config_dir = pjoin( xdg_config_home, 'foodlogger')
user_foodlist = pjoin( __config_dir, 'list.txt'  )
user_foodlog  = pjoin( __config_dir, 'log.txt'   )
user_weightlog= pjoin( __config_dir, 'weight.txt')

# Custom user
user_config_file = pjoin( expanduser('~'), '.pyflogrc' )

if exists( user_config_file ):
    # ConfigParser is a bit much for this, just use simple read
    with open(user_config_file, 'r') as conf:

        for line in conf:
            tokens = line.splitlines()[0].split('=')
            if tokens[0].startswith('user_foodlist'):
                user_foodlist = normpath( tokens[1].strip() )
            elif tokens[0].startswith('user_foodlog'):
                user_foodlog = normpath( tokens[1].strip() )
            elif tokens[0].startswith('user_weightlog'):
                user_weightlog = normpath( tokens[1].strip() )

        # if not all found, defaults are used
        conf.close()






class Config:

    @staticmethod
    def resolveAllPaths(): # called from main
        Config.resolvePath(user_foodlist)
        Config.resolvePath(user_foodlog)
        Config.resolvePath(user_weightlog)


    @staticmethod
    def resolvePath(filepath):
        Config.__touch(filepath)


    @staticmethod
    def __touch(filename):
        if not exists(filename):

            print("[INFO]", filename, "does not exist -- creating new")

            direc = sep.join(filename.split(sep)[:-1])
            if not exists(direc):
                mkdir( direc )

            # Open file and write blank
            with open(filename,'w') as f:
                f.write("\n")
                f.close()

        return filename

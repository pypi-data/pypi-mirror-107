import datetime


__version_info__ = (int(datetime.datetime.now().strftime("%Y")), 0,)
__version_postfix__ = ".dev" + datetime.datetime.now().strftime("%Y") + "0"  # branch
__version__ = ".".join(map(str, __version_info__)) + __version_postfix__

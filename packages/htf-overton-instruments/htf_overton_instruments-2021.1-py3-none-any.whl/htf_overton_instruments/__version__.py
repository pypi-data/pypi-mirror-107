import datetime


__version_info__ = (int(datetime.datetime.now().strftime("%Y")), 1,)
__version__ = ".".join(map(str, __version_info__))

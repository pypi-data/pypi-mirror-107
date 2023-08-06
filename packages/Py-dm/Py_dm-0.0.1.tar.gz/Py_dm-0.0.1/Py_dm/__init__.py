'''
模块说明：模块使用大漠3.1233版本集成鼠标，键盘，图等模块，后续会继续完善。
操作系统：win7,64位专业版，使用前先把dm.dll注册到系统才能正常使用
'''
from . import regserdm
from .regserdm import *
from . import pic
from .pic import *
from .import mouse
from .mouse import *
from .import window
from .window import *
from . import string
from .string import *
print('Py_dm插件版本：',1.1)
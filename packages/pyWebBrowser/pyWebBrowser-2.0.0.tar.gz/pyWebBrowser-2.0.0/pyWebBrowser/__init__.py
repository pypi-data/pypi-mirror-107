# -*- coding: utf-8 -*-

'''
项目介绍:
开发者  : Yogurt_cry
模块说明: 1. webBrowser.Browser()   : 浏览器控制
　　　　  2. webBrowser.Mouse()     : 鼠标控制
　　　　  3. webBrowser.Keyboard()  : 键盘控制
　　　　  4. webBrowser.Screenshot(): 屏幕截图
　　　　  5. webBrowser.Clipboards(): 剪切板控制
'''

import clr
clr.AddReference('pyWebBrowser/WebBrowser/webBrowser')
import webBrowser

__title__ = 'pyWebBrowser'
__description__ = '基于 C# 开发的浏览器控制工具。整合提供了浏览器控制、键鼠控制、屏幕截图、剪切板控制等常用 API'
__url__ = 'https://gitee.com/Yogurt_cry/pyWebBrowser'
__version__ = 'v2.0.0.0'
__build__ = ''
__author__ = 'Yogurt_cry'
__author_email__ = 'ben.2001@foxmail.com'
__license__ = 'MIT License'
__copyright__ = 'CCSDESIGN'

class Browser:
    def __init__(self):
        '''
        浏览器控制
        '''
        self.__browser = webBrowser.Browser()
    
    def Create(self, width: int = 1024, height: int = 768, topMost: bool = False):
        '''
        创建浏览器
        :param width  : int.  选填。窗体宽度。默认 1024
        :param height : int.  选填。窗体高度。默认 768
        :param topMost: bool. 选填。窗体置顶状态。默认 False。True: 置顶; False: 不置顶
        '''
        self.__browser.Create(width, height, topMost)
    
    def Open(self, url: str):
        '''
        打开网页
        :param url: str.  必填。网页链接
        '''
        self.__browser.Open(url)
    
    def Download(self, url: str, downloadPath: str):
        '''
        下载文件
        :param url         : str.  必填。下载链接
        :param downloadPath: str.  必填。保存路径
        '''
        self.__browser.Download(url, downloadPath)
    
    def Html(self) -> str:
        '''
        获取网页源代码
        :return str. 返回主页面源代码(不含 iFrame 框架)
        '''
        return self.__browser.Html()
    
    def ElementLocation(self, xpath: str) -> str:
        '''
        获取指定元素坐标
        :param xpath: str. 必填。定位元素的 xpath 语句
        :return str. 返回 xpath 指定元素的坐标信息字符串。格式: [[x, y, width, height]]
        '''
        return self.__browser.ElementLocation(xpath)

    def ExecJS(self, query: str):
        '''
        执行 javaScript 语句
        :param query: str. 必填。需要执行的 javaScript 语句
        :return object. 返回执行语句的结果
        '''
        return self.__browser.ExecJS(query)
    
    def Close(self):
        '''
        关闭浏览器
        '''
        self.__browser.Close()

class Mouse:
    def __init__(self):
        '''
        鼠标控制
        '''
        self.__mouse = webBrowser.Mouse()
    
    def LeftDown(self):
        '''
        左键按下
        '''
        self.__mouse.LeftDown()
    
    def LeftUp(self):
        '''
        左键抬起
        '''
        self.__mouse.LeftUp()
    
    def LeftClick(self):
        '''
        左键单击
        '''
        self.__mouse.LeftClick()
    
    def RightDown(self):
        '''
        右键按下
        '''
        self.__mouse.RightDown()
    
    def RightUp(self):
        '''
        右键抬起
        '''
        self.__mouse.RightUp()
    
    def RightClick(self):
        '''
        右键单击
        '''
        self.__mouse.RightClick()
    
    def MiddleDown(self):
        '''
        中键按下
        '''
        self.__mouse.MiddleDown()
    
    def MiddleUp(self):
        '''
        中键抬起
        '''
        self.__mouse.MiddleUp()
    
    def MiddleClick(self):
        '''
        中键单击
        '''
        self.__mouse.MiddleClick()
    
    def Move(self, x: int, y: int):
        '''
        鼠标移动
        :param x: int. 必填。x 坐标
        :param y: int. 必填。y 坐标 
        '''
        self.__mouse.Move(x, y)
    
    def SmoothMove(self, startX: float, startY: float, endX: float, endY: float, pointCount: int = 10, moveSpeed: int = 5):
        '''
        鼠标平滑直线移动
        :param startX    : float. 必填。起始点 x 坐标
        :param startY    : float. 必填。起始点 y 坐标
        :param endX      : float. 必填。终止点 x 坐标
        :param endY      : float. 必填。终止点 y 坐标
        :param pointCount: int. 选填。拆分点数量
        :param moveSpeed : int. 选填。移动总速度
        '''
        self.__mouse.SmoothMove(startX, startY, endX, endY, pointCount, moveSpeed)
        
class Keyboard:
    def __init__(self):
        '''
        键盘控制
        '''
        self.__keyboard = webBrowser.Keyboard()
    
    def KeyDown(self, keyName: str = None, keyValue: int = -1):
        '''
        键盘按键按下
        :param keyName : str. 非必填但 keyName/keyValue 必填一个。键盘按键值
        :param keyValue: int. 非必填但 keyName/keyValue 必填一个。键盘按键 ASCII 值
        '''
        
        self.__keyboard.KeyDown(keyName, keyValue)
    
    def KeyUp(self, keyName: str = None, keyValue: int = -1):
        '''
        键盘按键弹起
        :param keyName : str. 非必填但 keyName/keyValue 必填一个。键盘按键值
        :param keyValue: int. 非必填但 keyName/keyValue 必填一个。键盘按键 ASCII 值
        '''
        
        self.__keyboard.KeyUp(keyName, keyValue)
    
    def KeyPress(self, keyName: str = None, keyValue: int = -1):
        '''
        键盘按键单击
        :param keyName : str. 非必填但 keyName/keyValue 必填一个。键盘按键值
        :param keyValue: int. 非必填但 keyName/keyValue 必填一个。键盘按键 ASCII 值
        '''
        
        self.__keyboard.KeyPress(keyName, keyValue)
    
    def KeyCombination(self, keyNameList: list = None, keyValueList: list = None, clickWaitTime: int = 10):
        '''
        键盘组合按键。组合按键执行顺序为列表索引顺序
        :param keyNameList  : list. 元素数据类型为 str. 非必填但 keyNameList/keyValueList 必填一个。键盘按键值列表
        :param keyValueList : list. 元素数据类型为 int. 非必填但 keyNameList/keyValueList 必填一个。键盘按键 ASCII 值列表
        :param clickWaitTime: int. 按键执行间隔时间
        '''
        
        self.__keyboard.KeyCombination(keyNameList, keyValueList, clickWaitTime)
    
class Screenshot:
    def __init__(self):
        '''
        屏幕截图
        '''
        self.__screenshot = webBrowser.Screenshot()

    def AnySize(self, startX: int, startY: int, endX: int, endY: int):
        '''
        任意尺寸屏幕截图
        :param startX: int. 截图起始点 x 坐标
        :param startY: int. 截图起始点 y 坐标
        :param endX  : int. 截图终止点 x 坐标
        :param endY  : int. 截图终止点 y 坐标
        '''
        return self.__screenshot.AnySize(startX, startY, endX, endY)

class Clipboard:
    def __init__(self):
        '''
        剪切板控制
        '''
        self.__clipboard = webBrowser.Clipboards()
    
    def Set(self, data: str):
        '''
        设置剪切板内容
        :param data: str. 需要存入剪切板的文本数据
        '''
        return self.__clipboard.Set(data)
    
    def Get(self):
        '''
        获取剪切板内容
        :return 当前剪切板的文本数据
        '''
        return self.__clipboard.Get()


'''
单例模式

使用方法：使用@Singleton类装饰器
@Singleton
class MyClass:
   ...
'''

class Singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}
    def __call__(self, *args):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls(*args)
        return self._instance[self._cls]
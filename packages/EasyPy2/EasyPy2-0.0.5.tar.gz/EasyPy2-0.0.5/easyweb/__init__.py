#oding = utf-8
# -*- coding:utf-8 -*-
def about(self):
    print("The module by Yubadboy.Let us make a easy web?Write a email to me.")
import flask, json
from flask import request
import subprocess
class EasyWeb():
    php_class=None
    def __init__(self, name):
        self.web = flask.Flask(name)
    def service_init(self):
        self.service=self.web.route
    def getvalue(self,key):
        return request.values.get(key)
    def run(self,host:str="0.0.0.0",port:int=18888,debug:bool=False):
        self.web.run(debug=debug,port = port,host=host)
    def php_return(self,filepath): #在返回数据时使用
        return subprocess.getoutput(self.php_class.php_path.strip()+" "+filepath)

class php():
    php_path=str()
    def __init__(self):
        pass
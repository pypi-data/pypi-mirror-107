import json

class HSResult:
    # 0 表示 正常状态，-1 表示非正常状态
    status = None
    #消息内容
    message = ""
    #对象体
    data=None

    @staticmethod
    def saySuccess(message):
        result = HSResult()
        result.status = 0
        result.message = message
        return result

    @staticmethod
    def sayFail(message):
        result = HSResult()
        result.status = -1
        result.message = message
        return result

    #转换成json字符串
    def toJSON(self):
        return json.dumps(self,ensure_ascii=False,default=lambda o: o.__dict__, sort_keys=True, indent=4)

    #携带数据
    def withData(self,data):
        self.data = data
        return self

# 消息答应分隔符
def line(number = None,message = None):
    if number == None:
        number = 0
    print("\n\n<%s> ----------------------"
          "---------------------------"
          "---------------------------"
          "---------------------------"
          "------------"%(number))
    if message != None:
        print('    ' + message)
        print("    ----------------" )

# 各种类型都转换成字符串
def toString(obj = None):
    if(obj == None):
        return ""
    if isinstance(obj,int):
        return str(obj)
    if isinstance(obj,float):
        return str(obj)
    if isinstance(obj,bool):
        return str(bool)
    if isinstance(obj,str):
        return str
    raise Exception("未知类型")

# 将对象转换成json
def toJSON(obj):
    return json.dumps(obj,ensure_ascii=False,default=lambda o: o.__dict__, sort_keys=True, indent=4)

# 做方法测试
if __name__ == '__main__':
    print(toJSON({"a":1,"b":2}))
    print(toJSON({
        "a":1,
        "b":2,
        "c":{
            "a1":1,
            "b1":2
        }
    }))

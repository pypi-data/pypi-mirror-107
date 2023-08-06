import base64

def to(img):    #图片转换base64函数
    with open(img,"rb") as f:#转为二进制格式
        base64_data = base64.b64encode(f.read())#使用base64进行加密
        return str(base64_data,'utf-8')
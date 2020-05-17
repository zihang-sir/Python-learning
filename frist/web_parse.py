import urllib.request
import requests
url = "https://www.bilibili.com/"
'''伪装浏览器对抗网站反爬，但使用headers爬取网页内容不全'''
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
}
'''def use_urllib(url):
    req=urllib.request.Request(url, headers=headers)
    response=urllib.request.urlopen(req)
    data=response.read().decode()
    #print(data)'''

def use_requests(url):
    response = requests.get(url, headers=headers)
    data = response.text
    print(response)
    # print(data)
    # 将爬取内容保存到本地
    file_path = "D:/爬虫练习/bilibili首页.html"  # 注意文件路径用/分隔

    '''Python对with的处理基本思想是with所求值的对象必须有一个__enter__()方法，
    一个__exit__()方法。紧跟with后面的语句被求值后，返回对象的__enter__()方法被调用，
    这个方法的返回值将被赋值给as后面的变量。
    当with后面的代码块全部被执行完之后，将调用前面返回对象的__exit__()方法。'''
    with open(file_path,"w",encoding="utf-8") as f:
        f.write(data)

if __name__ == '__main__':
    # use_urllib(url)
    use_requests(url)


# 注意文件名不能命名为selenium否则导致Python会先导入这个文件，出现selenium不是一个包的错误
from selenium import webdriver
url = "https://www.bilibili.com/"

driver = webdriver.Chrome()
driver.get(url)
data = driver.page_source
file_path = "D:/爬虫练习/bilibili_selenium.html"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(data)

driver.close()

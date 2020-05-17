# https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start=980&type=T
# 导入quote给汉字编码
import urllib.request
import requests
from bs4 import BeautifulSoup
import csv
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
}
# 使用列表存储网页标签，并依次为其编ASCII码
'''key_list = ["小说", "散文", "诗歌"]
for i in key_list:
    key_ASCII = urllib.request.quote(i)
    print(key_ASCII)'''
# 解析豆瓣读书小说部分
key = "小说"
key_ASCII = urllib.request.quote(key)

# 定义一个存储书籍标签的列表
book_name_list = []
author_list = []
time_list = []
price_list = []
score_list = []
person_list = []
book_list = []  # 所有内容存到一起
# 爬取3页内容
for i in range(0, 3):
    url = "https://book.douban.com/tag/"+key_ASCII+"?start="+str(i*20)+"&type=T"
    response = requests.get(url, headers=headers)
    data = response.text
    # 网页保存到本地
    # file_path = "D:/爬虫练习/豆瓣读书/douban第"+str(i+1)+"页.html"
    # with open(file_path, "w", encoding="utf-8") as f:
    #     f.write(data)
    soup = BeautifulSoup(data, "html.parser")
    for j in range(1, 21):
        # 使用选择器在浏览器中检查，copy检查器中内容，获得需要的信息
        # select方法获得的是一个列表
        book_name = soup.select("#subject_list > ul > li:nth-child("+str(j)+") > div.info > h2 > a")
        author_time_prise = soup.select("#subject_list > ul > li:nth-child("+str(j)+") > div.info > div.pub")
        score = soup.select("#subject_list > ul > li:nth-child("+str(j)+") > div.info > div.star.clearfix > span.rating_nums")
        person = soup.select("#subject_list > ul > li:nth-child("+str(j)+") > div.info > div.star.clearfix > span.pl")
        # 取出列表中第一个元素
        # book_name = book_name[0]
        # 第二种方法，用for循环获取列表中每个元素，当列表为空时，for循环直接跳过，可解决每页书目不一致的情况
        for book_name in book_name:
            book_name_list.append(book_name.get_text().replace("\n", "").replace(" ", ""))  # 获取爬到的文本，并去掉换行与空格
        for author_time_prise in author_time_prise:
            author_time_prise = author_time_prise.get_text().replace("\n", "").replace(" ", "").replace("元", "")
            author_time_prise_list = author_time_prise.split("/")
            if len(author_time_prise_list) >= 3:
                author_list.append(author_time_prise_list[0])
                time_list.append(author_time_prise_list[-2])
                price_list.append(author_time_prise_list[-1])
            else:
                author_list.append(author_time_prise_list[0])
                time_list.append("null")
                price_list.append("null")
        for score in score:
            score_list.append(score.get_text().replace("\n", "").replace(" ", ""))
        for person in person:
            person_list.append(person.get_text().replace("\n", "").replace(" ", "").replace("(", "").replace("人评价)", ""))

# for i in range(len(book_name_list)):
#     book_list.append(
#         {
#             "书名": book_name_list[i],  # 使用字典存储书籍标签
#             "作者": author_list[i],
#             "出版时间": time_list[i],
#             "价格": price_list[i],
#             "评分": score_list[i],
#             "评价人数": person_list[i]
#         }
#     )
# print(book_list)
file_path = "D:/爬虫练习/豆瓣读书/豆瓣小说.csv"
with open(file_path, "w", newline="", encoding="utf-8") as f:
    fieldnames = ["书名", "作者", "出版时间", "价格（元）", "评分", "评价人数"]
    f_csv = csv.DictWriter(f, fieldnames)  # 名称必须与DictWriter类初始化函数中形参相同
    f_csv.writeheader()
    for i in range(len(book_name_list)):
        f_csv.writerow(
            {
                "书名": book_name_list[i],  # 使用字典存储书籍标签
                "作者": author_list[i],
                "出版时间": time_list[i],
                "价格（元）": price_list[i],
                "评分": score_list[i],
                "评价人数": person_list[i]
            }
        )
import requests
import json
from bs4 import BeautifulSoup
import csv
# 谷歌浏览器检查-Network-XHR/JS，获取存储网页信息的json文件

class MovieInformation():
    # headers是MovieInformation()的私有成员
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }
    # 爬取电影链接
    def getMovieUrl(self):
        movie_url_list = []
        # 爬取1页内容
        for i in range(0, 20, 20):
            url = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E5%8D%8E%E8%AF%AD&sort=recommend&page_limit=20&page_start="+str(i)
            response = requests.get(url, headers=self.headers)  # self类似this
            data = response.text
            # 将json文件转化为列表
            data2 = json.loads(data)
            movie_list = data2["subjects"]
            # 获取json文件中的电影网址
            for j in movie_list:
                movie_url = j['url']
                movie_url_list.append(movie_url)
        return movie_url_list
    # 爬取电影详细信息
    def catchMovieInformation(self):
        movie_name_list = []
        director_list = []
        actor_list = []
        year_list = []
        score_list = []
        people_list = []
        for movie_url in self.getMovieUrl():
            response = requests.get(movie_url, headers=self.headers)  # self类似this
            data = response.text
            soup = BeautifulSoup(data, "html.parser")
            # 电影名,网页检查，选择内容右键，copy->copy selector
            movie_name = soup.select("#content > h1 > span:nth-child(1)")
            movie_name = movie_name[0]  # 列表中只有一个元素
            movie_name = movie_name.get_text().replace("\n", "").replace(" ", "")
            movie_name_list.append(movie_name)
            # 导演
            director = soup.select("#info > span:nth-child(1) > span.attrs > a")
            director = director[0]  # 列表中只有一个元素
            director = director.get_text().replace("\n", "").replace(" ", "")
            director_list.append(director)
            # 主演
            actor = soup.select("#info > span.actor > span.attrs")
            actor = actor[0]
            actor = actor.get_text().replace("\n", "").replace(" ", "")
            actors = actor.split("/")
            if len(actors) >= 3:
                actor_list.append({
                    "主演1": actors[0],
                    "主演2": actors[1],
                    "主演3": actors[2],
                })
            elif len(actors) == 2:
                actor_list.append({
                    "主演1": actors[0],
                    "主演2": actors[1],
                })
            else:
                actor_list.append({
                    "主演1": actors[0],
                })
            # 上映时间
            year = soup.select("#content > h1 > span.year")
            year = year[0]  # 列表中只有一个元素
            year = year.get_text().replace("\n", "").replace(" ", "").replace("(", "").replace(")", "")
            year_list.append(year)
            # 评分数
            score = soup.select("#interest_sectl > div.rating_wrap.clearbox > div.rating_self.clearfix > strong")
            score = score[0]  # 列表中只有一个元素
            score = score.get_text().replace("\n", "").replace(" ", "")
            score_list.append(score)
            # 评价人数
            people = soup.select("#interest_sectl > div.rating_wrap.clearbox > div.rating_self.clearfix > div > div.rating_sum > a")
            people = people[0]  # 列表中只有一个元素
            people = people.get_text().replace("\n", "").replace(" ", "")
            people_list.append(people)
        return movie_name_list,director_list,actor_list,year_list,score_list,people_list
    # 类的实例化,在主函数中使用类时首先调用init函数
    def __init__(self):
        file_path = "D:/爬虫练习/豆瓣读书/豆瓣电影.csv"
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["电影名", "导演", "主演", "上映年份", "评分", "评价人数"]
            f_csv = csv.DictWriter(f, fieldnames)
            f_csv.writeheader()
            for i in range(len(self.catchMovieInformation()[0])):
                f_csv.writerow({
                    "电影名": self.catchMovieInformation()[0][i],  # 使用字典存储书籍标签
                    "导演": self.catchMovieInformation()[1][i],
                    "主演": self.catchMovieInformation()[2][i].values(),
                    "上映年份": self.catchMovieInformation()[3][i],
                    "评分": self.catchMovieInformation()[4][i],
                    "评价人数": self.catchMovieInformation()[5][i]
                })


if __name__ == '__main__':
    MovieInformation()


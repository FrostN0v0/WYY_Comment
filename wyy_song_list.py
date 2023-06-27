from urllib import request
from bs4 import BeautifulSoup
import re


class Music(object):
    def __init__(self, baseurl):
        head = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
            }
        self.baseurl = baseurl  # 设置请求链接
        self.headers = head  # 设置请求头

    def main(self):
        html = self.askurl()    # 调用askurl函数获取网页内容
        bs4 = self.analysis(html)   # 调用analysis函数对网页内容进行分析
        name1 = self.matching(bs4)  # 调用matching函数对分析结果进行匹配
        return name1

    def askurl(self):
        req = request.Request(url=self.baseurl, headers=self.headers)
        response = request.urlopen(req)  # 发送请求并获取响应
        html = response.read().decode("utf-8")  # 读取响应内容并解码
        return html

    def analysis(self, html):
        soup = BeautifulSoup(html, "html.parser")   # 使用BeautifulSoup解析HTML
        bs4 = soup.find_all("textarea")  # 查找所有textarea标签
        bs4 = str(bs4)  # 将结果转换为字符串
        return bs4

    def matching(self, bs4):
        rule0 = re.compile(r'"name":"(.*?)","tns":[],"alias":[]')   # 定义匹配规则0
        name0 = re.findall(rule0, bs4)  # 使用正则表达式进行匹配
        str = ""
        for i in name0:
            str  = str + "," + i    # 将匹配结果拼接为字符串
        str = str.replace("\xa0", " ")  # 替换特殊字符
        rule1 = re.compile(r'jpg,(.*?),(.*?)","id":(\d*)')  # 定义匹配规则1
        name1 = re.findall(rule1, str)  # 使用正则表达式进行匹配
        return name1  # 返回榜单歌曲对应的歌手、曲名、歌曲ID信息



if __name__ == "__main__":
    baseurl = "https://music.163.com/discover/toplist"  # 要爬取的热歌榜链接
    demo0 = Music(baseurl)
    demo0.main()

import csv
import os
import datetime
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from wyy_song_list import Music


class WYYmusic:  # 音乐
    # 初始化类
    def __init__(self, music_id):
        opt = Options()
        opt.add_argument('--headless')  # 设置无头模式启动
        chromedriver = "F:\python\chromedriver"  # chromedriver本地路径
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(chromedriver, options=opt)   # 启动ChromeDriver
        self.music_id = music_id
        self.driver.get(f'https://music.163.com/#/song?id={music_id}')  # 根据获取的歌曲ID打开评论页链接
        self.driver.implicitly_wait(3)  # 隐式等待3秒
        self.driver.switch_to.frame(self.driver.find_element(By.ID, 'g_iframe'))  # 切换到iframe框架中

    # 操作
    def operate(self):
        # 歌评论
        err = 0
        dict_id = 1
        for self.i in range(50):    # 循环50次翻页获取数据
            self.SongReview = []    # 初始化歌曲评论列表
            divlist = self.driver.find_elements(By.XPATH, '//*[@class="itm"]/div[2]')   # 查找评论的div元素列表
            for item in divlist:
                # 评论
                try:
                    commentdict = {}
                    comment = item.find_element(By.XPATH, './/div[@class="cnt f-brk"]').text    # 获取评论内容
                    time = item.find_element(By.XPATH, './/div[@class="time s-fc4"]').text  # 获取评论时间
                    name = comment.split("：")   # 按照冒号拆分评论内容，分为用户名和评论内容
                    commentdict['_id'] = dict_id    # 定义数据库ID
                    commentdict['name'] = name[0]
                    commentdict['comment'] = name[1]
                    # 利用正则匹配，统一时间格式
                    if time == '刚刚':
                        time = datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M")
                    if re.match('\d+分钟前', time):
                        atime = time.split('分钟前')
                        btime = datetime.datetime.now() - datetime.timedelta(minutes=atime[0])
                        time = btime.strftime("%Y年%m月%d日 %H:%M")
                    if re.match('\d+:\d+', time):
                        time = datetime.datetime.now().strftime("%Y年%m月%d日") + ' ' + time
                    if re.match('昨天\d+:\d+', time):
                        btime = datetime.datetime.now() - datetime.timedelta(days=1)
                        time = btime.strftime("%Y年%m月%d日") + ' ' + time.split('昨天')[1]
                    if re.match('\d月\d+日 \d+:\d+', time):
                        time = datetime.datetime.now().strftime("%Y年") + time.split(' ')[0] + ' ' + time.split(' ')[1]
                    else:
                        time = time
                    commentdict['time'] = time  # 定义数据库ID
                    dict_id += 1
                    self.SongReview.append(commentdict)     # 将评论数据添加到歌曲评论列表中
                except Exception:
                    err += 1
            self.save()     # 调用保存方法保存评论数据
            # 定位下一页按钮，通过动作链点击下一页按键
            button_tag = self.driver.find_element(By.XPATH, '//*[@class="m-cmmt"]/div[3]/div/a[11]')
            action = ActionChains(self.driver)
            action.move_to_element(button_tag)
            action.click()
            action.perform()
        self.driver.quit()  # 关闭ChromeDriver

    def save(self):
        if self.i == 0:  # 判断文件打开方式
            self.mod = 'w'
        else:
            self.mod = "a"
        headers = ['_id', 'name', 'comment', 'time']
        # 根据歌曲ID创建并写入csv文件保存
        with open(f'./raw_data/{self.music_id}.csv', self.mod, encoding='utf-8-sig', newline='') as f:
            writers = csv.DictWriter(f, headers)    # 创建CSV写入器
            if self.i == 0:
                writers.writeheader()   # 写入CSV头部
            writers.writerows(self.SongReview)  # 写入歌曲评论信息


if __name__ == "__main__":
    baseurl = "https://music.163.com/discover/toplist"  # 要爬取的热歌榜链接
    demo0 = Music(baseurl)
    cm_url = demo0.main()
    reptile = WYYmusic(cm_url)
    reptile.operate()

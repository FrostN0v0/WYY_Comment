from db_handle import write_data
from wyy_song_list import Music
from wy_selenium import WYYmusic
import datetime
from cloud import generate_wrod_clound


baseurl = "https://music.163.com/discover/toplist"  # 榜单链接
wyy_comment = datetime.datetime.now().strftime("%Y-%m-%d-") + 'toplist'  # 定义数据库名称
demo0 = Music(baseurl)  # 传入需抓取的网易云榜单链接
cm_url = demo0.main()   # 获取榜单中音乐的音乐ID
for i in range(len(cm_url)+1):    # 循环100次以抓取榜单中所有歌曲的数据
    reptile = WYYmusic(cm_url[i][2])    # 传入音乐ID
    reptile.operate()   # 开始爬取评论数据
    docuname = f'{i+1}_' + cm_url[i][1]     # 以歌曲排名+歌曲名的格式定义数据库中表单名称
    write_data(docuname, cm_url[i][2], wyy_comment)      # 写入数据库
    print(f'《{cm_url[i][1]}》-{cm_url[i][0]}，前50页评论爬取成功')
    generate_wrod_clound(wyy_comment, docuname, cm_url[i][1])   # 为每首歌生成词云

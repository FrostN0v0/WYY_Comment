import pymongo
from wordcloud import WordCloud


def generate_wrod_clound(wyy_comment, docu_name, music_name):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[wyy_comment]  # 新建数据库
    mycol = mydb[docu_name]  # 定义表单名称
    datas = mycol.find()
    comments = ''
    for data in datas:
        comments += data.get('comment')
    # 生成对象
    wc = WordCloud(font_path="MSYH.TTF", width=800, height=600, mode="RGBA", background_color=None).generate(comments)

    # 保存到文件
    wc.to_file(f"./comment_cloud/{music_name}.png")


if __name__ == "__main__":
    generate_wrod_clound('2023-06-25-toplist', '1_好运来', '1_好运来')

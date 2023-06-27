import pymongo
import csv
import datetime



def write_data(docu_name, music_id):
    wyy_comment = datetime.datetime.now().strftime("%Y-%m-%d-") + 'toplist'  # 定义数据库名称
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[wyy_comment]    # 新建数据库
    mycol = mydb[docu_name]  # 定义表单名称
    # 根据歌曲ID读取对应csv文件
    with open(f'./raw_data/{music_id}.csv', encoding="utf-8-sig", mode="r") as f:
        reader = csv.DictReader(f)  # 以字典格式读取数据
        raw_data = []
        # 以列表嵌套字典的方式写入数据
        for row in reader:
            raw_data.append(row)
        mycol.insert_many(raw_data)  # 将数据写入MongoDB数据库

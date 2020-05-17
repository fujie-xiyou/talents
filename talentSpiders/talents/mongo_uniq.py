import pymongo
from pprint import pprint
from talents.settings import MONGO_DB_URI, MONGO_DB_NAME

client = pymongo.MongoClient(MONGO_DB_URI)
db = client[MONGO_DB_NAME]
talent_col = db["talent"]
if __name__ == '__main__':
    pipeline = [
        {
            '$group': {
                '_id': {
                    'name': "$name",
                    'download_num': "$download_num",
                    'orgn': "$orgn",
                    'article_num': "$article_num"
                },
                'count': {
                    '$sum': 1
                },
                'ids': {
                    "$addToSet": "$_id"
                }
            }
        },
        {
            '$match': {
                'count': {
                    '$gt': 1
                }
            }
        }
    ]
    ts = list(talent_col.aggregate(pipeline))
    print("有 {} 个信息有重复".format(len(ts)))
    input("要列出吗？")
    del_list = []
    for t in ts:
        t['ids'].pop()
        del_list.extend(t['ids'])
    del_data = talent_col.find({"_id": {"$in": del_list}})
    pprint(list(del_data))
    print("以上 {} 条信息将被删除".format(len(del_list)))
    y = input("确认删除？(y/n)")
    if y == 'y':
        talent_col.delete_many({"_id": {"$in": del_list}})
        print("删除成功")
    else:
        print("放弃删除")

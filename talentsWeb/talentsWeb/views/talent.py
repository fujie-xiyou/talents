import pymongo
from talentsWeb.utils.TalentDecorator import request_decorator, login_decorator, dump_form_data
from talentsWeb.utils.TalentExceptions import FormException
from talentsWeb.settings import db

talent_col = db["talent"]


@request_decorator
@login_decorator
def fetch_by_cate(request, category=None):
    """
    :return: 返回某个类别下的前5个人
    """
    query = {}
    if category:
        query = {"domas": category}
    talents = list(talent_col.find(query, {"_id": 0}).limit(5))
    return talents


@request_decorator
@login_decorator
def search(request, category=None):
    search_type = int(request.GET.get("type"))
    value = request.GET.get("value")
    page = int(request.GET.get("page"))
    count = int(request.GET.get("count"))
    query = {}
    if category:
        query["domas"] = category
    key = "name" if search_type == 1 else "orgn"
    query[key] = {"$regex": ".*{}.*".format(value)}
    talents = list(talent_col.find(query, {"_id": 0}).limit(count).skip((page - 1) * count))
    total = talent_col.find(query).count()
    result = {
        "total": total,
        "page": page,
        "count": count,
        "talents": talents
    }
    return result


@request_decorator
# @login_decorator
def group_by_orgn(request):
    """
    :return: 返回按所在单位分组后人才数量前10的单位名和人才数
    """
    group = {"$group": {"_id": "$orgn", "count": {"$sum": 1}}}
    sort = {"$sort": {"count": -1}}
    limit = {"$limit": 10}
    project = {"$project": {"_id": False, "orgn": "$_id", "count": "$count"}}
    data = list(talent_col.aggregate([group, sort, limit, project]))
    scale = [{"dataKey": 'count'}]
    result = {
        "data": data,
        "scale": scale
    }
    return result


@request_decorator
# @login_decorator
def group_by_doma(request):
    """
    :return: 返回按行业分组后人才数量前10和行业名和人才数
    """
    unwind = {"$unwind": "$domas"}
    group = {"$group": {"_id": "$domas", "count": {"$sum": 1}}}
    sort = {"$sort": {"count": -1}}
    limit = {"$limit": 10}
    project = {"$project": {"_id": False, "doma": "$_id", "count": "$count"}}
    data = list(talent_col.aggregate([unwind, group, sort, limit, project]))
    scale = [{"dataKey": 'count'}]
    position = "doma*count"

    result = {
        "data": data,
        "scale": scale,
        "position": position
    }
    return result


@request_decorator
# @login_decorator
def top10(request, sort_field):
    if sort_field not in ["article_num", "download_num"]:
        raise FormException("参数错误")
    data = list(
        talent_col.find({}, {"_id": 0, "name": 1, sort_field: 1, }).sort(sort_field, pymongo.DESCENDING).limit(10)
    )
    scale = [{"dataKey": 'download_num'}]
    position = "name*{}".format(sort_field)
    result = {
        "data": data,
        "scale": scale,
        "position": position
    }
    return result


@request_decorator
# @login_decorator
def download_with_article(request):
    step = 100
    pipeline = [
        {
            "$group": {
                "_id": {
                    "$subtract": ["$article_num", {"$mod": ["$article_num", step]}]
                },
                "download_num": {"$avg": "$download_num"}
            }
        },
        {
            "$sort": {"_id": 1}
        },
        {
            "$project": {
                "_id": False,
                "article_num": "$_id",
                "download_num": "$download_num"
            }
        }
    ]
    data = list(talent_col.aggregate(pipeline))
    for t in data:
        t['article_num'] = "{}-{}篇".format(t['article_num'], t['article_num'] + step)
        t['download_num'] = int(t['download_num'])
    result = {
        "data": data,
        "position": "article_num*download_num"
    }
    return result


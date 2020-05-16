from talentsWeb.utils.FPDecorator import request_decorator, login_decorator, dump_form_data
from talentsWeb.utils.FPExceptions import FormException
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
    unwind ={"$unwind": "$domas"}
    group = {"$group": {"_id": "$domas", "count": {"$sum": 1}}}
    sort = {"$sort": {"count": -1}}
    limit = {"$limit": 10}
    project = {"$project": {"_id": False, "doma": "$_id", "count": "$count"}}
    data = list(talent_col.aggregate([unwind, group, sort, limit, project]))
    scale = [{"dataKey": 'count'}]
    result = {
        "data": data,
        "scale": scale
    }
    return result

# 用来实现自增键
from talentsWeb.models import AI
from mongoengine import DoesNotExist


def getNextSequence(name):
    try:
        ai = AI.objects.filter(_id=name).get()
        seq = ai.seq + 1
        ai.seq = seq

    except DoesNotExist:
        AI(_id=name, seq=1).save()
        seq = 1
    return seq

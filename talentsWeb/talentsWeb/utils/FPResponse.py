import json
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder


class FPResponse:
    @classmethod
    def success(cls, data):
        return HttpResponse(json.dumps({"succeed": True, "data": data}, sort_keys=True, cls=DjangoJSONEncoder))

    @classmethod
    def failure(cls, message=None):
        return HttpResponse(json.dumps({"succeed": False, "message": message}, sort_keys=True, cls=DjangoJSONEncoder))
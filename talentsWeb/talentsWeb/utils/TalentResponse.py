import json
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder


class TalentResponse:
    @classmethod
    def success(cls, data):
        return HttpResponse(json.dumps({"succeed": True, "data": data}, sort_keys=True, cls=DjangoJSONEncoder),
                            content_type="application/json")

    @classmethod
    def failure(cls, message=None):
        return HttpResponse(json.dumps({"succeed": False, "message": message}, sort_keys=True, cls=DjangoJSONEncoder),
                            content_type="application/json")

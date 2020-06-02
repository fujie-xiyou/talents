# 测试ip被封
import requests
for i in range(100):
    response = requests.get("http://navi.cnki.net/knavi/JournalDetail/GetJournalYearList?pcode=CJFD&pykm=SWJT&pIdx=0")
    print("%s  %s" % (response.status_code, response.content))
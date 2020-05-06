import scrapy
import urllib

from talents.items import TalentsItem
from talents.utils import prerr


class Talent(scrapy.spiders.Spider):
    name = "talent"
    allowed_domains = ["cnki.net"]
    start_urls = [
        "http://cajn.cnki.net/cajn/",
    ]

    """
    从首页爬取学科名称，然后拼接成获取期刊列表的链接
    """

    def parse(self, response):
        xuekes = response.xpath("//ul[@id='cajnJournalUl']/li")
        for xueke in xuekes:
            zjcode = xueke.xpath("@code").extract()[0]
            zjname = xueke.xpath("@zjname").extract()[0]
            print("--解析出学科名：%s" % zjname)
            url = 'http://cajn.cnki.net/cajn/home/SearchCAJNMore?idx=0&journalType=CAJNJournal&zjCode=%s&zjName=%s' \
                  '&handler=&pageIdx=0&pSize=500' % (urllib.parse.quote(zjcode), urllib.parse.quote(zjname))
            yield scrapy.Request(
                url,
                callback=self.parse_all_xueke,
                headers={'X-Requested-With': 'XMLHttpRequest'},
                meta={"xueke": zjname}
            )

    """
    获取每个学科下的期刊对应的pcode(不知道代表什么，但是好像都一样)和pykm(期刊标识)
    """

    def parse_all_xueke(self, response):
        pcode = "CJFD"  # 不知道这个代表什么  但是看起来每个期刊都有这个参数 而且都一样, 先放在这里吧
        pys = response.xpath("//ul/li/a")
        if not pys:
            prerr("解析期刊列表失败，学科名： %s  url: %s" % (response.meta['xueke'], response.url))
            return
        for py in pys:
            pykm = py.xpath("@href").re(r'pykm=(.*)$')[0]
            py_name = py.xpath("span/@title").extract()[0]
            print("----获取到期刊名：%s , 学科：%s" % (py_name, response.meta['xueke']))
            url = 'http://navi.cnki.net/knavi/JournalDetail/GetJournalYearList?pcode=%s&pykm=%s&pIdx=0' % (pcode, pykm)
            yield scrapy.Request(
                url,
                callback=self.parse_time_type,
                meta={'pcode': pcode, 'pykm': pykm, 'xueke': response.meta['xueke']}
            )

    """
    解析期刊的时间分类 例如 2019年02期
    """

    def parse_time_type(self, response):
        year_list = response.xpath("//dd/a/@id").re(r'yq(\d{4})(.*)$')
        if not year_list:
            prerr("------yearList解析失败，resp: %s url: %s" % (response.body, response.url))
            return
        pcode = response.meta['pcode']
        pykm = response.meta['pykm']
        for i in range(0, len(year_list), 2):
            year = year_list[i]
            issue = year_list[i + 1]
            url = 'http://navi.cnki.net/knavi/JournalDetail/GetArticleList?' \
                  'year=%s&issue=%s&pykm=%s&pageIdx=0&pcode=%s' % (year, issue, pykm, pcode)
            print("------获取到文章列表, 学科：%s , 期刊：%s , 年份：%s , No.%s" % \
                  (response.meta['xueke'], pykm, year, issue)
                  )
            yield scrapy.Request(
                url,
                callback=self.parse_article_list,
                meta={"xueke": response.meta['xueke'],
                      "pykm": pykm,
                      "year": year,
                      "issue": issue,
                      }
            )

    def parse_article_list(self, response):
        arts = response.xpath('//dd/span/a')
        if not arts:
            prerr("--------文章列表解析失败，url: %s" % response.url)
            return
        for art in arts:
            title = art.xpath("text()").extract()[0].strip()
            url = art.xpath("@href").extract()[0]
            print("--------获取到文章标题：%s url: %s" % (title, url))
        args = response.xpath('//dd/span/a/@href').re(r'dbCode=(.*)&.*filename=(.*)&.*tableName=(.*)&.*')
        for i in range(0, len(args), 3):
            dbcode = args[i]
            filename = args[i + 1]
            dbname = args[i + 2]
            print("--------解析到文章filename参数：%s" % filename)
            url = "http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=%s&filename=%s&dbname=%s" % \
                  (dbcode, filename, dbname)
            yield scrapy.Request(url, callback=self.parse_article)

    def parse_article(self, response):
        author_list = response.xpath("//div[@class='author']/span/a/@onclick").re(r"\('(.*)','(.*)','(.*)'\)")
        if not author_list:
            prerr("----------解析作者列表失败，url: %s" % response.url)
            return
        for i in range(0, len(author_list), 3):
            sfield = author_list[i]
            skey = urllib.parse.quote(author_list[i + 1])
            code = author_list[i + 2]
            print("----------解析到作者名字：%s" % author_list[i + 1])
            url = "http://kns.cnki.net/kcms/detail/knetsearch.aspx?sfield=%s&skey=%s&code=%s" % \
                  (sfield, skey, code)
            yield scrapy.Request(url, callback=self.parse_author, meta={'code': code})

    def parse_author(self, response):
        code = response.meta['code']
        url = response.url
        name = response.xpath("//h2[@class='name']/text()").extract()
        if not name:
            prerr("----------解析作者信息失败，url: %s" % response.url)
            return
        if len(name) > 0:
            name = name.pop()
            print("----------获取到人才信息，姓名：%s" % name)
        else:
            prerr("----------没这个人： %s" % url)
            return
        # 所属单位
        orgn = response.xpath("//p[@class='orgn']//a/text()").extract()
        if len(orgn):
            orgn = orgn.pop()
        else:
            prerr("没这个组织： %s" % url)
            return
        # 行业/知识领域
        domas = response.xpath("//p[@class='doma'][1]/text()").re(r'(.*);$').pop().split(';')
        titleSide = response.xpath("//p[@class='num']/span/text()").re(r'(\d+)$')
        article_num = int(titleSide[0])
        download_num = int(titleSide[1])
        talent = TalentsItem(code=code, name=name, orgn=orgn, domas=domas, article_num=article_num,
                             download_num=download_num, url=url)

        return talent

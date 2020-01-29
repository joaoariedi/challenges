import scrapy

class Report(scrapy.Item):
    occured = scrapy.Field()
    posted = scrapy.Field()
    city  = scrapy.Field()
    state = scrapy.Field()
    shape = scrapy.Field()
    duration = scrapy.Field()
    summary = scrapy.Field()

    
class OVNIsSpider(scrapy.Spider):
    name = "ovnis"

    BASE_URL = 'http://www.nuforc.org/webreports/'

    def start_requests(self):
        yield scrapy.Request('http://www.nuforc.org/webreports/ndxevent.html', callback = self.parse_links)


    def parse_links(self, response):
        links = response.xpath("//a/@href").getall()
        for link in links[1:-1]:
            absolute_url = self.BASE_URL + link
            yield scrapy.Request(absolute_url, callback=self.parse_month)

    def parse_month(self, response):
        report = Report()
        table = response.xpath("//table")
        tbody = table.xpath("tbody")
        rows = tbody.xpath("tr")
        for row in rows:
            report['occured'] = row.xpath("td[1]/font//text()").get()
            report['city'] = row.xpath("td[2]/font//text()").get()
            report['state'] = row.xpath("td[3]/font//text()").get()
            report['shape'] = row.xpath("td[4]/font//text()").get()
            report['duration'] = row.xpath("td[5]/font//text()").get()
            report['summary'] = row.xpath("td[6]/font//text()").get()
            report['posted'] = row.xpath("td[7]/font//text()").get()

            yield report
        



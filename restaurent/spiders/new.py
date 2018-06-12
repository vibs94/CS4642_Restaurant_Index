import scrapy


class RestaurantSpider(scrapy.Spider):
    name = 'cons'
    start_urls = ['https://www.theconstructor.org',]

    def parse(self, response):
        name=[]
        for a in response.css("div.post-inner::text").extract():
            a=str(a)
            print(a)


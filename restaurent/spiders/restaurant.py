import scrapy


class RestaurantSpider(scrapy.Spider):
    name = 'restaurant'

    start_urls = ['https://www.gsmarena.com/']

    def parse(self, response):
        refs=[]
        names=[]
        div=response.css("div.brandmenu-v2")
        for a in div.css("li"):
            ref = a.css("li>a::attr(href)")
            print (ref)
            refs.append(ref)
            name = a.css("li>a::attr(text)")
            names.append(name)



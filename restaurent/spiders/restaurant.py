import scrapy
import unicodedata

class RestaurantSpider(scrapy.Spider):
    name = 'restaurant'

    res_url = 'https://www.yamu.lk/place/restaurants?page={}'

    start_urls = [res_url.format(1)]

    def parse(self, response):
        restaurants = response.css('a.front-group-item')
        for restaurant in restaurants:
            yield {
                'name': self.preprocess(restaurant.css('h3.front-h3::text').extract_first()),
                'address': self.preprocess(restaurant.css('text-muted::text').extract_first()),
                'disc': self.preprocess(restaurant.css('p.front-p::text').extract_first())
            }
        p=response.url.split("=")[-1]
        if(p=="44"):
            exit()
        yield scrapy.Request(url=self.res_url.format(int(p) + 1), callback=self.parse)

    def preprocess(self,text):
        if text == None: return None
        return unicodedata \
            .normalize('NFKD', text) \
            .encode('ascii', 'ignore') \
            .replace('\n', '').replace('\t', '').strip()




import scrapy
import unicodedata
import sys

class RestaurantSpider(scrapy.Spider):
    name = 'restaurant'

    res_url = 'https://www.yamu.lk/place/restaurants?page={}'

    start_urls = [res_url.format(1)]

    def parse(self, response):
        restaurants = response.css('a.front-group-item')
        for restaurant in restaurants:
            href = restaurant.css('::attr(href)').extract_first()
            yield scrapy.Request(url=response.urljoin(href), callback=self.parse_details)
        p=response.url.split("=")[-1]
        # if(p=="44"):
        #     sys.exit()
        yield scrapy.Request(url=self.res_url.format(int(p) + 1), callback=self.parse)

    def parse_details(self, response):

        contact = self.preprocess(response.css('a.emph::text').extract_first())
        if(contact!=None):contact = contact[5:]
        openh = self.preprocess(response.css('div.time-range>span::attr(title)').extract_first())
        if(openh!=None): openh = openh.split('>')[3]
        if (openh != None): openh = openh.split('<')[0]
        info = response.css('div.place-info-box')
        lables = info.css('div.label-yamu')
        la = []
        for lable in lables:
            uni = self.preprocess(lable.css('div.inner::text').extract_first())
            la.append(uni)
        place = info.css('div.info')
        dir = place[0].css('p')
        dire =""
        if (len(dir) > 3):
            dire = self.preprocess(dir[3].css('::text').extract_first())
        moreInfo = place[1].css('p')
        cuisine = []
        if(len(moreInfo)>2):
            cuisines = moreInfo[2].css('a')
            for cui in cuisines:
                cuisine.append(self.preprocess(cui.css('::text').extract_first()))
        price = ""
        if(len(moreInfo)>4):
            price = self.preprocess(moreInfo[4].css('a::text').extract_first())
        dish = []
        if (len(moreInfo) > 6):
            dishes = moreInfo[6].css('a')
            if(dishes!=None):
                for dis in dishes:
                    dish.append(self.preprocess(dis.css('::text').extract_first()))
        rate = response.css('div.place-rating-box-item')
        rate = self.preprocess(rate[0].css('a::text').extract_first())
        if("/" not in rate):
            rate = ""
        desc = self.preprocess(response.css('p.excerpt::text').extract_first())
        if(desc==None):
            desc = ""
        if (any(c.isalpha() for c in desc))==False:
            desc = ""
        addr = self.preprocess(response.css('p.addressLine::text').extract_first())
        if(addr==None):
            addr = ""
        if(contact==None):
            contact = ""
        # yield {
        #     'name': self.preprocess(response.css('h2::text').extract_first()),
        #     'contact': contact.strip(),
        #
        # }

        yield {
            'name': self.preprocess(response.css('h2::text').extract_first()),
            'address': addr,
            'directions': dire,
            'description': desc,
            'contact': contact.strip(),
            'open': openh,
            'lables': la,
            'cuisines': cuisine,
            'priceRange': price,
            'dishes': dish,
            'rating': rate
        }

    def preprocess(self,text):
        if text == None: return None
        return unicodedata \
            .normalize('NFKD', text) \
            .encode('ascii', 'ignore') \
            .replace('\n', '').replace('\t', '').replace('\r', '').replace('\"', '').strip()




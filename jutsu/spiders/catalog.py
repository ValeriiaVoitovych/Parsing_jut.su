import scrapy

class CatalogSpider(scrapy.Spider):
    name = "catalog"
    allowed_domains = ["jut.su"]
    start_urls = ["https://jut.su/anime/"]
    page_count = 32

    def start_requests(self):
        for page in range(1, self.page_count + 1):  
            url = f'https://jut.su/anime/page-{page}/'
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for anime in response.css('.all_anime_global'):
            link = anime.css('a::attr(href)').get()
            yield response.follow(link, callback=self.parse_anime)

    def parse_anime(self, response):
        yield {
            'name': ' '.join(response.css('h1.header_video::text').get().split()[1:3]),
            'original name': response.css('div.under_video_additional b::text').get(),
            'film genre': response.css('div.under_video_additional a[href^="/anime/"]::text').getall()[0]
        }

        

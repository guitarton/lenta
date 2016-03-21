from scrapy.spiders import SitemapSpider
from lenta.items import LentaItem


class LentaSiteMapSpider(SitemapSpider):
    name = 'lenta-sitemap'
    sitemap_urls = ['http://lenta.ru/robots.txt']
    # sitemap_urls = ['http://lenta.ru/news/sitemap5.xml.gz']

    def parse(self, response):
        item = LentaItem()
        item['url'] = response.url
        item['post_body'] = response.css('div.b-topic__content').extract_first()
        return item

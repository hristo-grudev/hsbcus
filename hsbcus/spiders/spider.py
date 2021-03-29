import scrapy

from scrapy.loader import ItemLoader

from ..items import HsbcusItem
from itemloaders.processors import TakeFirst


class HsbcusSpider(scrapy.Spider):
	name = 'hsbcus'
	start_urls = ['https://www.about.us.hsbc.com/news-and-media']

	def parse(self, response):
		post_links = response.xpath('//span[@class="tabular-list__title-wrapper"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		if 'pdf' in response.url:
			return
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="page-description__summary"]//text()[normalize-space()]|(//p[not(contains(@class,"disclaimer") or contains(@class,"page-description__meta") or contains(@class,"leaving-confirmation__copy"))])[position()>1]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//p[@class="page-description__meta"]/text()').get()

		item = ItemLoader(item=HsbcusItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()

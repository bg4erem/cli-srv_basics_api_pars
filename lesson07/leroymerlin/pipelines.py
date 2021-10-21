# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from lxml import html


class LeroymerlinPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        specs_processed = {}
        specs_source = ' '.join([str(element) for element in adapter['specs']])
        dom = html.fromstring(specs_source)
        els = dom.xpath('//div[@class="def-list__group"]')
        for el in els:
                term = el.xpath('.//dt/text()')[0]
                definition = el.xpath('.//dd/text()')[0]
                specs_processed[f'{str(term)}'] = str(definition).replace('\n', '').strip()
        adapter['specs'] = specs_processed
        adapter['price'] = adapter['price'].replace(' ','')
        adapter['price'] = int(adapter['price'])
        adapter['_id'] = adapter['link']
        return item


class LeroymerlinPhotos(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'full/{item["name"]}/{image_guid}.jpg'

    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)
        return item

import scrapy, logging
from scrapy.utils.log import configure_logging 

# Items
from animals_a_to_z.items import AnimalsAToZItem

class AnimalsSpider(scrapy.Spider):
    name = "animals"
    allowed_domains = ["a-z-animals.com"]
    start_urls = ["https://a-z-animals.com/"]

    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='logs/animals.log',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )

    def parse(self, response):
        # for item in response.css('li.list-item'):
        #     url = item.css('a::attr(href)').get()
        #     print(url)
        #     yield response.follow(url, self.parse_animals)
        animals = response.css('li.list-item.col-md-4.col-sm-6 a::attr(href)')
        for anim in animals:
            yield response.follow(anim, self.parse_animals)

    def parse_animals(self, response):
        item_anim = AnimalsAToZItem()

        item_anim['name'] = response.css('h1.has-text-align-center.has-custom-size.text-white::text').get()
        item_anim['facts'] = response.css('h2[id^="h-"]::text').getall()
        # item_anim['facts'] = response.css('h2[id^="h-"]::attr(id)').getall()

        # anim_image_url = response.css('figure.wp-block-image.size-large img::attr(src)').get()
        # if anim_image_url:
        #     img_url = response.urljoin(anim_image_url)
        #     item_anim['image_urls'] = [img_url]

        yield item_anim
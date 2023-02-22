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
        animals = response.css('li.list-item.col-md-4.col-sm-6 a::attr(href)')
        for anim in animals:
            yield response.follow(anim, self.parse_animals)

    def parse_animals(self, response):
        item_anim = AnimalsAToZItem()

        item_anim['name'] = response.css('h1.has-text-align-center.has-custom-size.text-white::text').get()
        # item_anim['facts'] = response.css('h2[id^="h-"]::text').getall()

        # Pake yang ini
        facts_list = []
        h2_facts = response.css('h2[id^="h-"]')
        for h2 in h2_facts:
            fact_dict = {}
            fact_dict['fact'] = h2.css('::text').get()
            fact_dict['desc'] = h2.xpath('following-sibling::p[1]').xpath('normalize-space(string())').get() # hilanging link di paragraf
            # fact_dict['desc'] = h2.xpath('following-sibling::p[1]/text()').get()
            facts_list.append(fact_dict)

        item_anim['facts'] = facts_list

        # Desc nyatu sama judul (gabung)
        # h2_facts = response.css('h2[id^="h-"]')
        # facts_list = []
        # for h2 in h2_facts:
        #     fact = h2.css('::text').get()
        #     desc = h2.xpath('following-sibling::p[1]/text()').get()
        #     facts_list.append({fact: desc})
        # item_anim['facts'] = facts_list

        # Desc pisah sama judul
        # facts_arr = []
        # desc_arr = []
        # h2_facts = response.css('h2[id^="h-"]')
        # for h2 in h2_facts:
        #     fact = h2.css('::text').get()
        #     desc = h2.xpath('following-sibling::p[1]/text()').get()
        #     facts_arr.append(fact)
        #     desc_arr.append(desc)
        # item_anim['facts'] = facts_arr
        # item_anim['facts_desc'] = desc_arr


        # anim_image_url = response.css('figure.wp-block-image.size-large img::attr(src)').get()
        # if anim_image_url:
        #     img_url = response.urljoin(anim_image_url)
        #     item_anim['image_urls'] = [img_url]

        yield item_anim
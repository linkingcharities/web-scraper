import scrapy


class CharitySpider(scrapy.Spider):
    name = "charities"
    base_url = 'http://www.charitychoice.co.uk'
    base_search_url = base_url + '/charities/search/?q=&t=qsearch&region=london&pid='
    starting_page = 1
    start_urls = [
        base_search_url + str(starting_page),
    ]

    def parse(self, response):
        sel = scrapy.Selector(response, type="html")
        results = sel.css('.result')
        cnt = 0
        for result in results:
            # charity_summary = {
            #     'title': result.xpath('./h2/a/text()').extract(),
            #     'town-county': result.css('.town-county').xpath('./text()').extract()
            # }
            page_url = result.xpath('./h2/a/@href').extract()[0]
            charity_page_url = self.base_url + page_url
            if cnt < 2:
                cnt += 1
                print('DETAIL PAGE:', charity_page_url)
                yield scrapy.Request(charity_page_url, callback=self.parse_details)

        return

    def parse_details(self, response):
        charity_info = {}
        sel = scrapy.Selector(response, type="html")
        summary = sel.css('.charity-hgroup')

        # Get the name
        charity_info['name'] = summary.xpath('./h1/text()').extract()[0]

        # Get short description
        charity_info['short-text'] = summary.xpath('./h2/text()').extract()
        if len(charity_info['short-text']) > 0:
            charity_info['short-text'] = charity_info['short-text'][0]

        # Get ID and county
        paragraph = summary.xpath('./p/text()').extract()
        paragraph = [x.replace('\n', '') for x in paragraph]
        paragraph = [x.replace('Registered Charity Number: ', '') for x in paragraph]
        paragraph = [x.strip() for x in paragraph]

        if len(paragraph) == 2:
            charity_info['register_id'] = paragraph[0]
            charity_info['town-county'] = paragraph[1]
        else:
            charity_info['town-county'] = paragraph[0]

        # Display
        for (k, v) in charity_info.items():
            print(k, ':', v)
        print('\n\n')
        yield charity_info

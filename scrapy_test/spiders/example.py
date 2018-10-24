# -*- coding: utf-8 -*-
import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    detail = 'https://read.douban.com'
    start_urls = [
        'https://read.douban.com/kind/101?start=0&sort=hot'
    ]

    def parse(self, response):
        #文件名  一页放入一个文件 可以放入数据库之类的
        page = response.url.split("=")[1]
        page = page.split("&")[0]
        file_name = '%s-图书.txt' % page
        
        li = response.css('li.store-item')
        for li_value in li:
            with open(file_name, "a+") as f:
                f.write('title：' + li_value.css('.title a::text').extract_first())

                f.write('  author：' + li_value.css('.author-item::text').extract_first())

                if li_value.css('.price-tag .original-tag::text'):
                    f.write('  price：' + li_value.css('.price-tag .original-tag::text').extract_first())

                if li_value.css('p .meta-item .labeled-text *::text'):
                    translator = li_value.css('p .meta-item .labeled-text *::text').extract()
                    translator = ','.join(translator)
                    f.write('  translator：' + translator)

                f.write('  category：' + li_value.css('.labeled-text span::text').extract_first())

                f.write('  img：' + li_value.css('.shadow-cover img::attr(src)').extract_first())

                detail_param = li_value.css('.shadow-cover a::attr(href)').extract_first()
                detail = self.detail + detail_param
                f.write('  detail_url：' + detail)

                if li_value.css('.list-rating span.rating-average').extract_first():
                    f.write('  score：' + li_value.css('.list-rating span.rating-average::text').extract_first())

                f.write('  desc：' + li_value.css('.article-desc-brief::text').extract_first())

                f.write('\n')  # ‘\n’ 表示换行
                f.close()

        #下一页
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

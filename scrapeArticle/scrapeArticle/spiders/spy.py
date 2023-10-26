import scrapy
import os

from ..urls_reader import read_urls_from_excel
from ..items import ScrapearticleItem


class SpySpider(scrapy.Spider):
    name = "spy"
    allowed_domains = ["blackcoffer.com"]

    def start_requests(self):

        # prepare the variables for reading the urls function
        excel_file_path = '../Input.xlsx'
        url_column_name = 'URL'
        url_id_column_name = 'URL_ID'

        urls, url_ids = read_urls_from_excel(excel_file_path,url_column_name,url_id_column_name)

        for i in range(len(urls)):
            yield scrapy.Request(url=urls[i], callback=self.parse, meta={'url_id': url_ids[i]})


    def parse(self, response):

        # extracting the texts
        article_title = response.css('.td-post-title .entry-title::text').extract()
        article_text = response.css('.tagdiv-type p::text').extract()
        article_text = article_text[0].replace('\u20b9', '')   # was giving an error as the unicode stands for the rupee symbol

        # making the scraped text file name
        url_id = response.meta['url_id']
        text_file_name = f'{url_id}.txt'        

        # store the data in the text file  # w stands for write : each time it will clear the file before writing
        with open(text_file_name, 'w') as file:
            file.write(f"Title: {article_title}\n")
            file.write(f"Description: {article_text}\n")
            file.write("\n")

        # now i want to make a csv file from all the extracted text, so that i can perform data analysis on it
        items = ScrapearticleItem()    # creating an instance of the class
        items['article_title'] = article_title
        items['article_text'] = article_text
        items['url_id'] = response.meta['url_id']

        yield items






        

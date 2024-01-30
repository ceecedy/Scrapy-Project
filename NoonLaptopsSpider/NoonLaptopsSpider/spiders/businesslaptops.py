import scrapy
from NoonLaptopsSpider.items import LaptopsItem

class BusinesslaptopsSpider(scrapy.Spider):
    name = "businesslaptops"
    allowed_domains = ["noon.com"]
    page_number = 2
    start_urls = ["https://www.noon.com/business-laptops-all"]
    

    def parse(self, response):
        div_grid = response.xpath('//div[@class="sc-926ab76d-7 eCDCTP grid"]')
        
        for span in div_grid.css('span'):
            href = span.css('a::attr(href)').get()
            
            if href:
                # Trim the "/uae-en" part
                trimmed_href = href.replace('/uae-en', '')
                relative_url = 'https://noon.com' + trimmed_href
                yield response.follow(relative_url, callback=self.parse_item_information)
        
        '''
        next_page = 'https://www.noon.com/business-laptops-all/?limit=50&page=' + str(BusinesslaptopsSpider.page_number)
        if BusinesslaptopsSpider.page_number <= 100:
            yield response.follow(next_page, callback = self.parse)
            BusinesslaptopsSpider.page_number += 1
        '''
            
            
    def parse_item_information(self, response):
        laptop = LaptopsItem()
        
        laptop['brand'] = response.xpath('//div[@class="sc-fe105d6c-17 jWmzRz"]/text()').get()
        laptop['product_name'] = response.xpath('//h1[@class="sc-fe105d6c-18 hgXzCs"]/text()').get()
        
        # Model Number
        model_numbers_element = response.css('.modelNumber')
        if model_numbers_element:
            model_numbers = model_numbers_element.xpath('.//text()').getall()[2:]  # Extract from index 2 to exclude headings
            laptop['model_number'] = ','.join(model_numbers)  # Join as a comma-separated string

        # Was price 
        original_price = response.css('.priceWas')
        if original_price:
            orig_price = original_price.xpath('.//text()').getall()[:] 
            laptop['was_price'] = ''.join(orig_price) 
            
        # Now price
        price_data = response.css('.priceNow').xpath('.//text()').getall()
        if price_data:
            # Extracting AED and price from the text
            aed_currency = price_data[0].strip()
            price_value = price_data[2].strip()

            # Now price is a combination of AED and price
            laptop['now_price'] = f"{aed_currency} {price_value}"
            
        # Now price
        potential_save = response.css('.priceSaving').xpath('.//text()').getall()
        if potential_save:
            # Extracting AED and price from the text
            aed_currency = potential_save[0].strip()
            price_value = potential_save[2].strip()

            # Now price is a combination of AED and price
            laptop['saving'] = f"{aed_currency} {price_value}"
    
        '''
       # **Improved Rating Scraping:**
        rating_element = response.css('div.sc-363ddf4f-2.jdb0Po')  # Select the element directly
        if rating_element:
            rating = rating_element.xpath('./text()').get().strip()  # Extract text using XPath
            laptop['rating'] = rating

        # **Improved Stock Scraping:**
        stock_element = response.css('div.sc-363ddf4f-4.erKDow span.sc-363ddf4f-5.bBssC')  # Consider nested element
        if stock_element:
            stock = stock_element.xpath('./text()').get().strip()  # Extract text using XPath
            laptop['stock'] = stock
        '''
        
        yield laptop
        
        
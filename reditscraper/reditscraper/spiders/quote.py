import scrapy,csv
from scrapy.crawler import CrawlerProcess

class quoteSpider(scrapy.Spider):
    name = 'quote'
    allowed_domains = ['www.reddit.com/r/gameofthrones/']
    start_urls = ['http://www.reddit.com/r/gameofthrones/']
    output = "output.csv"
    handle_httpstatus_list = [404]
    def __init__(self):
        self.outfile = open("output.csv", "w", newline="")
        self.writer = csv.writer(self.outfile)
        self.writer.writerow(['title'])
        print("***" * 20, "opened")

    def closed(self, reason):
        self.outfile.close()
        print("***" * 20, "closed")
        
    def parse(self, response):
        # Extracting the content using css selectors
        self.logger.info("got response %d for %r" % (response.status, response.url))
        if response.status >= 300 and response.status < 400:

            # HTTP header is ascii or latin1, redirected url will be percent-encoded utf-8
            location = to_native_str(response.headers['location'].decode('latin1'))

            # get the original request

            request = response.request
            # and the URL we got redirected to
            redirected_url = urljoin(request.url, location)

            if response.status in (301, 307) or request.method == 'HEAD':
                redirected = request.replace(url=redirected_url)
                yield redirected
            else:
                redirected = request.replace(url=redirected_url, method='GET', body='')
                redirected.headers.pop('Content-Type', None)
                redirected.headers.pop('Content-Length', None)
                yield redirected
        title = response.css('._eYtD2XCVieq6emjKBH3m::text').extract()
        votes = response.css('._1rZYMD_4xY3gRcSS3p8ODO::text').extract()
        image = response.css('img').xpath('@src').getall()         
        comm = response.css('.FHCV02u6Cp2zYL0fhQPsO::text').extract()
        # Give the extracted content row wise
        with open(self.output, "a", newline="") as f:
            writer = csv.writer(f)
            for item in zip(title, votes, image, comm):
                #create a dictionary to store the scraped info
                print("1")
                scraped_info = {
                     'title': item[0],
                     'votes': item[1],
                     'image': item[2],
                     'comm': item[3],
                 }
                yield scraped_info
                self.writer.writerow([item[0],item[1],item[2],item[3]])
            
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(quoteSpider)
    process.start()

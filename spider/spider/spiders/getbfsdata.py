import scrapy
import re

class CsvSpider(scrapy.Spider):
    name = 'bfs'
    start_urls = ['https://www.bfs.admin.ch/bfs/de/home/statistiken/kataloge-datenbanken/tabellen/_jcr_content/par/ws_catalog.dynamiclist.html?prodima=900035&institution=900004&_charset_=UTF-8&pageIndex=&publishingyearstart=&publishingyearend=2024&title=&orderNr=']

    def parse(self, response):
        for href in response.css('a.media-heading.list-link-heading::attr(href)'):
            yield response.follow(href, self.parse_detail_page)

        for href in response.css('a#NextLink::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_detail_page(self, response):
        h1_span_text = response.css('div.contentHead h1 span.h2::text').get(default='').strip()
        h1_direct_text = response.css('div.contentHead h1::text').getall()
        
        # Combine the text, inserting a colon between the span text and the direct text, then clean up whitespace
        h1_direct_text_combined = ''.join(h1_direct_text).strip()
        h1_text_combined_raw = f"{h1_span_text}: {h1_direct_text_combined}" if h1_span_text and h1_direct_text_combined else f"{h1_span_text}{h1_direct_text_combined}"
        
        # Clean up the h1_text_combined by removing excessive whitespace and ensuring a single space after the colon
        import re
        h1_text_combined = re.sub(r'\s+', ' ', h1_text_combined_raw).strip()

        # Iterate over each file link container
        for container in response.css('.col-sm-5'):
            # Check if the link is a CSV file
            if container.css('span.text-dimmed::text').re(r'\(CSV,'):
                # Extract the first href (link) within the container if it's a CSV
                bfs_href = container.css('a::attr(href)').extract_first()
                if bfs_href:
                    yield {
                        h1_text_combined: bfs_href
                    }





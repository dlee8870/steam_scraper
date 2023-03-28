import scrapy
from scrapy.crawler import CrawlerProcess


class SteamReviewsSpider(scrapy.Spider):
    name = "review_scrape"

    def start_requests(self):
        # Enter the URL of the game's page you want to scrape reviews from.
        urls = [
            'https://store.steampowered.com/app/252490/Rust/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Extract the review URLs from the game's page.
        review_urls = response.css('a.apphub_UserReviewCardContent::attr(href)').extract()
        for url in review_urls:
            yield scrapy.Request(url=response.urljoin(url), callback=self.parse_review)

        # Follow the pagination links to scrape all reviews.
        next_page_url = response.css('a.pagebtn::attr(href)').extract()[-1]
        if next_page_url:
            yield scrapy.Request(url=response.urljoin(next_page_url), callback=self.parse)

    def parse_review(self, response):
        # Extract the review details.
        yield {
            'game_title': response.css('div.apphub_AppName::text').extract_first().strip(),
            'review_title': response.css('div.title::text').extract_first().strip(),
            'review_text': response.css('div.content::text').extract_first().strip(),
            'review_date': response.css('div.date_posted::text').extract_first().strip(),
            'review_rating': response.css('div.rating::attr(title)').extract_first().strip(),
            'reviewer_username': response.css('div.user_avatar img::attr(alt)').extract_first().strip(),
            'reviewer_profile_url': response.css('div.user_avatar a::attr(href)').extract_first().strip(),
        }


process = CrawlerProcess()
process.crawl(SteamReviewsSpider)
process.start()

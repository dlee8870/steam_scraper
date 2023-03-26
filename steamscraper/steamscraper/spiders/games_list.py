import scrapy


class ReviewSpider(scrapy.Spider):
    name = 'similar_games'

    def start_requests(self):
        urls = [
            'https://steamcommunity.com/app/1172380'
        ]

        for url in urls:
            yield scrapy.Request(url, method='GET', callback=self.parse)

    def parse(self, response):
        # Load all reviews on current page.
        reviews = response.css('div.apphub_UserReviewCardContent')  # div of each response box
        for review in reviews:
            yield {
                "text": review.xpath(''.join('.//*[@class="apphub_CardTextContent"]//text()')).getall()[-1].replace(
                    '\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t', '').replace('\t\t\t', ''),
                "Recommend": review.css('div.title::text').get(),
                "date": review.css('div.date_posted::text').get(),
                'found_helpful': review.css('div.review_award_aggregated.tooltip').get()
            }

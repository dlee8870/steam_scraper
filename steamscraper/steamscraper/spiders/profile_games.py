# from scrapy import Spider
# from scrapy.spiders import Rule
#
#
# class SteamSpider(Spider):
#     name = 'products'
#     start_urls = ["http://store.steampowered.com/search/?sort_by=Released_DESC"]
#     allowed_domains = ["steampowered.com"]
#     rules = [
#         Rule(
#             LinkExtractor(
#                 allow='/app/(.+)/',
#                 restrict_css='#search_result_container'),
#             callback='parse_product'),
#         Rule(
#             LinkExtractor(
#                 allow='page=(d+)',
#                 restrict_css='.search_pagination_right'))
#     ]
#
#
# username = "steam_scraping_temp"
# password = "JANSF958^%195ma"

from newsapi import NewsApiClient
from datetime import datetime, timedelta
import os

class NewsClient(object):

    def __init__(self, keyword):
        self.keyword = keyword
        self.fetch_days = 10
        self.sources = 'bloomberg,business-insider,cnbc,fortune,nbc-news,reuters,techcrunch,the-wall-street-journal'
        self.key = os.environ['NEWS_API_KEY']

    def fetch_news_articles(self):
        try:
           news_api = NewsApiClient(api_key=self.key)
           to_date = datetime.today().strftime('%Y-%m-%d')
           from_date = (datetime.now() - timedelta(days=self.fetch_days)).strftime('%Y-%m-%d')
           all_articles = news_api.get_everything(q=self.keyword,
                                      from_param=from_date,
                                      to=to_date,
                                      sources=self.sources,
                                      language='en',
                                      sort_by='publishedAt')
           return all_articles
        except Exception as err:
            print("Something went wrong: {}".format(err))
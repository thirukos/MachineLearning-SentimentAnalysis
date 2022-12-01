import pandas as pd
import snscrape.modules.twitter as sntwit
import itertools
import matplotlib as plt

from wordcloud import WordCloud, STOPWORDS

search_terms = ['queen', 'elizabeth', 'colonialism', 'rip', 'royal family', 'death', 'irish',
                'britain', 'uk']
exclude_terms = ['-mermaid', 'minaj', 'latifah']
tweet_fields = ['date', 'content', 'lang', ]
locations = {'southasia': {'india': ['delhi', 'mumbai', 'chennai']}, 
             'ireland': {'ireland': ['dublin', 'cork', 'galway']},
             'uk': {'uk': ['london', 'glasgow', 'york', 'swansea']}}

exclude_query = ' OR -'.join(term for term in exclude_terms)


tweets = pd.DataFrame()

# Using a word cloud to select popular words in timeframe
search_query = 'since:2022-09-08 until:2022-09-10'
scraped_tweets = sntwit.TwitterSearchScraper(search_query).get_items()
wordcloud = WordCloud(stopwords = STOPWORDS, background_color="white").generate(scraped_tweets)
plt.imshow(wordcloud)
plt.show()


for region in locations:
    for country in locations[region]:
        city_list = locations[region][country]
        tweets = None
        for city in city_list:
            print(city)
            search_term_query = f"({' OR '.join(term for term in search_terms)}) near:{city} since:2022-09-08 until:2022-09-10 lang:en"
            print(search_term_query)
            scraped_tweets = sntwit.TwitterSearchScraper(search_term_query).get_items()
            sliced_scraped_tweets = itertools.islice(scraped_tweets, 1000)
            results = pd.DataFrame(sliced_scraped_tweets)[['date', 'content']]
            print(results.head())
            tweets = pd.concat([tweets, results])
            # tweets = pd.DataFrame(sliced_scraped_tweets)[['date', 'content']]
        print(tweets.head())
        with open(f'tweets_{country}.csv', 'w+', encoding="utf-8") as file:
            tweets.to_csv(file, sep=',', encoding='utf-8')
    


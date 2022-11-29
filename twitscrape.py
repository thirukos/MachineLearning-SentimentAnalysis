import pandas as pd
import snscrape.modules.twitter as sntwit
import itertools

search_terms = ['queen', 'elizabeth', 'colonialism', 'rip', 'royal', 'family', 'death', 'irish',
                'britain', 'uk']
exclude_terms = ['mermaid', 'minaj', 'latifah']
tweet_fields = ['date', 'content', 'lang', ]
locations = {'nagpur': '3000'}

exlude_query = 'OR -'.join(term for term in exclude_terms)
print(exclude_terms)

tweets = pd.DataFrame

for location in locations.keys():
    search_term_query = f"({' OR'.join(term for term in search_terms)}) near:{location} within:{locations[location]} {exclude_terms}"
    scraped_tweets = sntwit.TwitterSearchScraper(search_term_query).get_items()
    sliced_scraped_tweets = itertools.islice(scraped_tweets, 1000)
    print(sliced_scraped_tweets)
    pd.concat(tweets, pd.DataFrame(sliced_scraped_tweets))

print(tweets.head())
import pandas as pd
import snscrape.modules.twitter as sntwit
import itertools
import matplotlib.pyplot as plt
import ast
import numpy as np

from wordcloud import WordCloud, STOPWORDS

initial_search_terms = ['queen', 'elizabeth', 'colonialism', 'rip', 'royal family', 'death', 'irish',
                'britain', 'uk']

exclude_terms = ['-mermaid', 'minaj', 'latifah']
tweet_fields = ['date', 'content', 'lang', ]
locations = {'southasia': {'india': ['delhi', 'mumbai', 'chennai', 'bangalore', 'kolkata'],
                           'pakistan':['karachi', 'lahore'],
                           'nepal':['Kathmandu']}, 
             'ireland': {'ireland': ['dublin', 'galway']},
             'uk': {'uk': ['london', 'glasgow', 'york', 'swansea']},
             'us': {'useast': ['"new york"', 'washington'],
                    'uswest': ['"san fransisco"', '"los angeles"'],
                    'uscentral': ['"Kansas City"', 'denver']},
             'canada': {'canada': ['toronto', 'montreal', 'vancouver']},
             'europe': {'germany': ['berlin', 'munich'],
                        'sweden': ['stockholm']}}

exclude_query = ' OR -'.join(term for term in exclude_terms)

def get_all_tweets():
    dates = {'1':'since:2022-09-08 until:2022-09-09', '2':'since:2022-09-09 until:2022-09-10', '3':'since:2022-09-10 until:2022-09-11'}
    # Using a word cloud to select popular words in timeframe
    for date in dates.keys():
        search_query = f'#queenelizabeth {dates[date]}'
        print(search_query)
        s_tweets = sntwit.TwitterSearchScraper(search_query).get_items()
        sliced_s_tweets = itertools.islice(s_tweets, 5000)
        all_tweets = pd.DataFrame(sliced_s_tweets)[['content']]
        all_tweets.to_csv(f'data_{date}.csv', sep=',')

def generate_wordcloud():
    processed = pd.DataFrame()
    for i in range(1,4):
        inp = pd.read_csv(f'data_p_{i}.csv')
        processed = pd.concat([processed, inp])

    print(processed.head())
    stop_words = ['queenelizabeth', 'queenelizabethii', 'queen', 'elizabeth'] + list(STOPWORDS)
    words = []
    for line in processed['content'].tolist():
        words.extend([word for word in ast.literal_eval(line)])
    wordcloud = WordCloud(stopwords = stop_words, min_word_length = 3, max_words = 40, background_color="white").generate(' '.join(words))
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.show()


tweets = pd.DataFrame()

# generate_wordcloud()

search_terms = ['"rest in peace"', 'kingcharles', 'rip', 'abolishthemonarchy', '"royal family"', 
                'england', '"reina isabel"', 'death', 'majesty']
for region in locations:
    for country in locations[region]:
        city_list = locations[region][country]
        tweets = None
        for city in city_list:
            print(city)
            search_term_query = f'({" OR ".join(term for term in search_terms)}) near:{city} within:10km since:2022-09-08 until:2022-09-10 lang:en'
            print(search_term_query)
            scraped_tweets = sntwit.TwitterSearchScraper(search_term_query).get_items()
            sliced_scraped_tweets = itertools.islice(scraped_tweets, 1000)  
            results = pd.DataFrame(sliced_scraped_tweets)[['date', 'content']]
            print(np.where(pd.isnull(results)))
            for index, row in results.iterrows():
                if '\n' in row['content']:
                    results.at[index, 'content'] = str(row['content']).replace('\n', '')
            print(np.where(pd.isnull(results)))
            tweets = pd.concat([tweets, results])
            # tweets = pd.DataFrame(sliced_scraped_tweets)[['date', 'content']]
        print(tweets.head())
        with open(f'tweets_{country}.csv', 'w+', encoding="utf-8") as file:
            tweets.to_csv(file, sep=',', encoding='utf-8')
    


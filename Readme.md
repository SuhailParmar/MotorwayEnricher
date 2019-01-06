# Motorway Enricher

## Aim

Build a bigger picture around official highways agency tweets. The original tweet will have been mined to identify key attributes.

## Potential Flow

- Recieve Tweet from Rabbit? Bind to a duplicated queue?

- Reads the Json fields to identify what where and when

- Cross references with tier 1 Tweets?
  - Go to every Handle
  - Search if they tweeted in an +-x timeframe of the original tweet
  - See if the tweet is relevant???
  - record tweet. Repeat for every handle.

    Create a tokeniser_func() (do we want to preserve the original word? e.g. unstem)

    Use TfidfVectorizer with a custom list of stopwords too?

    TfidfVectorizer can create a matrix of all documents

    Once in a standardised format we can extract how similar each tweet is to each other by using the *cosine similarity* method.

    Once in the matrix we can run clustering algorithms to determine common phrases/reasonings between each tweet.

Repeat for others:
- Calulate tweet discovery maybe use GeoLocation??
- Repeat Statistical parts

Determine which information should be used.

Create the Json payload containing the information found:

```json
# Example returned object
{
    "extra_information": {
        "original_tweet_id": 0101...,
        "cause_of_incident": "",
        "delay_caused?": "",
    }
}
```




### How To 'Build a bigger picture'

```
Original Tweet    : Accident, junction 15, M6, 12:35
Tweet Scraper     : {"payload": "Congestion at junction 12", "created_at": 01923}
Tweet Converter   : {"closest_cities": [x, y], "direction": "n", "extra_information": []}
                  : POST ^converted_tweet to the MotorwayAPI AND to the enricher

Enricher
         : Retreives converted_tweet
         : Queries TRUSTED_TWEETERS to derive information
         : Queries OTHER_TWEETERS to derive other information
         : Generate the geo-location for the account
         : Populate an opinion segment??
```

```json
-- Attribute from the tweet_miner'd tweet
{
    "extra_information: {
    }
}
```

```json
-- Post enrichment data
{
    "original_tweet_id": 0101...,
    "cause_of_incident": "",
    "delay_caused?": "",
}
```


https://en.wikipedia.org/wiki/Tf%E2%80%93idf


## Interpretation 2

### Data collection

- What should be collected?
    - Only English language Tweets
    - Tweets specifically related to the motorway asked for
    - Tweets which are located in england
    - Tweets specifically related to junctions, otherwise it would be impossible to map where the incidents occured.
    - Tweets from a variety of accounts, Tier 1 trusted and Tier 2 general
    - Data from within 24 hours of the incident period

- How much data should be gathered?
    - Max 100 tweets around a specific incident
    - Each tweet should contain a key word [congestion, traffic, accident etc], based on the reason of the accident. Queried with M6 | Motorway6


- Where is this infomation going to be temp, stored?
    Cache e.g. redis as the information is short lived (tweet based).

- What should be discarded?

### Data pre-processing, Cleaning the data.

Data should be first tokenized.

Data should be cleaned of words which don't convey meaning (Stopwords)

Data should then be lemmatized, reduced to root words for lexical normilization.

Entities should be extracted from the data?

return a list of useful phrases from the tweet

I want to have a micro understanding of each tweet

### Data transformation,

useful_phrases will be converted into a tf-idf matrix. Term frequency-inverse document frequency.

Each tweet will be classed as a document



### Data analysis,

Once clustered we can visualised and determine which cluster to use when adding more information.

### Results interpretation
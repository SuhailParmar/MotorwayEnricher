# Motorway Enricher

## Aim

Build a bigger picture around official highways agency tweets. The original tweet will have been mined to identify key attributes.

### How To 'Build a bigger picture'

```
Tweet    : Accident, junction 15, M6, 12:35
         :
Enricher : Oauth connects to API
         : Retreives latest tweet, determines if it has already been queried
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
{
    "original_tweet_id": 0101...,
    "cause_of_incident": "",
    "delay_caused?": "",

}
```


https://en.wikipedia.org/wiki/Tf%E2%80%93idf

## Work Flow:

- Every time the API recieves a tweet ping the enricher with the  tweet ID of the latest tweet

- Enricher gets the tweet ID.

- Enricher reads the junction of the tweet :: (15)
- Enricher reads the reason of the tweet   :: ('congestion')

- Enricher figures out the Geo-Location of the Junction (-172...)
- Enricher attempts to find tweets containing 'Relevant Search Params'

 Relevant Search Params:

Query Trusted Accounts
-

Tier 1: permutations of congestion::
        [ (Congestion, congestion), (Junction 15) or (M6) ]

Tier 2: synonyms for congestion::
        [ (Traffic)]

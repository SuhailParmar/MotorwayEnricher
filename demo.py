from lib.twitter_client import TwitterClient
from lib.logger import Logger
import logging
from lib.twitter_client import TwitterClient
from lib.relevance_checker import RelevanceChecker
from lib.document_clusterer import DocumentClusterer
from lib.natural_language import NaturalLanguage
from lib.utils import Utils

"""
An Offline Demoable example of this Project.
"""

Logger.initiate_logger()

main_logger = logging.getLogger("MotorwayEnricher Demo")


rc = RelevanceChecker()
utils = Utils()
tc = TwitterClient()
dc = DocumentClusterer()
nt = NaturalLanguage()


swan_tweet = {
    "screen_name": "Traffic_M6",
    "created_at": "Thu Feb 21 08:48:45 +0000 2019",
    "id": 104,
    "payload": "#M6 northbound between J19 (Tabley Interchange) and J20 (M56) - Congestion - Full details at https://www.MotorwayCameras.co.uk/Traffic#M6  (Updated every 5 minutes)"
}

original_tweet = {
    "screen_name": "Traffic_M25",
    "created_at": "Mon Jan 28 05:00:45 +0000 2019",
    "id": 103,
    "payload": "#M25 clockwise between J8 (Reigate / Redhill) and J9 (Leatherhead / Epsom) - General Obstruction - Full details at https://www.MotorwayCameras.co.uk/Traffic#M25  (Updated every 5 minutes)"
}

mined_tweet = {
    "metadata": "Event Generated by Tweet Miner at 2019-01-28T11:44:48.106533",
    "motorway": 25, "event_id": 104, "junction": [8, 9], "direction": "s",
    "closest_cities": ["Reigate / Redhill", "Leatherhead / Epsom"],
    "reason": "general obstruction",
    "extra_information": "", "time_day_worded": "Mon",
    "time_timestamp": "2019-01-28T05:00:45", "time_day_numerical": 28,
    "time_year": 2019, "time_hour": 5, "time_minutes": 0,
    "time_seconds": 45
}

tweets_gathered = ['travel: very slow traffic due to lorry tyre on the road earlier on m25 clockwise from j8 a217 brighton road (reigat… ',
                   "travel: very slow on the m25 clockwise through j8 reigate after a lorry broke down earlier. it's also generally bus… ",
                   '#m25 very slow lorry tyre on the road earlier on m25 clockwise from j8 reigate to j9 leatherhead. congestion to j7… ',
                   '#m25 clockwise between j8 (reigate / redhill) and j9 (leatherhead / epsom) - general obstruction - full details at… ',
                   'm25 clockwise between j8 and j9 | clockwise | general obstruction',
                   'travel: the m25 is already building up clockwise into j6 and further round between j8 and j9 a lorry is having a ty… ',
                   'thinking of getting a #dog this #january #newyear? live within 20 miles radius of j8 m25 #reigate? billy our 14 yr-… ',
                   '#m25 anti-clockwise we have 2 lanes closed between j10 and j9 following a multiple vehicle collision.  30 minute de… ',
                   '#m25 anti-clockwise at the cobham services between j10 (guildford / woking / esher) and j9 (leatherhead / epsom) -… ',
                   "#m25 two lanes closed q's multi-vehicle accident anticlockwise from j10 a3 wisley to j9 leatherhead.lanes three and… ",
                   '#m25 anti-clockwise between j10 (guildford / woking / esher) and j9 (leatherhead / epsom) - congestion - full detai… ',
                   '#m25 anticlockwise - two lanes closed and queueing traffic due to a multi-vehicle accident between j10 (wisley inte… ',
                   '#m25 clockwise between j8 (reigate / redhill) and j9 (leatherhead / epsom) - general obstruction - full details at… ',
                   'm25 clockwise between j8 and j9 | clockwise | general obstruction',
                   'travel: the m25 is already building up clockwise into j6 and further round between j8 and j9 a lorry is having a ty… ',
                   'travel: very slow traffic due to lorry tyre on the road earlier on m25 clockwise from j8 a217 brighton road (reigat… ',
                   '#m25 very slow lorry tyre on the road earlier on m25 clockwise from j8 reigate to j9 leatherhead. congestion to j7… ',
                   'm25 anti-clockwise between j10 and j9 | anti-clockwise | accident',
                   'travel: two lanes closed and queueing traffic due to accident on m25 anticlockwise from j10 a3 (wisley interchange)… ',
                   '#m25 anti-clockwise between j10 (guildford / woking / esher) and j9 (leatherhead / epsom) - accident - full details… ',
                   'm25 anti-clockwise between j10 and j9 | anti-clockwise | congestion'
                   ]


def callback():
    # What do do when a message arrives

    tweet = mined_tweet

    main_logger.info(
        'Recieved message from Queue:{}'.format(tweet))

    motorway_and_junctions = ['M25', 'J8', 'J9']
    other_info = ['clockwise', 'general', 'obstruction',
                  'reigate', 'redhill', 'leatherhead', 'epsom']
    kws = [*motorway_and_junctions, *other_info]
    kws = nt.convert_to_lowercase(kws)

    # Strip keywords out
    stripped_tweets = Utils.strip_words(
        tweets_gathered,
        kws)

    # Begin Clustering
    cluster_one = dc.main(stripped_tweets)
    data = {"extra_information": cluster_one}

    tid = 1105020881515040768

    from lib.api_requests import APIRequests
    from json import dumps

    api = APIRequests()
    api.patch_to_api(tid, dumps(data))


if __name__ == "__main__":
    callback()

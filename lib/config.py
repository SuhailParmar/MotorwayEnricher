from os import getenv

# Motorway API specific values
api_base_url = getenv('API_BASE_URL', 'localhost')
api_post_endpoint = getenv('API_POST_ENDPOINT', 'api/events/')
api_port = getenv('API_PORT', 8000)

api_client_id = getenv(
    'API_ID', "motorway_enricher")  # Not real value

api_client_secret = getenv(
    'API_SECRET', "supersecret")  # Not real value

log_file = getenv('LOG_FILE', 'motorway_enricher.log')

# MotorwayRabbitBroker specific values
rabbit_host = getenv('MQ_HOST', 'localhost')
rabbit_port = getenv('MQ_PORT', 5672)
rabbit_source_queue = getenv('MQ_SOURCE_QUEUE', 'M6_Enriched')
rabbit_dlqueue = getenv('MQ_DL_QUEUE', 'M6_Dead_Letter')
rabbit_username = getenv('MQ_USERNAME', 'guest')
rabbit_password = getenv('MQ_PASSWORD', 'guest')
rabbit_exchange = getenv('MQ_EXCHANGE', 'MotorwayExchange')
rabbit_dl_routing_key = getenv('MQ_DL_ROUTING_KEY', 'M6_DL')
rabbit_vhost = getenv('MQ_VHOST', 'motorway_vhost')

# Connecting to the Twitter API
twitter_at_token = getenv("ACCESS_TOKEN",
                          "891994636285333504-BNjZKOEhdWjax3RtcCFOI5zhcX576uY")
twitter_at_secret = getenv("ACCESS_TOKEN_SECRET",
                           "mPrE2VhLeUURSrEcWk7kicDekzPpMESdnFrGNKLoSi2im")
twitter_api_key = getenv("API_KEY", "qfFuhBlJ8agaMAf322KDEHJe2")
twitter_api_secret = getenv(
    "API_SECRET", "K69lGLENMMrzXbS9d0H8wso1xui06TpD1aZQjvPGH8dLkE0TUp")

from os import getenv

api_base_url = getenv('API_BASE_URL', 'localhost')
api_post_endpoint = getenv('API_POST_ENDPOINT', 'api/events/')
api_port = getenv('API_PORT', 8000)

api_client_id = getenv(
    'API_ID', "motorway_enricher")  # Not real value

api_client_secret = getenv(
    'API_SECRET', "supersecret")  # Not real value

log_file = getenv('LOG_FILE', 'motorway_enricher.log')

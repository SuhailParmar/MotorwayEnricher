# A list of words which provide no extra meaning
# If these arent filtered out the tf-idf matrix will
# Have meaningless words with a greater weight

meaningless_words = [
    "travel", "due", "earlier", "slow", "road", "anti", "details",
    "accident"  # Contentious one...
]
class GConfig:
    class Cache:
        # MT : memoized times
        camp_userCount_MT = 0

    class Topic:
        options_per_page = 30
        userTopic_MT = 0
        popularTopic_MT = 0

        # popular topic in the last ? days
        popularTopicLast_Days = 30

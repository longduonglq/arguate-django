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
        recountTopicAfterModerated = 10 # minutes

    class User:
        markUserInactiveAfter = 15 # days
        markUserInactiveTimeCycle = 5 # minutes

        markUserOfflineAfter = 15
        markUserOfflineTimeCycle = 10 # minutes


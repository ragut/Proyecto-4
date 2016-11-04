import memcache

class ElastiCache:
    mc = None

    def __init__(self):
         self.mc = pylibmc.Client(["dmlogin.frkbsz.0001.usw2.cache.amazonaws.com",
                                  "dmlogin.frkbsz.0002.usw2.cache.amazonaws.com",
                                  "dmlogin.frkbsz.0003.usw2.cache.amazonaws.com"],
                                 binary=True,
                                 behaviors={"tcp_nodelay": True, "ketama": True})

    def set_variable(self, key, value):
        try:
            return self.mc.set(key,value)
        except:
            return None

    def get_variable(self, key):
        try:
            return self.mc.get(key)
        except:
            return None



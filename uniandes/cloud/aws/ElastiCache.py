import memcache

class ElastiCache:
    mc = None

    def __init__(self):
        self.mc = memcache.Client(["dlogin.frkbsz.cfg.usw2.cache.amazonaws.com:11211"], debug=0)


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



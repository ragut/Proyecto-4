import pylibmc
import os


class ElasticCache:
    mc = None

    def __init__(self):
        self.mc = pylibmc.Client(os.environ.get('MEMCACHIER_SERVERS', '').split(','), binary=True,
                    username=os.environ.get('MEMCACHIER_USERNAME', ''), password=os.environ.get('MEMCACHIER_PASSWORD', ''),
                    behaviors={
                      # Faster IO
                      "tcp_nodelay": True,
                      "no_block": True,

                      # Timeout for set/get requests
                      "_poll_timeout": 2000,

                      # Use consistent hashing for failover
                      "ketama": True,

                      # Configure failover timings
                      "connect_timeout": 2000,
                      "remove_failed": 4,
                      "retry_timeout": 2,
                      "dead_timeout": 10,
                    })

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
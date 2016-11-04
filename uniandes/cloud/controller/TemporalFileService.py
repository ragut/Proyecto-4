import os

class TemporalFileService:
    url_converted = None

    def __init__(self):
        self.url_converted = os.path.abspath(__file__ + "/../../tmp")+"/"
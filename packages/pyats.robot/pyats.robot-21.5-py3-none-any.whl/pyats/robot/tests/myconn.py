class MyConn(object):
    # mock class

    def __init__(self, *args, **kwargs):
        pass

    def connect(self, *args, **kwargs):
        self.connected = True

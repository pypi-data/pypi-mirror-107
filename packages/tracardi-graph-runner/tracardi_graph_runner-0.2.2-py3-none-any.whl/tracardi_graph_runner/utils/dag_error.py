class DagError(ValueError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.port = kwargs['port'] if 'port' in kwargs else None

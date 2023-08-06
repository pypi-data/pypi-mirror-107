
class DMSalesAPIConnectionError(Exception):
    
    def __init__(self, timeout, *args, **kwargs):
        self.timeout = timeout
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f'Connection Timeout (timeout: {self.timeout}). Check if your api key hasn\'t expired'


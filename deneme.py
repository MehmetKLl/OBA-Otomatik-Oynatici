import requests_toolbelt
import random
import string

class create_multipart_data:
    def __init__(self,field,boundary=None):
        encoder = requests_toolbelt.MultipartEncoder(fields=field,
                                                     boundary=f"----WebKitFormBoundary{''.join(random.sample(string.digits+string.ascii_letters,k=16))}" if boundary is None else f"----WebKitFormBoundary{boundary}")
        self.body = encoder.to_string()
        self.content_type = encoder.content_type
        

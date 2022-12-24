class BorderNotFoundException(Exception):
    pass

class ImageNotFoundException(Exception):
    def __init__(self, *args, **kwargs):
        self.image = kwargs["image"]
        kwargs.pop("image")
        super().__init__(*args, **kwargs)
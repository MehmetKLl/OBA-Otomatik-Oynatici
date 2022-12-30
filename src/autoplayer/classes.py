from . import events
from numpy import array_equal

class CapturedImage:
    def __init__(self, x_pos, y_pos, width, height, image_array):
        self.x_pos, self.y_pos, self.width, self.height, self.image_array = x_pos, y_pos, width, height, image_array

    def __repr__(self):
        return f"CapturedImage(x={self.x_pos}, y={self.y_pos}, width={self.width}, height={self.height})"

    def __eq__(self,obj):
        if isinstance(obj, CapturedImage):
            return (obj.x_pos, obj.y_pos) == (self.x_pos, self.y_pos) and array_equal(self.image_array, obj.image_array)
        
        return False

    def get_pos(self):
        return (self.x_pos, self.y_pos, self.width, self.height)

    def click(self,button,scroll_value=None):
        if button.lower() != "scroll" and scroll_value is not None:
            raise ValueError("Third parameter is only usable at scroll mode.")
        
        if button.lower() == "left":
            return events.left_click(self.x_pos, self.y_pos)

        elif button.lower() == "right":
            return events.right_click(self.x_pos,self.y_pos)
            
        elif button.lower() == "scroll":
            return events.scroll(scroll_value,self.x_pos,self.y_pos)
        
        raise ValueError(f"Invalid button name: \"{button}\"")

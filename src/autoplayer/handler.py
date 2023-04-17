from win32api import GetSystemMetrics
from win32con import SRCCOPY
from win32gui import GetDesktopWindow, GetWindowDC, DeleteObject, ReleaseDC
from win32ui import CreateDCFromHandle, CreateBitmap
from numpy import uint8, frombuffer, where
from cv2 import cvtColor, COLOR_BGRA2BGR, COLOR_BGR2HSV, imread, matchTemplate, TM_CCOEFF_NORMED, split
from .classes import CapturedImage
from utils.exceptions import ImageNotFoundException

class Screen:
    def __init__(self):
        self.height = GetSystemMetrics(1)
        self.width = GetSystemMetrics(0)
        
        hwnd = GetDesktopWindow()
        hwnddc = GetWindowDC(hwnd)
        mfcdc = CreateDCFromHandle(hwnddc)
        savedc = mfcdc.CreateCompatibleDC()
        
        bitmap = CreateBitmap()
        bitmap.CreateCompatibleBitmap(mfcdc,self.width,self.height)

        savedc.SelectObject(bitmap)

        bmp = savedc.BitBlt((0,0), (self.width,self.height), mfcdc, (0, 0), SRCCOPY)

        bmp_info = bitmap.GetInfo()
        bmp_bytes = bitmap.GetBitmapBits(True)

        self.screen_array = cvtColor(cvtColor(frombuffer(bmp_bytes, dtype=uint8).reshape((self.height,self.width,4)), COLOR_BGRA2BGR), COLOR_BGR2HSV)
        
        DeleteObject(bitmap.GetHandle())
        savedc.DeleteDC()
        mfcdc.DeleteDC()
        ReleaseDC(hwnd,hwnddc)

        

    def capture(self, image=None, threshold=0.99, mode="single", exceptions="silent"):
        if mode not in ["single","all"] or exceptions not in ["silent","raise"]:
            raise ValueError("Invalid arguments.")
        
        self.template_image_array = cvtColor(cvtColor(imread(image), COLOR_BGRA2BGR), COLOR_BGR2HSV)
        self.template_height, self.template_width, _ = self.template_image_array.shape

        match_template_array = where(matchTemplate(self.screen_array, self.template_image_array, TM_CCOEFF_NORMED) >= threshold)

        x_array, y_array = match_template_array[1], match_template_array[0]


        if x_array.size == 0 or y_array.size == 0:
            if exceptions == "raise":
                raise ImageNotFoundException(f"Image \"{image}\" couldn't found.",image=image)

            return None

        if mode == "single":
            return CapturedImage(x_array[0], y_array[0], self.template_width, self.template_height, self.template_image_array)

        matched_sub_images_objects = [CapturedImage(x, y, self.template_width, self.template_height, self.template_image_array) for x, y in zip(x_array, y_array)] 
        return matched_sub_images_objects
            


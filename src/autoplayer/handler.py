from win32api import GetSystemMetrics
from win32con import SRCCOPY
from win32gui import GetDesktopWindow, GetWindowDC, DeleteObject, ReleaseDC
from win32ui import CreateDCFromHandle, CreateBitmap
from numpy import uint8, frombuffer, where
from cv2 import cvtColor, COLOR_BGRA2BGR, COLOR_BGR2HSV, imread, matchTemplate, TM_CCOEFF_NORMED
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

        bitmap_bytes = bitmap.GetBitmapBits(True)

        self.screen_array = cvtColor(cvtColor(frombuffer(bitmap_bytes, dtype=uint8).reshape((self.height,self.width,4)), COLOR_BGRA2BGR), COLOR_BGR2HSV)
        
        DeleteObject(bitmap.GetHandle())
        savedc.DeleteDC()
        mfcdc.DeleteDC()
        ReleaseDC(hwnd,hwnddc)

        

    def capture(self, image=None, threshold=0.99, mode="single", exceptions="silent"):
        if mode not in ["single","all"] or exceptions not in ["silent","raise"]:
            raise ValueError("Invalid arguments.")
        
        self.template_image_array = cvtColor(cvtColor(imread(image), COLOR_BGRA2BGR), COLOR_BGR2HSV)
        self.template_height, self.template_width, _ = self.template_image_array.shape

        matched_template_cords = where(matchTemplate(self.screen_array, self.template_image_array, TM_CCOEFF_NORMED) >= threshold)

        x_cords, y_cords = matched_template_cords[1], matched_template_cords[0]


        if x_cords.size == 0 or y_cords.size == 0:
            if exceptions == "raise":
                raise ImageNotFoundException(f"Image \"{image}\" couldn't found.",image=image)

            return None

        if mode == "single":
            return CapturedImage(x_cords[0], y_cords[0], self.template_width, self.template_height, self.template_image_array)

        matched_sub_images_objects = [CapturedImage(x, y, self.template_width, self.template_height, self.template_image_array) for x, y in zip(x_cords, y_cords)] 
        return matched_sub_images_objects
            


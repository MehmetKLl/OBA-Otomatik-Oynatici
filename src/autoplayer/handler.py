from win32api import GetSystemMetrics
from win32con import SRCCOPY
from win32gui import GetDesktopWindow, GetWindowDC, DeleteObject, ReleaseDC
from win32ui import CreateDCFromHandle, CreateBitmap
from numpy import uint8, frombuffer, where
from cv2 import cvtColor, COLOR_BGRA2RGB, imread, matchTemplate, TM_CCOEFF_NORMED
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

        self.screen = cvtColor(frombuffer(bmp_bytes, dtype=uint8).reshape((self.height,self.width,4)), COLOR_BGRA2RGB)
        
        DeleteObject(bitmap.GetHandle())
        savedc.DeleteDC()
        mfcdc.DeleteDC()
        ReleaseDC(hwnd,hwnddc)

        

    def capture(self, image=None, threshold=0.99, mode="single", exceptions="silent"):
        if mode not in ["single","all"] or exceptions not in ["silent","raise"]:
            raise ValueError("Invalid arguments.")

        
        self.template_image = cvtColor(imread(image), COLOR_BGRA2RGB)
        self.template_height, self.template_width, _ = self.template_image.shape


        match_template_array = matchTemplate(self.screen, self.template_image, TM_CCOEFF_NORMED)

        matched_sub_images_cord_array = where(match_template_array >= threshold)
        x_array, y_array = matched_sub_images_cord_array[1], matched_sub_images_cord_array[0]


        if x_array.size == 0 or y_array.size == 0:
            if exceptions == "raise":
                raise ImageNotFoundException(f"Image \"{image}\" couldn't found.",image=image)

            return None

        if mode == "single":
            return CapturedImage(x_array[0], y_array[0], self.template_width, self.template_height, self.template_image)

        matched_sub_images_objects = [CapturedImage(x, y, self.template_width, self.template_height, self.template_image) for x, y in zip(x_array, y_array)] 
        return matched_sub_images_objects
            


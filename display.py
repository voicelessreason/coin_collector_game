from ctypes import windll, byref
import ctypes.wintypes
from turtle import screensize

class Display:

   @classmethod
   def get_screen_size(cls):
      '''
      Get the dimensions of the area in which the game window can be drawn
      without overflowing.

      We're reach into the Win32 API and grabbing:
      1. The current working area size. This is the size of the screen, 
         minus the height of the Windows taskbar.
      2. The system's default height of a window title bar.
      
      We then subtract #2 from  #1, and that gives us the amount of space we have
      in which to draw the game window.

      In a multi-monitor setup, this will only retrieve the dimensions of the primary monitor,
      and so the game window will be rendered with respect to that.

      Returns:
      If system information is successfully retrieved:
         A tuple with the format (WORKING_AREA_WIDTH, WORKING_AREA_HEIGHT - TITLE_BAR_HEIGHT)
      Else:
         A tuple (-1, -1)

      '''
      user32 = windll.user32
      
      try:
         border_thickness = user32.GetSystemMetrics(8)
         caption_area_height = user32.GetSystemMetrics(4)
         border_padding = user32.GetSystemMetrics(92)
      except:
         # If for whatever reason, we can't get the actual values, fudge it using expected values.
         border_thickness = 3
         caption_area_height = 23
         border_padding = 4

      title_bar_height = border_thickness + caption_area_height + border_padding

      work_area = ctypes.wintypes.RECT()
      success = user32.SystemParametersInfoW(48, 0, byref(work_area), 0)

      if(success):
         return work_area.right, work_area.bottom - title_bar_height
      else:
         return -1, -1

   @classmethod
   def get_max_window(cls, max):
      '''
      Get the upper bound for the dimensions of the game window.

      When either the width or height of the user's display monitor is smaller
      than 1000px, return the smallest of the three.
      This will be the upper bound on the size of the game window
      and prevent it from overflowing the bounds of the user's display.

      Returns:
      An integer, which is the minimum of SCREEN_WIDTH, SCREEN_HEIGHT, and 1000px.
      '''
      screen_size = cls.get_screen_size()
      if(-1 in screen_size):
         return max
      else:
         smallest_dimension = min(screen_size)
         max_window = min(smallest_dimension, max)
      return max_window

#print(Display.get_max_window(1000))
from config import *
from pygame.font import SysFont

class TextHelper:

   def __init__(self, fullscreen_helper):
      '''
      Attributes:
      fh: An object of class FullscreenHelper.
      '''
      self.fh = fullscreen_helper
   
   def blit_text(self, string, font, positioning_function, screen):
      '''
      Draws a string as text with a font, position, and surface.

      Parameters:
      string: A string of text.
      font: A pygame SysFont object.
      positioning_function: A function that returns a tuple (x, y) of where the text should be drawn.
      screen: A display surface on which to draw the text. Returned by pygame.display.set_mode().
      '''
      text = font.render(string, True, TEXT_COLOR)

      position = positioning_function(text)

      self.blit_border(string, font, position, screen, BLACK)

      screen.blit(text, position)


   def blit_border(self, string, font, position, screen, color):
      '''
      Builds up a border around a piece of text by drawing that same text underneath it.

      Parameters:
      string: A string of text.
      font: A pygame SysFont object.
      position: A tuple (x, y) representing the top-left coordinate of the text we want to border-ify.
      screen: A display surface on which to draw the text.
      color: The border color.
      '''
      shadow_text = font.render(string, True, color)

      shadow_location = (position[0] + 1, position[1] + 1)
      screen.blit(shadow_text, shadow_location) 

      shadow_location = (position[0] + -1, position[1] + -1)
      screen.blit(shadow_text, shadow_location)

      shadow_location = (position[0] + +1, position[1] + -1)
      screen.blit(shadow_text, shadow_location)

      shadow_location = (position[0] + -1, position[1] + +1)
      screen.blit(shadow_text, shadow_location)
      
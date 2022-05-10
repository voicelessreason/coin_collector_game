from config import *

class FullscreenHelper:
   
   def __init__(self, desktop_resolution):
      '''
      Attributes:
      ~~~~~~~~~~~      
      As Parameters:
      desktop_resolution: The tuple returned by pygame.display.get_desktop_sizes()[0]
         play_area_upper_bound is the maximum.

      From config.py:
      tiles_per_row: The number of tiles in each row (and column, since the play area is a square)
      base_play_area_size: The size of the play area at which fonts are rendered in their base size.
      base_header_font_size: The base size of the header font.
      base_subheader_font_size: The base size of the subheader font.

      Calculated on instantiation:
      smaller_screen_dimension: The smaller dimension of desktop_resolution (either width or height).
      larger_screen_dimension: The larger dimension of desktop_resolution.
      actual_play_area_size: A tuple of two equal values. The size of the play area (bounded by the rock border).
         Determined by smaller_screen_dimension to ensure that the entire play area always fits on the screen.
      scaling_ratio: Responsible for scaling font sizes up and down.
      tile_size: The size of each tile. Scales with play_area_size.
      actual_header_font_size: The font size at which headers are rendered, scaled appropriately.
      actual_subheader_font_size: The font size at which subheaders are rendered, scaled appropriately.
      play_area_offset: Because we are shifting the play area to the center, we need to offset where
         we draw sprites and text. This is that offset as a dict.
      self.play_area_center: The center coordinates of the play area. Useful for centering text.
      '''
      self.desktop_resolution = desktop_resolution

      self.tiles_per_row = TILES_PER_ROW
      self.base_play_area_size = BASE_PLAY_AREA_SIZE
      self.base_header_font_size = BASE_HEADER_FONT_SIZE
      self.base_subheader_font_size = BASE_SUBHEADER_FONT_SIZE

      self.smaller_screen_dimension = min(self.desktop_resolution)
      self.larger_screen_dimension = max(self.desktop_resolution)
      self.actual_play_area_size = (self.smaller_screen_dimension, self.smaller_screen_dimension)
      self.scaling_ratio = self.smaller_screen_dimension / self.base_play_area_size
      self.tile_size = self.smaller_screen_dimension // self.tiles_per_row
      self.actual_header_font_size = int(self.base_header_font_size * self.scaling_ratio)
      self.actual_subheader_font_size = int(self.base_subheader_font_size * self.scaling_ratio)
      self.play_area_offset = {
         'x': (self.desktop_resolution[0] - self.actual_play_area_size[0]) // 2,
         'y': (self.desktop_resolution[1] - self.actual_play_area_size[1]) // 2
      }
      self.play_area_center = {
         'x': self.play_area_offset['x'] + self.actual_play_area_size[0] // 2,
         'y': self.play_area_offset['y'] + self.actual_play_area_size[1] // 2
      }

   def get_centered_text_position(self, text__size):
      '''
      Determines where text should be positioned in order to be perfectly centered.

      Parameters:
      font_size: A tuple (width, height) of a line of text.
      Returns:
      A tuple (x, y) representing the top-left corner of a centered line of text.
      '''
      return (self.play_area_center['x'] - text__size[0] // 2, self.play_area_center['y'] - text__size[1] // 2)
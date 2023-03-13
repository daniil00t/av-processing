from PIL import Image
import numpy as np

def pixel_mean_value_grayscale(pixel) -> int:
  return int(round((pixel[0] + pixel[1] + pixel[2]) / 3))

def pixel_photoshop_grayscale(pixel) -> int:
  return int(round(pixel[0] * 0.3 + pixel[1] * 0.59 + pixel[2] * 0.11))

def mean_grayscale(image) -> Image:
  result = Image.new('L', (image.width, image.height))
  for x in range(result.width):
    for y in range(result.height):
      pixel = image.getpixel((x, y))
      new_pixel = int(round((pixel[0] + pixel[1] + pixel[2]) / 3))
      result.putpixel((x, y), new_pixel)
  return result

def photoshop_grayscale(image: Image) -> Image:
  result = Image.new('L', (image.width, image.height))

  for x in range(result.width):
    for y in range(result.height):
      pixel = image.getpixel((x, y))
      new_pixel = int(round(pixel[0] * 0.3 + pixel[1] * 0.59 + pixel[2] * 0.11))
      result.putpixel((x, y), new_pixel)
  return result

def two_threshold_binarize(image: Image, th_one: int, th_two: int, reverse = False) -> Image:
  # Применение бинаризации (одной строчкой)
  # return image.point(lambda x: 0 if x < th_one else (255 if x > th_two else x))

  grayscale_image = photoshop_grayscale(image)
  result = Image.new('L', (image.width, image.height))

  WHITE = 255
  BLACK = 0

  width, height = grayscale_image.size

  for x in range(width):
    for y in range(height):
      pixel = grayscale_image.getpixel((x, y))
      new_pixel = BLACK if not reverse else WHITE
      if(pixel < th_two and pixel > th_one):
        new_pixel = WHITE if not reverse else BLACK
      result.putpixel((x, y), new_pixel)

  return result
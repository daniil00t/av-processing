from PIL import Image
import numpy as np
import math
from progress import print_progress 


def upsampling (image: Image, k: int) -> Image:
  width, height = image.size

  pixels = image.load()

  newWidth = width * k
  newHeight = height * k

  newPixels = np.random.random_integers(0, 255, (newHeight, newWidth, 3))
  newPixels = np.array(newPixels, dtype=np.uint8)

  for i in range(width):
    # для красоты выводим прогресс выполнения функции
    for j in range(height):
      for s_i in range(k):
        for s_j in range(k):
          newPixels[j * k + s_j, i * k + s_i] = pixels[i, j]
      
  return Image.fromarray(newPixels)

def downsampling (image: Image, n: int, random_pick = False) -> Image:
  width, height = image.size

  pixels = image.load()

  newWidth = math.floor(width / n)
  newHeight = math.floor(height / n)

  newPixels = np.random.random_integers(0, 255, (newHeight, newWidth, 3))
  newPixels = np.array(newPixels, dtype=np.uint8)

  for i in range(newHeight):
    for j in range(newWidth):
      r, g, b = (0, 0, 0)

      x = j * n
      y = i * n

      # вычисление среднего значения (r, g ,b) пикселей в каждом блоке nxn
      if(random_pick):
        block = np.array(image.crop((x, y, x + n, y + n)))
        red, green, blue = list(), list(), list()

        for k in range(n):
          for m in range(n):
            red.append(block[k, m, 0])
            green.append(block[k, m, 1])
            blue.append(block[k, m, 2])

        r = int(np.mean(red))
        g = int(np.mean(green))
        b = int(np.mean(blue))
      else:
        # берем первый пиксель
        r, g, b = pixels[y, x]

      newPixels[i, j] = (r, g, b)
      
  return Image.fromarray(newPixels)

def resampling (image: Image, upsampling_k: int, downsampling_k: int) -> Image:
  return downsampling(upsampling(image, upsampling_k), downsampling_k)

def one_resampling (image: Image, m: float) -> Image:
  width, height = image.size
  pixels = image.load()

  newWidth = math.floor(width * m)
  newHeight = math.floor(height * m)

  newPixels = np.random.random_integers(0, 255, (newHeight, newWidth, 3))
  newPixels = np.array(newPixels, dtype=np.uint8)

  for i in range(newHeight):
    for j in range(newWidth):
      x = math.floor(j / m)
      y = math.floor(i / m)
      newPixels[i, j] = pixels[x, y]

  return Image.fromarray(newPixels)
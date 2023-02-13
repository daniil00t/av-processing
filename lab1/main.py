from PIL import Image
import numpy as np
import math
from progress import print_progress 


def upsampling (image: Image, k: int) -> Image:
  width, height = image.size
  pixels = image.load()
  newPixels = np.random.random_integers(0, 255, (height * k, width * k, 3))
  newPixels = np.array(newPixels, dtype=np.uint8)

  for i in range(width):
    print_progress(i, width, 5)
    for j in range(height):
      for s_i in range(k):
        for s_j in range(k):
          newPixels[j * k + s_j, i * k + s_i] = pixels[i, j]
      
  return Image.fromarray(newPixels)


def downsampling (image: Image, n: int) -> Image:
  width, height = image.size
  pixels = image.load()
  newPixels = np.random.random_integers(0, 255, (math.ceil(height / n), math.ceil(width / n), 3))
  newPixels = np.array(newPixels, dtype=np.uint8) 

  ii = 0
  for i in range(0, width, n):
    print_progress(i, width, 5)
    jj = 0
    for j in range(0, height, n):
      newPixels[jj, ii] = pixels[i, j]
      jj += 1
    ii += 1
      
  return Image.fromarray(newPixels)


def resampling (image: Image, k: int, n: int) -> Image:
  return downsampling(upsampling(image, k), n)

def one_resampling (image: Image, m) -> Image:
  width, height = image.size
  pixels = image.load()
  newPixels = np.random.random_integers(0, 255, (math.ceil(height * m), math.ceil(width * m), 3))
  newPixels = np.array(newPixels, dtype=np.uint8)

  i = 0
  while(i <= width * m - 1):
    print_progress(i, width * m - 1, 5)
    j = 0
    while(j <= height * m - 1):
      newPixels[j, i] = pixels[math.ceil(i / m), math.ceil(j / m)]
      j += 1
    i += 1

  return Image.fromarray(newPixels)


def main():
  img = Image.open('images/biggest.png', 'r').convert('RGB')

  newImage = downsampling(img, 10)
  newImage.save('images/out/biggest_0.1x.png')


if __name__ == '__main__':
  main()
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def photoshop_grayscale(image):
  result = Image.new('L', (image.width, image.height))

  for x in range(result.width):
    for y in range(result.height):
      pixel = image.getpixel((x, y))
      new_pixel = int(round(pixel[0] * 0.3 + pixel[1] * 0.59 + pixel[2] * 0.11))
      result.putpixel((x, y), new_pixel)

  return result

# получаем матрицу Харалика
def get_haralic(img):
  size = 256

  haralic_matrix = np.zeros((size, size))
  width = img.size[0]
  height = img.size[1]
  img_arr = np.asarray(img).transpose()

  for x in range(1, width - 1):
    for y in range(1, height - 1):
      pixel = img_arr[x, y]

      up_left_pixel = img_arr[x-1, y-1]
      down_left_pixel = img_arr[x-1, y+1]
      up_right_pixel = img_arr[x+1, y-1]
      down_right_pixel = img_arr[x+1, y+1]

      haralic_matrix[pixel, up_left_pixel] += 1
      haralic_matrix[pixel, down_left_pixel] += 1
      haralic_matrix[pixel, up_right_pixel] += 1
      haralic_matrix[pixel, down_right_pixel] += 1

  haralic_img = Image.fromarray(haralic_matrix).convert('L')
  return haralic_img, haralic_matrix

def get_Pj(i, matrix):
  Pj = 0
  for j in range(matrix.shape[1]):
    Pj += matrix[i, j]
  return Pj

def get_Pi(j, matrix):
  Pi = 0
  for i in range(matrix.shape[0]):
    Pi += matrix[i, j]
  return Pi

def hist_plt(image):
  matrix = np.asarray(image)
  shape = np.reshape(matrix, (1, -1))
  plt.figure()
  plt.hist(shape[0], bins=256)
  return plt

def contrast(img):
  result_matrix = np.asarray(img) / 255
  result_matrix = pow(result_matrix, 0.5)
  result_matrix = (result_matrix * 255).astype(np.uint8)
  
  result = Image.fromarray(result_matrix)
  return result

def get_con(haralic_matrix):
  size = haralic_matrix.shape[0]

  corr = 0
  for i in range(size):
    for j in range(size):
      corr += (i - j) ** 2 * haralic_matrix[i, j]

  return corr

def get_lun(haralic_matrix):

  size = haralic_matrix.shape[0]

  corr = 0
  for i in range(size):
    for j in range(size):
      corr += haralic_matrix[i, j] / (1 + (i - j) ** 2)

  return corr

def result_display(img_name):
    img = Image.open(img_name)
    grayscaled_img = photoshop_grayscale(img)
    contrast_img = contrast(grayscaled_img)

    print("Исходное изображение")
    img.save(f'{img_name}_source.png')

    print("Grayscale изображение")
    grayscaled_img.save(f'{img_name}_grayscaled.png')

    print("Контрастированное изображение")
    contrast_img.save(f'{img_name}_contrast.png')

    print("Гистограмма исходного изображения")
    hist_plt(grayscaled_img).savefig(f'{img_name}_histogram_source.png')

    print("Гистограмма контрастированного изображения")
    hist_plt(contrast_img).savefig(f'{img_name}_histogram_contrast.png')

    haralic_img, haralic_matrix = get_haralic(grayscaled_img)
    contrast_haralic_img, contrast_haralic_matrix = get_haralic(contrast_img)
    print("Матрица Харалика исходного изображения")
    haralic_img.save(f'{img_name}_haralic_source.png')

    print("Матрица Харалика контрастированного изображения")
    contrast_haralic_img.save(f'{img_name}_haralic_contrast.png')

    con = get_con(haralic_matrix)
    contrast_con = get_con(contrast_haralic_matrix)
    print(f"Корреляция исходного изображения = {con}") # change
    print(f"Корреляция контрастированного изображения = {contrast_con}")

    lun = get_lun(haralic_matrix)
    contrast_lun = get_lun(contrast_haralic_matrix)
    print(f"Корреляция исходного изображения = {lun}") # change
    print(f"Корреляция контрастированного изображения = {contrast_lun}")


    pass
from PIL import Image, ImageFont, ImageDraw, ImageOps
import numpy as np
from matplotlib import pyplot as plt
import csv

# получаем алфавит
def getAlphabet(string):
  alphabet = []
  for letter in string:
    alphabet.append(letter)

  return alphabet

# бинаризуем изображение
def simple_binarization(image, threshold):
  img_arr = np.array(image)
  new_image = np.zeros(shape=img_arr.shape)
  new_image[img_arr > threshold] = 255
  return Image.fromarray(new_image.astype(np.uint8), 'L')

# вырезаем белые места из изображения буквы
def cut_white_image_parts(image):

  for x in range(image.width-1, -1, -1):
    is_col_empty = True
    for y in range(image.height):
      if image.getpixel((x, y)) < 255:
        is_col_empty = False
        break

    if not is_col_empty:
      right_pixel = x
      break
      
  for y in range(image.height-1, -1, -1):
    is_row_empty = True
    for x in range(image.width):
      if image.getpixel((x, y)) < 255:
        is_row_empty = False
        break

    if not is_row_empty:
      bottom_pixel = y
      break
  
  for x in range(0, image.width):
    is_col_empty = True
    for y in range(image.height):
      if image.getpixel((x, y)) < 255:
        is_col_empty = False
        break

    if not is_col_empty:
      left_pixel = x
      break
      
  for y in range(0, image.height):
    is_row_empty = True
    for x in range(image.width):
      if image.getpixel((x, y)) < 255:
        is_row_empty = False
        break

    if not is_row_empty:
      upper_pixel = y
      break
      

  return image.crop(box=(left_pixel, upper_pixel, right_pixel, bottom_pixel))

def cut_empty_rows_and_cols(image):

  empty_row_numbers = []
  empty_column_numbers = []

  for x in range(image.width):
    is_col_empty = True
    for y in range(image.height):
      if image.getpixel((x, y)) < 255:
        is_col_empty = False
        break

    if is_col_empty:
      empty_column_numbers.append(x)

  for y in range(image.height):
    is_row_empty = True
    for x in range(image.width):
      if image.getpixel((x, y)) < 255:
        is_row_empty = False
        break

    if is_row_empty:
      empty_row_numbers.append(y)

  def last_element_in_a_row(elements, start_element, step):
    prev_element = start_element

    for element in elements[::step]:
      if abs(element - prev_element) > 1:
        return prev_element + step

      prev_element = element

    return prev_element + step

  left_whitespace_end = last_element_in_a_row(empty_column_numbers, -1, 1)
  upper_whitespace_end = last_element_in_a_row(empty_row_numbers, -1, 1)
  right_whitespace_end = last_element_in_a_row(empty_column_numbers, image.width, -1)
  lower_whitespace_end = last_element_in_a_row(empty_row_numbers, image.height, -1)

  return image.crop(box=(left_whitespace_end, upper_whitespace_end, right_whitespace_end + 1, lower_whitespace_end + 1))

# генерируем картинки букв и сохраняем их в файлы
def font_generate(alphabet):
  font_size = 100
  font = ImageFont.truetype("fonts/tnr_regular.ttf", font_size)

  for letter in alphabet:
    img = Image.new(mode="L", size=(font_size, font_size), color=255)
    draw = ImageDraw.Draw(img, mode = 'L')
    draw.text(xy=(0, 0), text=letter, fill=0, font=font, anchor = 'lt')
    cutted_img = cut_empty_rows_and_cols(img)
    threshloded_img = simple_binarization(cutted_img, 100)
    threshloded_img.save(f'letter_images/letter_{letter}.png')

def color_used_arr(img):
  return np.asarray(np.asarray(img) < 1, dtype = np.int0)

# получаем значения характеристик
def get_features(img):
  img_pixels = img.load()
  
  width = img.size[0]
  height = img.size[1]

  size = width * height

  weight, rel_weight, x_avg, y_avg, rel_x_avg, rel_y_avg = 0, 0, 0, 0, 0, 0
  inertia_x, rel_inertia_x, inertia_y, rel_inertia_y = 0, 0, 0, 0

  for i in range(width):
    for j in range(height):
      if img_pixels[i, j] == 0:
        weight += 1
        x_avg += i
        y_avg += j

  rel_weight = weight / size

  x_avg /= weight
  y_avg /= weight
  rel_x_avg = (x_avg - 1) / (width - 1)
  rel_y_avg = (y_avg - 1) / (height - 1)

  for i in range(width):
    for j in range(height):
      if img_pixels[i, j] == 0:
        inertia_x = (j - x_avg) ** 2
        inertia_y = (i - y_avg) ** 2

  rel_inertia_x = inertia_x / (width ** 2 + height ** 2)
  rel_inertia_y = inertia_y / (width ** 2 + height ** 2)
  
  return {
    'weight': weight,
    'rel_weight': rel_weight,
    'x_avg': x_avg,
    'y_avg': y_avg,
    'rel_x_avg': rel_x_avg,
    'rel_y_avg': rel_y_avg,
    'inertia_x': inertia_x,
    'inertia_y': inertia_y,
    'rel_inertia_x': rel_inertia_x,
    'rel_inertia_y': rel_inertia_y
  }

# получаем профили по x & y
def get_profiles(img):
  img_arr_for_calculations = color_used_arr(img)
  
  x_profiles = np.sum(img_arr_for_calculations, axis=0)
  x_range = np.arange(1, img_arr_for_calculations.shape[1] + 1)
  
  y_profiles = np.sum(img_arr_for_calculations, axis=1)
  y_range = np.arange(1, img_arr_for_calculations.shape[0] + 1)
  
  return {
    'x_profiles': x_profiles,
    'x_range': x_range,
    'y_profiles': y_profiles,
    'y_range': y_range
  }

def write_profile(img, letter_path, type='x'):
  profiles = get_profiles(img)
  
  if type == 'x':
    plt.bar(x=profiles['x_range'], height=profiles['x_profiles'], width=0.85)
    plt.ylim(0, max(profiles['x_profiles']))
    plt.xlim(0, max(profiles['x_range']))

  else:
    plt.barh(y=profiles['y_range'], width=profiles['y_profiles'], height=0.85)
    plt.ylim(max(profiles['y_range']), 0 )
    plt.xlim(0, max(profiles['y_profiles']))


  plt.savefig(letter_path)
  plt.clf()

# сохраняем значения характеристик в файлики
def features_save(alphabet):
  with open('lower_russian_font_features.csv', 'w', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['letter', 'weight', 'rel_weight',
                         'x_avg', 'y_avg', 'rel_x_avg', 'rel_y_avg', 
                         'inertia_x', 'inertia_y', 'rel_inertia_x', 'rel_inertia_y'])
    writer.writeheader()

    for letter in alphabet:
      image = Image.open(f'letter_images/letter_{letter}.png')
      
      features = get_features(image)
      features['letter'] = letter
      
      writer.writerow(features)

# сохраняем значения профилей в файлики
def profile_save(alphabet):
  for letter in alphabet:
    image = Image.open(f'letter_images/letter_{letter}.png')
    letter_x_profile_save_path = f'letter_profiles/letter_{letter}_x_profile.png'
    write_profile(image, letter_x_profile_save_path, 'x')
    letter_y_profile_save_path = f'letter_profiles/letter_{letter}_y_profile.png'
    write_profile(image, letter_y_profile_save_path, 'y')
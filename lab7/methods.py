from PIL import Image, ImageFont, ImageDraw, ImageOps
import numpy as np
from matplotlib import pyplot as plt
import csv
from operator import itemgetter

# бинаризуем изображение
def simple_binarization(image, threshold):
  img_arr = np.array(image)
  new_image = np.zeros(shape=img_arr.shape)
  new_image[img_arr > threshold] = 255
  return Image.fromarray(new_image.astype(np.uint8), 'L')

# вырезаем белые места из изображения буквы
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

# генерируем фразу и сохраняем в картинку
def generate_sentence(font_size, txt = 'я люблю оави'):
  font = ImageFont.truetype("../common/fonts/tnr_regular.ttf", font_size)
  img = Image.new(mode="L", size=(2555, font_size), color=255)
  draw = ImageDraw.Draw(img, mode = 'L')
  draw.text(xy=(0, 0), text= txt, fill=0, font=font, anchor = 'lt')
  cutted_img = cut_empty_rows_and_cols(img) # cut_white_image_parts(img)
  result_img = simple_binarization(cutted_img, 100)
  result_img.save(f'font_{font_size}_test.png')
  return result_img 

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
  
  # 'rel_weight' 'rel_x_avg' 'rel_y_avg' 'rel_inertia_x' 'rel_inertia_y'
  return (rel_weight, rel_x_avg, rel_y_avg, rel_inertia_x, rel_inertia_y)

def color_used_arr(img):
  return np.asarray(np.asarray(img) < 1, dtype = np.int0)

# сегментируем фразу на отдельные буквы
def get_segments_list(img):
  img_arr_for_calculations = color_used_arr(img)
  x_profiles = np.sum(img_arr_for_calculations, axis=0)
  x_profiles[0] = 0
  lst = []
  new_lst = []
  for i in range(len(x_profiles)):
    if x_profiles[i] == 0:
      lst.append(i)
  lst.append(img.width)

  for i in range(len(lst)-1):
    if lst[i] + 1 != lst[i+1]:
      new_lst.append(lst[i])
      new_lst.append(lst[i+1])
  new_lst.append(img.width-1)
  new_lst = sorted(list(set(new_lst)))
  
  segments = []
  for i in range(0, len(new_lst)-1, 2):
    segments.append((new_lst[i], new_lst[i+1]))
  return segments
    
def get_letter_images(image):
  letter_images_list = []
  
  segments = get_segments_list(image)
  
  for segment in segments:
    letter_image = image.crop(box=(segment[0], 0, segment[1]+1, image.height))
    cutted_letter_image = cut_empty_rows_and_cols(letter_image)
    
    letter_images_list.append(cutted_letter_image)
  return letter_images_list

def get_probability_list(img, reference_letter_list, reference_letter_features_list):
  letter_images_list = get_letter_images(img)
  full_list = []

  for i, letter in enumerate(letter_images_list):
    # получаем профиль данной буквы
    recognized_letter_features = get_features(letter)
    euclid_distances = []

    for ind, ref_letter in enumerate(reference_letter_list):
      zipped_features = zip(recognized_letter_features, reference_letter_features_list[ind])
      euclid_distance = 0

      # считаем дистанцию
      for el in zipped_features:
        euclid_distance += (el[0] - el[1]) ** 2
      euclid_distance = euclid_distance ** 0.5
      euclid_distances.append([ref_letter, euclid_distance])

    # сортируем и находим ближайшее подходящее
    euclid_distances = sorted(euclid_distances, key = itemgetter(1))
    max_dist = max(euclid_distances, key = itemgetter(1))[1]

    for n in range(len(euclid_distances)):
      euclid_distances[n][1] /= max_dist
      euclid_distances[n][1] = round(1 - euclid_distances[n][1], 2)
      euclid_distances[n] = tuple(euclid_distances[n])

    full_list.append((i + 1, euclid_distances))
    print(euclid_distances[:5])
  return full_list


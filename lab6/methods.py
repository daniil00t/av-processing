from PIL import Image, ImageFont, ImageDraw, ImageOps
import numpy as np
from matplotlib import pyplot as plt
import csv

def getAlphabet(string):
  alphabet = []
  for letter in string:
    alphabet.append(letter)

  return alphabet

def simple_binarization(image, threshold):
  img_arr = np.array(image)
  new_image = np.zeros(shape=img_arr.shape)
  new_image[img_arr > threshold] = 255

  return Image.fromarray(new_image.astype(np.uint8), 'L')

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

def color_used_arr(img):
  return np.asarray(np.asarray(img) < 1, dtype = np.int0)

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

def show_profiles_x(img):
  profiles = get_profiles(img)
  plt.figure(figsize=(12,2))
  plt.bar(x=profiles['x_range'], height=profiles['x_profiles'], width=0.85)
  plt.ylim(0, max(profiles['x_profiles']))
  plt.xlim(0, max(profiles['x_range']))
  plt.show()

def show_profiles_y(img):
  profiles = get_profiles(img)
  plt.figure(figsize=(12,2))
  plt.barh(y=profiles['y_range'], width=profiles['y_profiles'], height=0.85)
  plt.ylim(max(profiles['y_range']), 0 ) #img.size[1], 0)
  plt.xlim(0, max(profiles['y_profiles']))
  plt.show()

def get_segments_list(img):
  img_arr_for_calculations = color_used_arr(img)
  x_profiles = np.sum(img_arr_for_calculations, axis=0)
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

def result_draw(image, segments):
  left_color = (124,252,0)
  right_color = (160,32,240)
  result = image.copy().convert('RGB')
  result_draw = ImageDraw.Draw(im=result)
  for segment in segments:
    result_draw.rectangle(xy=[(segment[0], 0), (segment[0], result.height)], fill=left_color)
    result_draw.rectangle(xy=[(segment[1], 0), (segment[1], result.height)], fill=right_color)
  return result


font_size = 52
font = ImageFont.truetype("fonts/tnr_regular.ttf", font_size)


def generate_sentence():
  img = Image.new(mode="L", size=(2555, 150), color="white")
  draw = ImageDraw.Draw(img, mode = 'L')
  draw.text(xy=(0, 0), text='СВЕРХЗВУКОВОЙ ИСТРЕБИТЕЛЬ', fill=0, font=font, anchor = 'lt')
  cutted_img = cut_empty_rows_and_cols(img) #cut_white_image_parts(img)
  simple_binarization(cutted_img, 100).save('font_52_test.png')
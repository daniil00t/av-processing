from PIL import Image
import numpy as np

# вариант: 10

def calculate_template_space(temp_side_length):
  return int(temp_side_length/2)

def median_filter(image, template_side_length):
  new_image = np.zeros(image.shape, image.dtype)

  # Coordinates are provided as (y,x), where the origin is at the top left of the image
  # So always remember that (-) is used instead of (+) to iterate
  template_space = calculate_template_space(template_side_length)
  template = []
  half_template = int((template_side_length-1)/2)

  for x in range(template_space, new_image.shape[1] - template_space):
    a = x + half_template
    for y in range(template_space, new_image.shape[0] - template_space):
      b = y + half_template

      # a and b basically imply that from any center point always start iterating at the top left of the template
      # Iteration:
      for c in range(0, template_side_length):
        for d in range(0, template_side_length):
          template.append(image[b - d, a - c])
      template.sort()
      new_image[y, x] = template[int((int(math.pow(template_side_length, 2)) - 1) / 2)]
      template = []
  return new_image

def erosion(image, template_side_length, template):
  new_image = np.zeros(image.shape, image.dtype)

  # Coordinates are provided as (y,x), where the origin is at the top left of the image
  # So always remember that (-) is used instead of (+) to iterate
  template_space = calculate_template_space(template_side_length)
  half_template = int((template_side_length - 1) / 2)

  for x in range(template_space, new_image.shape[1] - template_space):
    for y in range(template_space, new_image.shape[0] - template_space):
      minimum = 256
      for c in range(0, template_side_length):
        for d in range(0, template_side_length):
          a = x - half_template - 1 + c
          b = y - half_template - 1 + d
          sub = image[b, a] - template[d, c]
          if sub < minimum:
            if sub > 0:
              minimum = sub
      new_image[y, x] = int(minimum)
  return new_image

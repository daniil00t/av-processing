from PIL import Image, ImageFilter, ImageChops
from time import time_ns
import math
from main import erosion

def getImages():
  img_main = Image.open('images/in/neuro_binary.png', 'r').convert('RGB')
  img_neuro_grayscale = Image.open('images/in/neuro_grayscale.png', 'r').convert('RGB')
  img_random_forms = Image.open('images/in/random_forms.png', 'r').convert('RGB')

  return {'binary': img_main, 'grayscale': img_neuro_grayscale, 'img_random_forms': img_random_forms}

def printAudit(test_name, delta_time, audit):
  print(f'\nTest {test_name} passed: {(delta_time) / math.pow(10, 9)}s')
  for i in audit:
    name = i.get('name')
    input_size = i.get('input_size')
    output_size = i.get('output_size')
    print(f'Image {name}; input_size: {input_size}; output_size: {output_size}')


def erosion_test(iterations: int, template_n: int):
  images = getImages()

  start_time = time_ns()
  audit = []
  for (image_name, image) in images.items():
    newImage = image
    for i in range(iterations):
      newImage = newImage.filter(ImageFilter.MinFilter(template_n))

    output_name = f'images/out/{image_name}.processed.png'
    diff_name = f'images/out/{image_name}.diff.png'

    audit.append({
      'name': output_name,
      'input_size': f'{image.size[0]}x{image.size[1]}',
      'output_size': f'{newImage.size[0]}x{newImage.size[1]}'
    })
    diff_image = ImageChops.difference(newImage, image)
    newImage.save(output_name)
    diff_image.save(diff_name)

  end_time = time_ns()
  printAudit('mean_grayscale', end_time - start_time, audit)

def test():
  erosion_test(3, 3)

if __name__ == '__main__':
  test()
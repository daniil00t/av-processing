from PIL import Image
from time import time_ns
import math
from main import mean_grayscale, photoshop_grayscale, two_threshold_binarize

def getImages():
  img_main = Image.open('images/in/mob.png', 'r').convert('RGB')
  img_nogame = Image.open('images/in/nogame.png', 'r').convert('RGB')
  img_rentgen = Image.open('images/in/rentgen.png', 'r').convert('RGB')
  img_circles = Image.open('images/in/circles.png', 'r').convert('RGB')
  img_forms = Image.open('images/in/forms.png', 'r').convert('RGB')

  return {'main': img_main, 'img_big': img_nogame, 'img_rentgen': img_rentgen, 'circles': img_circles, 'forms': img_forms}

def printAudit(test_name, delta_time, audit):
  print(f'\nTest {test_name} passed: {(delta_time) / math.pow(10, 9)}s')
  for i in audit:
    name = i.get('name')
    input_size = i.get('input_size')
    output_size = i.get('output_size')
    print(f'Image {name}; input_size: {input_size}; output_size: {output_size}')

def mean_grayscale_test():
  images = getImages()

  start_time = time_ns()
  audit = []
  for (image_name, image) in images.items():
    newImage = mean_grayscale(image)
    output_name = f'images/out/mean_grayscale/{image_name}.processed.png'
    audit.append({
      'name': output_name,
      'input_size': f'{image.size[0]}x{image.size[1]}',
      'output_size': f'{newImage.size[0]}x{newImage.size[1]}'
    })
    newImage.save(output_name)

  end_time = time_ns()
  printAudit('mean_grayscale', end_time - start_time, audit)

def photoshop_grayscale_test():
  images = getImages()

  start_time = time_ns()
  audit = []
  for (image_name, image) in images.items():
    newImage = photoshop_grayscale(image)
    output_name = f'images/out/photoshop_grayscale/{image_name}.processed.png'
    audit.append({
      'name': output_name,
      'input_size': f'{image.size[0]}x{image.size[1]}',
      'output_size': f'{newImage.size[0]}x{newImage.size[1]}'
    })
    newImage.save(output_name)

  end_time = time_ns()
  printAudit('photoshop_grayscale', end_time - start_time, audit)

def two_threshold_binarize_test():
  images = getImages()


  start_time = time_ns()
  audit = []
  for (image_name, image) in images.items():
    # newImage = two_threshold_binarize(image, 150, 200)
    newImage = two_threshold_binarize(image, 10, 200, reverse=True)
    output_name = f'images/out/two_threshold_binarize/{image_name}.processed.png'
    audit.append({
      'name': output_name,
      'input_size': f'{image.size[0]}x{image.size[1]}',
      'output_size': f'{newImage.size[0]}x{newImage.size[1]}'
    })
    newImage.save(output_name)

  end_time = time_ns()
  printAudit('two_threshold_binarize', end_time - start_time, audit)


def main():
  # mean_grayscale_test()
  photoshop_grayscale_test()
  two_threshold_binarize_test()

if __name__ == '__main__':
  main()
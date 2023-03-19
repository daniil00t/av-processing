from PIL import Image
from time import time_ns
import math
from main import upsampling, downsampling, resampling, one_resampling

def getImages():
  img_main = Image.open('images/main.png', 'r').convert('RGB')
  img_big = Image.open('images/big.png', 'r').convert('RGB')
  img_biggest = Image.open('images/biggest.png', 'r').convert('RGB')
  img_gigachad = Image.open('images/gigachad.png', 'r').convert('RGB')

  return {'main': img_main, 'img_big': img_big, 'img_biggest': img_biggest, 'img_gigachad': img_gigachad}
  # return {'main': img_main}

def printAudit(test_name, delta_time, audit):
  print(f'\nTest {test_name} passed: {(delta_time) / math.pow(10, 9)}s')
  for i in audit:
    name = i.get('name')
    input_size = i.get('input_size')
    output_size = i.get('output_size')
    print(f'Image {name}; input_size: {input_size}; output_size: {output_size}')

def upsampling_test():
  images = getImages()
  n = 5

  start_time = time_ns()
  audit = []
  for (image_name, image) in images.items():
    newImage = upsampling(image, n)
    output_name = f'images/upsampling/{image_name}.processed.png'
    audit.append({
      'name': output_name,
      'input_size': f'{image.size[0]}x{image.size[1]}',
      'output_size': f'{newImage.size[0]}x{newImage.size[1]}'
    })
    newImage.save(output_name)

  end_time = time_ns()
  printAudit('upsampling_test', end_time - start_time, audit)

def downsampling_test():
  images = getImages()
  n = 5

  start_time = time_ns()
  audit = []
  for (image_name, image) in images.items():
    newImage = downsampling(image, n)
    output_name = f'images/downsampling/{image_name}.processed.png'
    audit.append({
      'name': output_name,
      'input_size': f'{image.size[0]}x{image.size[1]}',
      'output_size': f'{newImage.size[0]}x{newImage.size[1]}'
    })
    newImage.save(output_name)

  end_time = time_ns()
  printAudit('downsampling_test', end_time - start_time, audit)

def resampling_test():
  images = getImages()
  n = 3
  m = 7

  start_time = time_ns()
  audit = []
  for (image_name, image) in images.items():
    newImage = resampling(image, n, m)
    output_name = f'images/resampling/{image_name}.processed.png'
    audit.append({
      'name': output_name,
      'input_size': f'{image.size[0]}x{image.size[1]}',
      'output_size': f'{newImage.size[0]}x{newImage.size[1]}'
    })
    newImage.save(output_name)

  end_time = time_ns()
  printAudit('resampling_test', end_time - start_time, audit)

def one_resampling_test():
  images = getImages()
  n = 64 / 235

  start_time = time_ns()
  audit = []
  for (image_name, image) in images.items():
    newImage = one_resampling(image, n)
    output_name = f'images/one_resampling/{image_name}.processed.png'
    audit.append({
      'name': output_name,
      'input_size': f'{image.size[0]}x{image.size[1]}',
      'output_size': f'{newImage.size[0]}x{newImage.size[1]}'
    })
    newImage.save(output_name)

  end_time = time_ns()
  printAudit('one_resampling_test', end_time - start_time, audit)


def main():
  upsampling_test()
  downsampling_test()
  resampling_test()
  one_resampling_test()


if __name__ == '__main__':
  main()
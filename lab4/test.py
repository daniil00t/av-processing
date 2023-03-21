from PIL import Image
from time import time_ns
import math
from main import photoshop_grayscale, contour_selection, operator_roberts_x, operator_roberts_y

def getImages():
  img_tangero = Image.open('images/in/tangero.png', 'r').convert('RGB')
  img_saitama = Image.open('images/in/saitama.png', 'r').convert('RGB')
  img_sun = Image.open('images/in/sun.png', 'r').convert('RGB')

  return {'tangero': img_tangero, 'saitama': img_saitama, 'img_sun': img_sun}

def printAudit(test_name, delta_time, audit):
  print(f'\nTest {test_name} passed: {(delta_time) / math.pow(10, 9)}s')
  for i in audit:
    name = i.get('name')
    input_size = i.get('input_size')
    output_size = i.get('output_size')
    print(f'Image {name}; input_size: {input_size}; output_size: {output_size}')

def contour_selection_test(operator_x, operator_y, window_size: int):
  images = getImages()

  start_time = time_ns()
  audit = []
  for (image_name, image) in images.items():
    grayscale_image = photoshop_grayscale(image)
    g_x_img, g_y_img, g_img, binary_img = contour_selection(grayscale_image, operator_x, operator_y, window_size)

    output_name_x = f'images/out/{image_name}_x.processed.png'
    output_name_y = f'images/out/{image_name}_y.processed.png'
    output_name_binary = f'images/out/{image_name}_binary.processed.png'
    output_name = f'images/out/{image_name}.processed.png'
    output_name_grayscale = f'images/out/{image_name}_grayscale.processed.png'

    audit.append({
      'name': output_name_x,
      'input_size': f'{image.size[0]}x{image.size[1]}',
      'output_size': f'{g_x_img.size[0]}x{g_x_img.size[1]}'
    })
    audit.append({
      'name': output_name_y,
      'input_size': f'{image.size[0]}x{image.size[1]}',
      'output_size': f'{g_y_img.size[0]}x{g_y_img.size[1]}'
    })
    audit.append({
      'name': output_name,
      'input_size': f'{image.size[0]}x{image.size[1]}',
      'output_size': f'{g_img.size[0]}x{g_img.size[1]}'
    })
    audit.append({
      'name': output_name_binary,
      'input_size': f'{image.size[0]}x{image.size[1]}',
      'output_size': f'{binary_img.size[0]}x{binary_img.size[1]}'
    })

    g_x_img.save(output_name_x)
    g_y_img.save(output_name_y)
    g_img.save(output_name)
    binary_img.save(output_name_binary)
    grayscale_image.save(output_name_grayscale)

  end_time = time_ns()
  printAudit('contour_selection', end_time - start_time, audit)

def test():
  contour_selection_test(operator_roberts_x, operator_roberts_y, 3)

if __name__ == '__main__':
  test()
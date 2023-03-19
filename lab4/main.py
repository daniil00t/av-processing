from PIL import Image
import numpy as np

def photoshop_grayscale(image):
  result = Image.new('L', (image.width, image.height))

  for x in range(result.width):
    for y in range(result.height):
      pixel = image.getpixel((x, y))
      new_pixel = int(round(pixel[0] * 0.3 + pixel[1] * 0.59 + pixel[2] * 0.11))
      result.putpixel((x, y), new_pixel)

  return result

operator_roberts_x = np.array([[ 0, 0, 0], 
                              [0, -1, 0],
                              [ 0, 0, 1]])
operator_roberts_y = np.array([[ 0, 0, 0], 
                              [ 0, 0, -1],
                              [ 0, 1, 0]])

def contour_selection(image, operator_x, operator_y, window_size):
  width, height = image.size
  
  gray_arr = np.asarray(image, dtype=np.uint8)
  
  G_x_matrix = np.zeros(shape=(height, width))
  G_y_matrix = np.zeros(shape=(height, width))
  G_matrix = np.zeros(shape=(height, width))
  
  padded_gray_arr = np.pad(gray_arr, ((1, 1), (1, 1)), mode='constant') 
  for i in range(1, height+1): 
    for j in range(1, width+1): 
      i_min = max(i - window_size // 2, 0)
      i_max = min(i + window_size // 2, height+1)
      j_min = max(j - window_size // 2, 0)
      j_max = min(j + window_size // 2, width+1)
      
      window_matrix = padded_gray_arr[i_min:i_max+1, j_min:j_max+1]
      
      G_x = np.sum(operator_x * window_matrix)
      G_y = np.sum(operator_y * window_matrix)
      G = np.abs(G_x) + np.abs(G_y)

      G_x_matrix[i-1, j-1] = int(round(G_x))
      G_y_matrix[i-1, j-1] = int(round(G_y))
      G_matrix[i-1, j-1] = int(round(G))
        
  G_x_matrix_normalized = np.abs(G_x_matrix / np.max(G_x_matrix) * 255)
  G_y_matrix_normalized = np.abs(G_y_matrix / np.max(G_y_matrix) * 255)
  G_matrix_normalized = G_matrix / np.max(G_matrix) * 255
  
  t = np.mean(G_matrix_normalized) * 2.5

  g_x_img = Image.fromarray(G_x_matrix_normalized.astype(np.uint8), mode='L')
  g_y_img = Image.fromarray(G_y_matrix_normalized.astype(np.uint8), mode='L')
  g_img = Image.fromarray(G_matrix_normalized.astype(np.uint8), mode='L')
  binary_img = Image.fromarray((G_matrix_normalized > t).astype(np.uint8) * 255, mode = 'L')

  return g_x_img, g_y_img, g_img, binary_img
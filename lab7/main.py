from methods import *

# получаем профили из 5 лабы
with open('../lab5/lower_russian_font_features.csv', 'r', encoding='utf-8') as f:
  reader = csv.DictReader(f, fieldnames=['letter', 'weight', 'rel_weight',
                                        'x_avg', 'y_avg', 'rel_x_avg', 'rel_y_avg', 
                                        'inertia_x', 'inertia_y', 'rel_inertia_x', 'rel_inertia_y'])
  next(reader)
  reference_letter_list = []
  reference_letter_features_list = []
  for row in reader:
    reference_letter_list.append(row['letter'])
    reference_letter_features_list.append((float(row['rel_weight']), float(row['rel_x_avg']), float(row['rel_y_avg']), 
                                          float(row['rel_inertia_x']), float(row['rel_inertia_y'])))
    

# генерируем текст 120 шрифтом
phrase_some_size = generate_sentence(120, 'я люблю оави')

# пытаемся распознать
euclid_distances_some_size = get_probability_list(phrase_some_size, reference_letter_list, reference_letter_features_list)

recognized_text = ''
for el in euclid_distances_some_size:
  recognized_text += el[1][0][0]
print(recognized_text)

with open('recognize_result.txt', 'w', encoding='utf-8') as f:
  for row in euclid_distances_some_size:
    f.write(f"{row}\n")
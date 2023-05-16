from methods import *

generate_sentence('я люблю оави')

font_52_test_img = Image.open('font_52_test.png')

segments = get_segments_list(font_52_test_img)

print(segments)

result = result_draw(font_52_test_img, segments)
result.save('result_font_52.png')
print(result)

show_profiles_x(font_52_test_img)

show_profiles_y(font_52_test_img)
from PIL import Image
from PIL import ImageEnhance
import matplotlib.pyplot as plt

# 原始图像
image = Image.open('Interview-question-collection/picture/1.jpg')  # 打开图片
# image.show()
plt.figure("origan_image")
plt.imshow(image)
plt.show()

# 亮度增强
enh_bri = ImageEnhance.Brightness(image)
brightness = 1.5
image_brightened = enh_bri.enhance(brightness)
# image_brightened.show()
plt.figure("brightened")
plt.imshow(image_brightened)
plt.show()
image_brightened.save('Interview-question-collection/picture/image_brightened.jpg')

# 色度增强
enh_col = ImageEnhance.Color(image)
color = 1.5
image_colored = enh_col.enhance(color)
# image_colored.show()
plt.figure("colored")
plt.imshow(image_colored)
plt.show()
image_colored.save('Interview-question-collection/picture/image_colored.jpg')

# 对比度增强
enh_con = ImageEnhance.Contrast(image)
contrast = 1.5
image_contrasted = enh_con.enhance(contrast)
# image_contrasted.show()
plt.figure("contrast")
plt.imshow(image_contrasted)
plt.show()
image_contrasted.save('Interview-question-collection/picture/image_contrasted.jpg')

# 锐度增强
enh_sha = ImageEnhance.Sharpness(image)
sharpness = 1.5
image_sharped = enh_sha.enhance(sharpness)
# image_sharped.show()
plt.figure("sharpness")
plt.imshow(image_sharped)
plt.show()
image_sharped.save('Interview-question-collection/picture/image_sharped.jpg')

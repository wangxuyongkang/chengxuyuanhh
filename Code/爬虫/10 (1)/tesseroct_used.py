import pytesseract
from PIL import Image
#pip3 install pytesseract
#pip3 install pillow
# image1 = Image.open('01.jpg')
# result = pytesseract.image_to_string(image1)

# image2 = Image.open('02.jpg')
# result = pytesseract.image_to_string(image2)

# image3 = Image.open('03.jpg')
# result = pytesseract.image_to_string(image3)
#antispam_v2

# image3 = Image.open('antispam_v2.jpeg')
# result = pytesseract.image_to_string(image3)

# print(result)

#图片的灰度处理

img = Image.open('antispam_v2.jpeg')
#对图片进行会读处理
l_img = img.convert('L')
l_img.save('l_img.jpg')
#对图片进行二值化处理
#设置阀值
num = 180
data = []
for i in range(0,256):
    if i < num:
        data.append(0)
    else:
        data.append(1)

n_img = l_img.point(data,'1')
n_img.save('n_img.jpg')

result = pytesseract.image_to_string(n_img)

print(result)




import pytesseract
from PIL import Image, ImageEnhance

def sharpen_image(image):
    enhancer = ImageEnhance.Sharpness(image)
    sharpened_image = enhancer.enhance(3.0)
    return sharpened_image

def image_rotated(image):
    rotated_image = image.rotate(270, expand=True)
    return rotated_image

def ocr_with_array_per_word(image_path):
    try:
        image = Image.open(image_path)
    except IOError:
        print("Unable to open image file")
        return []

    sharpened_image = sharpen_image(image)
    rotated_image = image_rotated(sharpened_image)

    try:
        text = pytesseract.image_to_string(rotated_image, lang='eng')
        word_array = text.split()
        return word_array
    except pytesseract.TesseractError:
        print("Error during OCR processing")
        return []

image_path = 'D:/KP_GIN/FILE 1/ConvertedImages/PDF1_2.jpg' 
words = ocr_with_array_per_word(image_path)
for word in words:
    print(word)
noak_index = words.index("By") - 1
if noak_index < len(words):
    selected_word = words[noak_index]
    print("Berdasarkan Akta Kematian Nomor ",selected_word)
sleman_index = words.index("banwe")+ 2
if sleman_index < len(words):
    selected_word = words[sleman_index]
    print("bahwa di ",selected_word)
tanggal_index = words.index("padeianggal")+ 1
if tanggal_index < len(words):
    selected_word = words[tanggal_index]+' '+words[tanggal_index+1]+' '+words[tanggal_index+2]
tahun_index = words.index("tahun")+1
if tahun_index < len(words):
    selected_word = words[tahun_index]+' '+words[tahun_index+1]+' '+words[tahun_index+2]+' '+words[tahun_index+3]+' '+words[tahun_index+4]
    print("tahun ",selected_word)
nama_index = words.index("Tn/Nv/Nn") + 1
if nama_index < len(words):
    selected_word = words[nama_index]
    print("telah meninggal dunia seorang bernama Tn/Ny/Nn ",selected_word)
lahir_index = words.index("lahirdi") + 1
if lahir_index < len(words):
    selected_word = words[lahir_index]
    print("lahir di ",selected_word)
tanggaldead_index = words.index("padaianggal")+1
if tanggaldead_index < len(words):
    selected_word = words[tanggaldead_index]+' '+words[tanggaldead_index+1]+' '+words[tanggaldead_index+8]
    print("tanggal ",selected_word)

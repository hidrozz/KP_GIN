import pytesseract
from PIL import Image, ImageEnhance

def sharpen_image(image):
    enhancer = ImageEnhance.Sharpness(image)
    sharpened_image = enhancer.enhance(3.0)
    return sharpened_image

def image_rotated(image):
    rotated_image = image.rotate(268, expand=True)
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

image_path = 'D:/KP_GIN/FILE 1/ConvertedImages/PDF1_4.jpg' 
words = ocr_with_array_per_word(image_path)
for word in words:
    print(word)
judul_index = words.index("FORMULIR")
if judul_index < len(words):
    selected_word = words[judul_index] +' '+ words[judul_index + 1] +" "+ words[judul_index + 2]
    print(selected_word)
# noak_index = words.index("°") + 1
# if noak_index < len(words):
#     selected_word = words[noak_index]
#     print("Nomor Akta =",selected_word)
# pekerjaan_index = words.index("PETANUPEKEBUN") + 1
# if pekerjaan_index < len(words):
#     words[pekerjaan_index]="PETANI"
#     words[pekerjaan_index + 1]="PEKEBUN"
#     selected_word = ' '.join(words[pekerjaan_index:pekerjaan_index+2])
#     print("Pekerjaan =",selected_word)
# alamt_index = words.index("terakhir") + 1
# if alamt_index < len(words):
#     selected_word = words[alamt_index]
#     print("Alamat Terakhir =",selected_word)
# klurahan_index = words.index("Kelurahan/Desa") + 1
# if klurahan_index < len(words):
#     selected_word = words[klurahan_index]
#     print("Kelurahan/Desa =",selected_word)
# kcmatan_index = words.index("Kecamaian") + 1
# if kcmatan_index < len(words):
#     selected_word = words[kcmatan_index]
#     print("Kecamatan =",selected_word)
# kota_index = words.index("Kabupaten/Kota") + 1
# if kota_index < len(words):
#     selected_word = words[kota_index]
#     print("Kabupaten/Kota =",selected_word)
# provinsi_index = words.index("Provinsi") + 1
# if provinsi_index < len(words):
#     selected_word = words[provinsi_index]+' '+ words[provinsi_index + 1]+' '+ words[provinsi_index + 2]
#     print("Provinsi =",selected_word)
# ibu_index = words.index("bernamae") + 1
# if ibu_index < len(words):
#     selected_word = words[ibu_index]
#     print("Nama Ibu =",selected_word)
# saksi1_index = words.index("SUHARMIYATI")
# if saksi1_index < len(words):
#     selected_word = words[saksi1_index]
#     print("Saksi 1 =",selected_word)
# saksi2_index = words.index("IRMAWAT!")
# if saksi2_index < len(words):
#     words[saksi2_index] ="IRMAWATI"
#     selected_word = ' '.join(words[saksi2_index:saksi2_index+1])
#     print("Saksi 2 =",selected_word)
# pelapor_index = words.index("bernamea") + 1
# if pelapor_index < len(words):
#     selected_word = words[pelapor_index]
#     print("pelapor =",selected_word)
# pejabat_index = words.index("saya") + 1
# if pejabat_index < len(words):
#     selected_word = words[pejabat_index]+' '+ words[pejabat_index + 1]+' '+ words[pejabat_index + 2]+' '+ words[pejabat_index + 3]
#     print("Pejabat Pencatatan Sipil Sleman =",selected_word)
     
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

image_path = 'D:/KP_GIN/FILE 2/ConvertedImages/PDF2_1.jpg' 
words = ocr_with_array_per_word(image_path)
# for word in words:
#     print(word)
nama_index = words.index("meninggal") + 4
if nama_index < len(words):
    words[nama_index] = "BOINEM"
    words[nama_index + 1] = "SUYOTO"
    words[nama_index + 2] = "KAHONO"
selected_word = ' '.join(words[nama_index:nama_index+3])
print("Nama =", selected_word)
nik_index = words.index("NIK") + 2
if nik_index < len(words):
    selected_word = words[nik_index]+''+ words[nik_index + 1]
    print("NIK =",selected_word)
noak_index = words.index("NOMORAKTA") + 2
if noak_index < len(words):
    selected_word = words[noak_index]+''+ words[noak_index + 1]
    print("Nomor Akta =",selected_word)
pelapor_index = words.index("pelapor") + 2
if pelapor_index < len(words):
    selected_word = words[pelapor_index]+' '+ words[pelapor_index + 1]
    print("Pelapor =",selected_word)
pekerjaan_index = words.index("PETANUPEKEBUN") + 1
if pekerjaan_index < len(words):
    words[pekerjaan_index]="PETANI"
    words[pekerjaan_index + 1]="PEKEBUN"
    selected_word = ' '.join(words[pekerjaan_index:pekerjaan_index+2])
    print("Pekerjaan =",selected_word)
alamt_index = words.index("terakhir") + 1
if alamt_index < len(words):
    selected_word = words[alamt_index]
    print("Alamat Terakhir =",selected_word)
klurahan_index = words.index("Kelurahan/Desa") + 1
if klurahan_index < len(words):
    selected_word = words[klurahan_index]
    print("Kelurahan/Desa =",selected_word)
kcmatan_index = words.index("Kecamatan") + 1
if kcmatan_index < len(words):
    selected_word = words[kcmatan_index]
    print("Kecamatan =",selected_word)
kota_index = words.index("Xabupaten/Kote") + 1
if kota_index < len(words):
    selected_word = words[kota_index]
    print("Kabupaten/Kota =",selected_word)
provinsi_index = words.index("Provinsi") + 1
if provinsi_index < len(words):
    selected_word = words[provinsi_index]+' '+ words[provinsi_index + 1]+' '+ words[provinsi_index + 2]
    print("Provinsi =",selected_word)
ibu_index = words.index("Kandung") + 2
if ibu_index < len(words):
    selected_word = words[ibu_index]+' '+ words[ibu_index + 1]+' '+ words[ibu_index + 2]
    print("Nama Ibu =",selected_word)
saksi1_index = words.index("disaksikan") + 4
if pekerjaan_index < len(words):
    words[saksi1_index]="YUNITA"
    words[saksi1_index + 1]="SARI"
    words[saksi1_index + 2]="WIDAYANTI"
    selected_word = words[saksi1_index]+' '+ words[saksi1_index + 1]+' '+ words[saksi1_index + 2]
    print("Saksi 1 =",selected_word)
saksi2_index = words.index("uMuUr") - 3
if saksi2_index < len(words):
    selected_word = words[saksi2_index]+' '+ words[saksi2_index + 1]+' '+ words[saksi2_index + 2]
    print("Saksi 2 =",selected_word)
# saksi2_index = words.index("IRMAWAT!")
# if saksi2_index < len(words):
#     selected_word = words[saksi2_index]
#     print("Saksi 2 =",selected_word)
# # pelapor_index = words.index("bernamea") + 1
# # if pelapor_index < len(words):
# #     selected_word = words[pelapor_index]
# #     print("pelapor =",selected_word)
pejabat_index = words.index("saya") + 1
if pejabat_index < len(words):
    selected_word = words[pejabat_index]+' '+ words[pejabat_index + 1]+' '+ words[pejabat_index + 2]+' '+ words[pejabat_index + 3]
    print("Pejabat Pencatatan Sipil Sleman =",selected_word)
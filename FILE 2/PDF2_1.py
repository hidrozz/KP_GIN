from PIL import Image, ImageEnhance
import pytesseract
import openpyxl
import tkinter as tk
from tkinter import messagebox
import os
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
source_directory = os.path.dirname(image_path)
workbook = openpyxl.Workbook()
sheet = workbook.active


headers = ["Field", "Value"]
sheet.append(headers)

def add_data_to_excel(field, value):
    sheet.append([field, value])
# for word in words:
#     print(word)

nama_index = words.index("meninggal") + 4
if nama_index < len(words):
    words[nama_index] = "BOINEM"
    words[nama_index + 1] = "SUYOTO"
    words[nama_index + 2] = "KAHONO"
    selected_word = ' '.join(words[nama_index:nama_index+3])
    print("Nama =", selected_word)
    add_data_to_excel("Nama", selected_word)
nik_index = words.index("NIK") + 2
if nik_index < len(words):
    selected_word = words[nik_index]+''+ words[nik_index + 1]
    print("NIK =",selected_word)
    add_data_to_excel("NIK", selected_word)
excel_directory = os.path.join(source_directory, 'Excel')
os.makedirs(excel_directory, exist_ok=True)
# Simpan
excel_file_path = os.path.join(excel_directory, 'PDF2.xlsx')

# Save the Excel file
workbook.save(excel_file_path)

# Display success alert
root = tk.Tk()
root.withdraw()
messagebox.showinfo("Success", "Excel file has been exported successfully!")

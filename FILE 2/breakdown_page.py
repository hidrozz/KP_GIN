import os
from pdf2image import convert_from_path

pdf_path = r"D:\KP_GIN\FILE 2\20010616081855.pdf"
output_folder = r"D:\KP_GIN\FILE 2\ConvertedImages"
os.makedirs(output_folder, exist_ok=True)

pages = convert_from_path(pdf_path, dpi=600)

i = 1
for page in pages:
    image_name = "PDF2_" + str(i) + ".jpg"
    image_path = os.path.join(output_folder, image_name)
    page.save(image_path, "JPEG")
    i += 1

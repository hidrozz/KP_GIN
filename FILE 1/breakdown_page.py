import os
from pdf2image import convert_from_path

pdf_path = r"D:\KP_GIN\FILE 1\20010616050717.pdf"
output_folder = r"D:\KP_GIN\FILE 1\ConvertedImages"
os.makedirs(output_folder, exist_ok=True)

pages = convert_from_path(pdf_path, dpi=600)

i = 1
for page in pages:
    image_name = "PDF1_" + str(i) + ".jpg"
    image_path = os.path.join(output_folder, image_name)
    page.save(image_path, "JPEG")
    i += 1

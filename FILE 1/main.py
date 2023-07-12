import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment


# Rest of your code...

# Create a new Excel workbook
workbook = openpyxl.Workbook()
sheet = workbook.active
selected_word = ""

# Write the extracted information to the Excel file
row = 1
sheet['A{}'.format(row)] = "Nama"
sheet['B{}'.format(row)] = selected_word
row += 1

sheet['A{}'.format(row)] = "NIK"
sheet['B{}'.format(row)] = selected_word
row += 1

# Write other extracted information in a similar manner...

# Save the Excel file
workbook.save('output.xlsx')

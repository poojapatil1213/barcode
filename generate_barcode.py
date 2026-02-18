


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.graphics.barcode.code39 import Standard39

# -----------------------------
# VALIDATION FUNCTION
# -----------------------------
def add_validation(series_number_str):
    weighted_list = [8,6,4,2,3,5,9,7]

    if len(series_number_str) != 8:
        raise ValueError("Series number must be exactly 8 digits")

    total = 0
    for i, digit in enumerate(series_number_str):
        total += int(digit) * weighted_list[i]

    remainder = total % 11
    check_digit = 11 - remainder

    if check_digit == 10:
        check_digit = 0
    elif check_digit == 11:
        check_digit = 5

    return str(check_digit)


# -----------------------------
# GENERATE SERIES
# -----------------------------
def generate_series(series_start, prefix, suffix, count):
    barcode_list = []
    number = int(series_start)

    for i in range(count):
        current_number = str(number + i).zfill(8)
        check_digit = add_validation(current_number)
        full_barcode = f"{prefix}{current_number}{check_digit}{suffix}"
        barcode_list.append(full_barcode)

    return barcode_list


# -----------------------------
# USER INPUT
# -----------------------------
series_start = input("Enter 8-digit starting number: ")
prefix = input("Enter prefix: ")
suffix = input("Enter suffix: ")
count = int(input("Enter how many barcodes: "))

barcode_values = generate_series(series_start, prefix, suffix, count)

# -----------------------------
# A4 LABEL SETUP
# -----------------------------
filename = "barcode_labels_A4.pdf"
c = canvas.Canvas(filename, pagesize=A4)

page_width, page_height = A4

# Label grid configuration
cols = 4
rows = 12

left_margin = 8 * mm
top_margin = 10 * mm

label_width = (page_width - 2 * left_margin) / cols
label_height = (page_height - 2 * top_margin) / rows

x = left_margin
y = page_height - top_margin - label_height

label_count = 0

# -----------------------------
# DRAW BARCODES
# -----------------------------
for code in barcode_values:

    # Center barcode inside label
    barcode = Standard39(code, barWidth=0.20*mm, barHeight=9*mm, stop=True)
    barcode_width = barcode.width

    barcode_x = x + (label_width - barcode_width) / 2
    barcode_y = y + (label_height / 2)

    barcode.drawOn(c, barcode_x, barcode_y)

    # Draw text below barcode
    c.setFont("Helvetica", 7)
    c.drawCentredString(x + label_width/2, barcode_y - 5*mm, "*"+code+"*",charSpace=4)

    # Move to next column
    x += label_width
    label_count += 1

    if label_count % cols == 0:
        x = left_margin
        y -= label_height

    if label_count % (cols * rows) == 0:
        c.showPage()
        x = left_margin
        y = page_height - top_margin - label_height

c.save()
print("A4 Barcode Label PDF Generated:", filename)
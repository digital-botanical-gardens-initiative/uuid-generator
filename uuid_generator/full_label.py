import uuid 
from io import BytesIO
import sys
import os

from PIL import Image

from typing import List

import pandas as pd
import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import colors

def generate_uuids(n: int) -> List[str]:
    uuid_list = [str(uuid.uuid4()) for _ in range(n)]
    return uuid_list

def create_big_labels_pdf(values: List[str], output_folder: str) -> None:
    # Splitting the values into groups of 15 (number of labels per page)
    value_groups = [values[i : i + 15] for i in range(0, len(values), 15)]

    # Set up the PDF canvas
    pdf_path = f"{output_folder}/full_labels.pdf"
    pdf = canvas.Canvas(pdf_path, pagesize=A4)

    # Set the margins and box size
    height_margin = 1 * cm
    width_margin = 2.2 * cm
    box_size = 5.54 * cm

    # Set drawing position
    x_position = width_margin
    y_position = height_margin

    draw_qr(value_groups, pdf, x_position, height_margin, box_size, width_margin)
    draw_checks(value_groups, pdf, x_position, height_margin, box_size, width_margin)

    # Save and close the PDF file
    pdf.save()

def draw_qr(value_groups: List[List[str]], pdf: Canvas, x_position: float, height_margin: float, box_size: float, width_margin: float) -> None:
    # Iterate over the value groups
    for group in value_groups:

        draw_lines(pdf, x_position, height_margin, box_size, width_margin)

        # Add the QR code
        for i, value in enumerate(group):
            # Calculate the position for drawing the value and QR code
            pos_x = (width_margin  + (i % 3)* box_size) + 8
            pos_y = (height_margin  + (i // 3) * box_size) + 8

            print(pos_x)

            # Generate QR code
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=5, border=0)
            qr.add_data(value)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")

            # Draw QR code
            qr_img_path = BytesIO()
            qr_img.save(qr_img_path, format="PNG") # type: ignore
            qr_img_path.seek(0)
            image = ImageReader(qr_img_path)
            pdf.drawImage(image, pos_x, pos_y, width=5 * cm, height=5 * cm)

        # Move to the next page
        pdf.showPage()

def draw_checks(value_groups: List[List[str]], pdf: Canvas, x_position: float, height_margin: float, box_size: float, width_margin: float) -> None:
    image = ImageReader("../images/organs_check_box.png")
    # Iterate over the value groups
    for group in value_groups:

        draw_lines(pdf, x_position, height_margin, box_size, width_margin)

        # Add the QR code
        for i, _ in enumerate(group):
            # Calculate the position for drawing the value and QR code
            pos_x = (width_margin  + (i % 3)* box_size) + 8
            pos_y = (height_margin  + (i // 3) * box_size) + 8

            pdf.drawImage(image, pos_x, pos_y, width=5 * cm, height=5 * cm, mask='auto')

        # Move to the next page
        pdf.showPage()

def draw_lines (pdf: Canvas, x_position: float, height_margin: float, box_size: float, width_margin: float) -> None:
    # Set line width
    pdf.setLineWidth(0.3)

    pdf.setStrokeColor(colors.gray)

    # Draw vertical lines
    for i in range(4):
        pdf.line(x_position + i * box_size, height_margin, x_position + i * box_size, 29.7 * cm - height_margin)
    
    # Draw horizontal lines
    for i in range(6):
        pdf.line(x_position, height_margin + i * box_size, 21 * cm - width_margin, height_margin + i * box_size)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python full_label.py <number> <path>")
        sys.exit(1)
    number = sys.argv[1]
    path = sys.argv[2]
    list = generate_uuids(int(number))
    create_big_labels_pdf(list, path)


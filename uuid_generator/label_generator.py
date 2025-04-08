import sys
import uuid
from io import BytesIO

import qrcode
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas


def generate_uuids(n: int) -> list[str]:
    uuid_list = [str(uuid.uuid4()) for _ in range(n)]
    return uuid_list


def create_big_labels_pdf(values: list[str], output_folder: str, uuid_requested: str, organs_requested: str) -> None:
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

    # Iterate over the value groups
    for group in value_groups:
        # Draw QR codes if requested
        if uuid_requested == "y":
            draw_qr(pdf, x_position, height_margin, box_size, width_margin, group)

        # Draw checkboxes if requested
        if organs_requested == "y":
            draw_checks(pdf, x_position, height_margin, box_size, width_margin, group)

    # Save and close the PDF file
    pdf.save()


def draw_qr(
    pdf: Canvas,
    x_position: float,
    height_margin: float,
    box_size: float,
    width_margin: float,
    group: list[str],
) -> None:
    draw_lines(pdf, x_position, height_margin, box_size, width_margin)

    # Add the QR code
    for i, value in enumerate(group):
        # Calculate the position for drawing the value and QR code
        pos_x = (width_margin + (i % 3) * box_size) + 8
        pos_y = (height_margin + (i // 3) * box_size) + 8

        # Generate QR code
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=5, border=0)
        qr.add_data(value)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Draw QR code
        qr_img_path = BytesIO()
        qr_img.save(qr_img_path)
        qr_img_path.seek(0)
        image = ImageReader(qr_img_path)
        pdf.drawImage(image, pos_x, pos_y, width=5 * cm, height=5 * cm)

    # Move to the next page
    pdf.showPage()


def draw_checks(
    pdf: Canvas,
    x_position: float,
    height_margin: float,
    box_size: float,
    width_margin: float,
    group: list[str],
) -> None:
    image = ImageReader("../images/organs_check_box.png")
    draw_lines(pdf, x_position, height_margin, box_size, width_margin)

    # Add the QR code
    for i, _ in enumerate(group):
        # Calculate the position for drawing the value and QR code
        pos_x = (width_margin + (i % 3) * box_size) + 8
        pos_y = (height_margin + (i // 3) * box_size) + 8

        pdf.drawImage(image, pos_x, pos_y, width=5 * cm, height=5 * cm, mask="auto")

    # Move to the next page
    pdf.showPage()


def draw_lines(pdf: Canvas, x_position: float, height_margin: float, box_size: float, width_margin: float) -> None:
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
    number = sys.argv[1]
    path = sys.argv[2]
    uuid_requested = sys.argv[3]
    organs_requested = sys.argv[4]
    uuid_list = generate_uuids(int(number))
    create_big_labels_pdf(uuid_list, path, uuid_requested, organs_requested)

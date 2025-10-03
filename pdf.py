import os
from reportlab.lib.pagesizes import A4 as size
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from PIL import Image

def images_to_pdf(image_folder, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=size)
    width, height = size

    images_per_row = 3
    images_per_page = 9
    margin = 0.3 * inch
    spacing_x = 0.2 * inch
    spacing_y = 0.3 * inch

    img_width = (width - 2 * margin - (images_per_row - 1) * spacing_x) / images_per_row
    img_height = (height - 2 * margin - (images_per_page/images_per_row - 1) * spacing_y) / (images_per_page/images_per_row)
    img_width = 2.5 * inch
    img_height = 3.5 * inch
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    image_files.sort()

    x_positions = [margin + i * (img_width + spacing_x) for i in range(images_per_row)]
    y_positions = [height - margin - (j+1) * img_height - j * spacing_y for j in range(images_per_page//images_per_row)]

    count = 0
    for img_file in image_files:
        row = (count // images_per_row) % (images_per_page // images_per_row)
        col = count % images_per_row
        x = x_positions[col]
        y = y_positions[row]

        img_path = os.path.join(image_folder, img_file)
        with Image.open(img_path) as img:
            iw, ih = img.size
            aspect = iw / ih
            target_w, target_h = img_width, img_height

            if aspect > target_w / target_h:  
                draw_w = target_w
                draw_h = target_w / aspect
            else:
                draw_h = target_h
                draw_w = target_h * aspect

            offset_x = x + (target_w - draw_w) / 2
            offset_y = y + (target_h - draw_h) / 2

            c.drawImage(img_path, offset_x, offset_y, draw_w, draw_h, preserveAspectRatio=True, anchor='c')

        count += 1

        if count % images_per_page == 0:
            c.showPage()

    c.save()


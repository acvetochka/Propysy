from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def generate_guidelines(output_pdf="guidelines.pdf"):
    # Розміри сторінки A4
    page_width, page_height = A4
    
    # Параметри ліній
    horizontal_step_6mm = 6  # Відстань 6 мм
    horizontal_step_4mm = 4  # Відстань 4 мм
    slant_line_spacing = 28  # Відстань між косими лініями у мм
    slant_angle = 65  # Нахил у градусах
    margin_mm = 10  # Поля з усіх боків у мм
    
    # Конвертація мм у пікселі
    mm_to_px = 2.834
    step_6mm = horizontal_step_6mm * mm_to_px
    step_4mm = horizontal_step_4mm * mm_to_px
    slant_spacing_px = slant_line_spacing * mm_to_px
    margin = margin_mm * mm_to_px
    
    # Нові межі для малювання
    drawing_width = page_width - 2 * margin
    drawing_height = page_height - 2 * margin
    
    # Створення PDF
    c = canvas.Canvas(output_pdf, pagesize=A4)
    c.setStrokeColorRGB(0.8, 0.8, 0.8)  # Світло-сірий колір для ліній
    
    # Малювання горизонтальних ліній
    y = page_height - margin - step_6mm  # Початкова позиція з урахуванням верхнього поля
    while y > margin:
        # Пунктирна лінія
        c.setDash(3, 3)  # Довжина штриха та пробілу
        c.line(margin, y, page_width - margin, y)
        y -= step_6mm
        
        # Суцільна лінія через 6 мм
        c.setDash()  # Скидання пунктиру
        c.line(margin, y, page_width - margin, y)
        y -= step_4mm
        
        # Ще одна суцільна лінія через 4 мм
        c.line(margin, y, page_width - margin, y)
        y -= step_6mm
    
    # Малювання косих ліній
    c.setDash()  # Скидання пунктиру для косих ліній
    num_lines = int(drawing_width / slant_spacing_px) + 2  # Кількість косих ліній
    for i in range(-num_lines, num_lines):
        x_start = margin + i * slant_spacing_px
        y_start = margin
        x_end = x_start + drawing_height * (1 / (2.5))  # Тангенс кута приблизно відповідає 65°
        
        # Обмеження x_end, щоб лінія не виходила за праву межу
        if x_end > page_width - margin:
            x_end = page_width - margin
            y_end = margin + (x_end - x_start) * 2.5
        else:
            y_end = page_height - margin
        
        # Обмеження y_end, щоб лінія не виходила за нижню межу
        if y_end > page_height - margin:
            y_end = page_height - margin
        
        if x_start < margin:  # Якщо початок лінії виходить за ліву межу
            y_start = margin + (margin - x_start) * 2.5
            x_start = margin
        
        # Малюємо лінії у межах робочої області
        if y_start <= page_height - margin and y_end >= margin:
            c.line(x_start, y_start, x_end, y_end)
    
    # Поля рамкою (опціонально)
    c.setStrokeColorRGB(1, 1, 1)  
    c.rect(margin, margin, drawing_width, drawing_height)
    
    # Завершення малювання
    c.save()
    print(f"PDF-файл з виправленими лініями збережено як {output_pdf}")

# Генеруємо файл
generate_guidelines()

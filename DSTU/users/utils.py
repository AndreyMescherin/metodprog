import os
from PIL import Image
from django.conf import settings


def resize_image(image_field, max_width=300, max_height=300):
    """
    Изменяет размер изображения, сохраняя пропорции.
    
    Args:
        image_field: Поле изображения (InMemoryUploadedFile)
        max_width: Максимальная ширина
        max_height: Максимальная высота
    """
    img = Image.open(image_field)
    
    # Конвертируем RGBA в RGB (если нужно)
    if img.mode in ('RGBA', 'LA', 'P'):
        # Создаем белый фон
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = background
    
    # Изменяем размер с сохранением пропорций
    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
    
    # Сохраняем во временный буфер
    from io import BytesIO
    from django.core.files.uploadedfile import InMemoryUploadedFile
    
    output = BytesIO()
    img.save(output, format='JPEG', quality=85, optimize=True)
    output.seek(0)
    
    return InMemoryUploadedFile(
        output,
        'ImageField',
        f"{os.path.splitext(image_field.name)[0]}.jpg",
        'image/jpeg',
        output.tell(),
        None
    )
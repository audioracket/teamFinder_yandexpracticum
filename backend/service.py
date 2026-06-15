# backend/service.py

import io
import random

from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from django.core.paginator import Paginator

from .constants import (PROJECTS_PER_PAGE, AVATAR_SIZE, AVATAR_FONT_SIZE,
                        AVATAR_TEXT_COLOR, AVATAR_COLOR_MIN, AVATAR_COLOR_MAX)


def paginate(queryset, page, per_page=PROJECTS_PER_PAGE):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(page)


def generate_default_avatar(name):
    color = tuple(random.randint(AVATAR_COLOR_MIN, AVATAR_COLOR_MAX) for _ in range(3))
    img = Image.new('RGB', (AVATAR_SIZE, AVATAR_SIZE), color=color)
    d = ImageDraw.Draw(img)
    letter = name[0].upper() if name else '?'

    try:
        font = ImageFont.truetype('arial.ttf', AVATAR_FONT_SIZE)
    except IOError:
        font = ImageFont.truetype('DejaVuSans.ttf', AVATAR_FONT_SIZE)

    bbox = d.textbbox((0, 0), letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    d.text(
        ((AVATAR_SIZE - text_width) / 2, (AVATAR_SIZE - text_height) / 2),
        letter,
        fill=AVATAR_TEXT_COLOR,
        font=font
    )

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return ContentFile(buffer.getvalue(), name=f'default_{name}.png')

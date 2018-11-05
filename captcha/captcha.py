# PROJECT : easy-captcha
# TIME : 18-7-30 下午4:00
# AUTHOR : Younger Shen
# EMAIL : younger.shen@hotmail.com
# CELL : 13811754531
# WECHAT : 13811754531
import os
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageColor


class BaseError(Exception):
    message = None

    def __str__(self):
        return self.message


class CreateCaptchaFailedError(BaseError):
    message = 'create captcha image failed.'


class FontNotFoundError(BaseError):
    message = 'the required font is not found.'


class StringIsNoneError(BaseError):
    message = 'the captcha string is none.'


class Captcha:
    FONTS = [
        'RexBoldInline.otf',
        'TruenoBdOlIt.otf',
        'MicroSoftYaHei.ttf',
        'MicroSoftYaHeiBold.ttf'
    ]

    def make_captcha(self, string: str= None):
        raise NotImplementedError()

    def __init__(self):
        self.size = (100, 50)

    def _make_char(self, char, font, color=None, rotate=0):
        width, height, width_offset, height_offset = self._get_char_size(font, char)
        image = Image.new(mode='RGBA', size=(width, height))
        draw = ImageDraw.Draw(image)
        color = color if color else self._rand_color
        draw.text((width_offset, height_offset), char, font=font, fill=color)

        if rotate is not None:
            image = self._rotate(image, rotate)
        else:
            image = self._rand_rotate(image)

        image = image.crop(image.getbbox())
        return image

    def _make_background(self, width, height, color=None,):
        color = color if color else self._rand_color
        image = Image.new('RGB', (width, height), color=color)
        return image

    def _load_font(self, path=None, name=None, size=48, index=0, encoding='', layout_engine=None):
        font_path = self._get_font_path(path=path, name=name)
        font = ImageFont.truetype(font=font_path,
                                  size=size,
                                  index=index,
                                  encoding=encoding,
                                  layout_engine=layout_engine)
        return font

    def _load_rand_font(self, index=0, encoding='', layout_engine=None):
        import random
        i = random.randrange(0, len(self.FONTS))
        name = self.FONTS[i]
        font = self._load_font(name=name,
                               index=index,
                               encoding=encoding,
                               layout_engine=layout_engine)
        return font

    def _rand_rotate(self, image):
        angel = random.randint(0, 360)
        image = self._rotate(image, angel)
        return image

    @property
    def _rand_color(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = 'rgb({R}, {G}, {B})'.format(R=r, G=g, B=b)
        return ImageColor.getrgb(color)

    @staticmethod
    def _get_color(r, g, b):
        color = 'rgb({R}, {G}, {B})'.format(R=r, G=g, B=b)
        return color

    @staticmethod
    def _get_char_size(font, char):
        size = font.getsize(char)
        width = size[0] * 2
        height = size[1] * 2
        width_offset = (width - size[0]) / 2
        height_offset = (height - size[1]) / 2
        return width, height, width_offset, height_offset

    @staticmethod
    def _rotate(image, angel=0):
        return image.rotate(angel)

    @staticmethod
    def _resize(image, size=None):
        return image.resize(size, resample=Image.ANTIALIAS)

    @staticmethod
    def _rand_resize(image):
        import math
        ratio = random.random() + 0.5
        width = math.floor(image.size[0] * ratio)
        height = math.floor(image.size[1] * ratio)
        size = width, height
        return image.resize(size)

    @staticmethod
    def _base_dir():
        path = os.path.dirname(__file__)
        return path

    @staticmethod
    def _rand_padding():
        return random.randrange(10, 15)

    def _get_font_path(self, path: Path=None, name: str=None):
        path = path if path else Path(os.path.join(self._base_dir(), 'fonts', name))
        if path.exists():
            return str(path)
        else:
            raise FontNotFoundError()


class SinaCaptcha(Captcha):
    # https://login.sina.com.cn/cgi/pin.php
    def make_captcha(self, string: str = None, font_size: int = 48, image_size: tuple = None):
        captcha = self._make_captcha(string, font_size)
        size = image_size if image_size else self.size
        captcha = self._resize(captcha, size)
        return captcha

    def _make_captcha(self, string, font_size):
        font_name = 'MicroSoftYaHei.ttf'
        font = self._load_font(name=font_name, size=font_size)
        char_images = self._make_char_images(string, font)
        image = self._make_image(char_images)
        return image

    def _make_image(self, images):
        width = 0
        height = 0
        padding = self._rand_padding()

        for i in images:
            width = width + i.size[0]
            height = i.size[1] if height < i.size[1] else height

        width = width + padding * len(images) - 1
        image = self._make_background(width, height, color=self._get_color(255, 255, 255))

        offset = 0
        for i in images:
            image.paste(i, (offset, 0), mask=i)
            offset = offset + i.size[0] + padding

        return image

    def _make_char_images(self, string, font):
        images = map(lambda c: self._make_char(c, font), string)
        return list(images)


class SimpleCaptcha(Captcha):
    def make_captcha(self, string: str= None):
        pass


class SimpleChineseCaptcha(Captcha):
    def make_captcha(self, string: str= None):
        pass

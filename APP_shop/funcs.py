import os

import xlrd
from django.conf import settings
from django.core.files.images import ImageFile
from django.db import transaction

from APP_shop.models import Product, Category


def find_file_in(file_name: str, path_for_find: str):
    """
    Ищет файл с заданным именем в заданном каталоге без учета расширения.
    Возвращает полный путь к файлу или None, если файл не найден.
    """
    # Получить список файлов в заданном каталоге
    files = os.listdir(path_for_find)

    # Пройти по всем файлам в каталоге
    for file in files:
        # Получить имя файла без расширения
        name, ext = os.path.splitext(file)
        if name == file_name:
            # Если найден файл с заданным именем, вернуть его полный путь
            return os.path.join(path_for_find, file)

    # Если файл не найден, вернуть None
    return None


@transaction.atomic
def parse_xls_file_to_bd(xlsfile, category):
    wb = xlrd.open_workbook(file_contents=xlsfile.read())
    sheet = wb.sheet_by_index(0)
    for row in range(1, sheet.nrows):
        first_value_splited = sheet.cell(row, 0).value.split(', ')
        if len(first_value_splited[0]) != 13 or len(first_value_splited) != 2:
            continue
        proba = first_value_splited[1].strip()
        size = str(sheet.cell(row, 3).value).strip().replace(',', '.')
        try:
            size = float(size)
        except ValueError:
            size = None
        desc = sheet.cell(row, 4).value.strip()
        name = sheet.cell(row, 7).value.split()[0].strip()
        weight = str(sheet.cell(row, 8).value).strip().replace(',', '.')
        try:
            weight = float(weight)
        except ValueError:
            weight = None
        img_path = find_file_in(name, os.path.join(settings.BASE_DIR, '1C_PHOTO'))
        # print('-------------------------')
        # print(f'0:{sheet.cell(row, 0).value} '  # proba[1]
        #       f'1:{sheet.cell(row, 1).value} '  # none
        #       f'2:{sheet.cell(row, 2).value} '  # none
        #       f'3:{sheet.cell(row, 3).value} '  # size
        #       f'4:{sheet.cell(row, 4).value} '  # desc
        #       f'5:{sheet.cell(row, 5).value} '  # none
        #       f'6:{sheet.cell(row, 6).value}'   # UID
        #       f'7:{sheet.cell(row, 7).value.split()[0]}'   # name
        #       f'8:{sheet.cell(row, 8).value}'   # weight
        #       )
        if img_path and not Product.objects.filter(name=name).exists():
            product = Product.objects.create(
                name=name,
                description=desc,
                slug=name + str(weight) + str(size),
                proba=proba,
                size=size,
                weight=weight,
                category=Category.objects.get(name=category)
            )
            product.image.save(name, ImageFile(open(img_path, 'rb')))
            product.save()

import requests
from bs4 import BeautifulSoup
import sys
import re
import os
import django
from django.core.files import File
from io import BytesIO

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Clothing_StoreProject.settings")

# 2. Initialize Django
django.setup()

from ClothingShop.models import *


url = "https://4menshop.com/"
mainPageSoup = BeautifulSoup(requests.get(url).text, features="html.parser")
mainPageDropDownMenuListItems = mainPageSoup.select(".dropdown")

LoaiSanPham.objects.all().delete()
SanPham.objects.all().delete()

for mainPageDropDownMenuListItem in mainPageDropDownMenuListItems:
    mainPageDropDownAnchor = mainPageDropDownMenuListItem.select(".dropdown-toggle")[0]
    mainCategory = mainPageDropDownAnchor.text.lower()
    if mainCategory.startswith("bộ sưu tập"):
        continue
    mainPageDropDownSubMenuAnchors = mainPageDropDownMenuListItem.select(
        ".dropdown-menu.submenu li a"
    )
    for mainPageDropDownSubMenuAnchor in mainPageDropDownSubMenuAnchors:
        subcategory = mainPageDropDownSubMenuAnchor.text.lower()

        productCategoryPageHREF = mainPageDropDownSubMenuAnchor.get("href")
        if not productCategoryPageHREF.startswith("https"):
            productCategoryPageHREF = "https://4menshop.com" + productCategoryPageHREF

        productCategoryPageBeautifulSoup = BeautifulSoup(
            requests.get(productCategoryPageHREF).text, "html.parser"
        )

        productItems = productCategoryPageBeautifulSoup.select(".product-item")

        for productItem in productItems:
            try:
                img = productItem.select(".thumb-img img")[0].get("src")
                # imgFilename = img.get()
                productTitle = productItem.select(".product-title")[0].text
                productPrice = productItem.select(".product-price")[0].text

                image_response = File((BytesIO(requests.get(img).content)))
                image_name = os.path.basename(img)
                
                json = {
                    "TenSanPham": productTitle.lower(),
                    "Gia": int("".join(productPrice[0:-2].split(","))),
                    "HinhAnh": "" + os.path.basename(img),
                    "DanhMucChinh": mainCategory.lower(),
                    "DanhMucPhu": subcategory.lower(),
                }
                LoaiSanPham_, _ = LoaiSanPham.objects.get_or_create(
                    DanhMucChinh=json["DanhMucChinh"], DanhMucPhu=json["DanhMucPhu"]
                )

                SanPham_ = SanPham.objects.create(
                    TenSanPham=json["TenSanPham"],
                    Gia=json["Gia"],
                    LoaiSanPham=LoaiSanPham_,
                )

                SanPham_.HinhAnh.save(image_name, image_response, save = True)
                print(f"Created product: {SanPham_.TenSanPham} with image {image_name}")
            except Exception as e:
                print(e)
                continue

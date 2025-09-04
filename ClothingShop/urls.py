from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

app_name = "ClothingShop"
urlpatterns = [
    path("", IndexView, name="Index"),
    path("dangky/", DangKyView, name="DangKy"),
    path("dangnhap/", DangNhapView, name="DangNhap"),
    path("timsanpham/", TimSanPhamView, name="TimKiemSanPham"),
    path("getdanhmucphu/", GetDanhMucPhu, name="GetDanhMucPhu"),
    path("bovaogiohang/", BoVaoGioHang, name="BoVaoGioHang"),
    path("dathang/", DatHangView, name="DatHang"),
    path(
        "suasoluongsanphamtrongdonhang/",
        SuaSoLuongSanPhamTrongDonHang,
        name="SuaSoLuongSanPhamTrongDonHang",
    ),
    path(
        "xoasanphamtrongdonhang/",
        XoaSanPhamTrongDonHang,
        name="XoaSanPhamTrongDonHang",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

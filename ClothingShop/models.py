from django.db import models

# Create your models here.


class TaiKhoan(models.Model):
    TenNguoiDung = models.CharField(
        max_length=200, blank=False, null=False, unique=True
    )
    MatKhau = models.CharField(max_length=200, blank=False, null=False, unique=True)
    Email = models.EmailField(max_length=200, blank=False, null=False)


class LoaiSanPham(models.Model):
    DanhMucChinh = models.CharField(max_length=200, blank=False, null=False)
    DanhMucPhu = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return f"{self.id}-{self.DanhMucChinh}-{self.DanhMucPhu}"


class SanPham(models.Model):
    TenSanPham = models.CharField(max_length=200, blank=False, null=False, unique=True)
    LoaiSanPham = models.ForeignKey(
        LoaiSanPham, on_delete=models.CASCADE, blank=False, null=False
    )
    HinhAnh = models.ImageField(upload_to="AnhSanPham/")
    Gia = models.PositiveBigIntegerField(blank=False, null=False)

    def __str__(self):
        return f"{self.id}-{self.TenSanPham}-{self.HinhAnhURL}-{self.Gia}-{self.LoaiSanPham.DanhMucChinh}-{self.LoaiSanPham.DanhMucPhu}"


class DonHang(models.Model):
    TenNguoiNhan = models.CharField(max_length=200, blank=False, null=False)
    SDTNguoiNhan = models.CharField(max_length=10, blank=False, null=False)
    DiaChi = models.CharField(max_length=200, blank=False, null=False)
    ThoiGianDat = models.DateTimeField(blank=False, null=False, auto_now_add=True)
    NguoiDat = models.ForeignKey(
        TaiKhoan, on_delete=models.CASCADE, blank=False, null=False
    )
    DaNhan = models.BooleanField(blank=False, null=False, default=False)


class ChiTietDonHang(models.Model):
    SanPham = models.ForeignKey(
        SanPham, on_delete=models.CASCADE, blank=False, null=False
    )
    DonHang = models.ForeignKey(
        DonHang, on_delete=models.CASCADE, blank=False, null=False
    )
    SoLuong = models.IntegerField(blank=False, null=False)

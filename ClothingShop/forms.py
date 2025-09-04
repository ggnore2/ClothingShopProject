from django import forms
from .models import *


class DangKyForm(forms.ModelForm):
    class Meta:
        model = TaiKhoan
        fields = ["TenNguoiDung", "Email", "MatKhau"]
        widgets = {
            "TenNguoiDung": forms.TextInput(
                attrs={
                    "class": "FormControl",
                    "placeholder": "Nhập tên người dùng",
                }
            ),
            "Email": forms.EmailInput(
                attrs={
                    "class": "FormControl",
                    "placeholder": "Nhập email",
                }
            ),
            "MatKhau": forms.PasswordInput(
                attrs={
                    "class": "FormControl",
                    "placeholder": "Nhập mật khẩu",
                }
            ),
        }
        error_messages = {
            "TenNguoiDung": {
                "required": "Không được để trống",
                "unique": "Tên người dùng đã tồn tại",
            },
            "Email": {
                "required": "Không được để trống",
                "unique": "Email đã tồn tại",
                "invalid": "Phải nhập email hợp lệ",
            },
            "MatKhau": {
                "required": "Không được để trống",
            },
        }


class DangNhapForm(forms.Form):
    TenNguoiDungHayEmail = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Tên người dùng hoặc Email", "class": "FormControl"},
        ),
        error_messages={"required": "Không được để trống"},
    )

    MatKhau = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Mật khẩu", "class": "FormControl"},
        ),
        error_messages={"required": "Không được để trống"},
    )


class TimSanPhamForm(forms.Form):
    TenSanPham = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Tên sản phẩm", "class": "FormControl"}
        ),
    )
    DanhMucChinh = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(attrs={"class": "FormControl DanhMucChinh"}),
    )
    DanhMucPhu = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(attrs={"class": "FormControl DanhMucPhuField"}),
    )
    GiaLonNhat = forms.IntegerField(
        initial=1000000,
        min_value=0,
        widget=forms.NumberInput(
            attrs={"placeholder": "Giá lớn nhất (VND)", "class": "FormControl"}
        ),
    )
    GiaNhoNhat = forms.IntegerField(
        initial=0,
        min_value=0,
        widget=forms.NumberInput(
            attrs={"placeholder": "Giá nhỏ nhất (VND)", "class": "FormControl"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Luôn load danh mục chính
        mains = LoaiSanPham.objects.values_list("DanhMucChinh", flat=True).distinct()
        self.fields["DanhMucChinh"].choices = [("", "Chọn danh mục chính")] + [
            (m, m.capitalize()) for m in mains
        ]

        # Nếu có DanhMucChinh trong data thì load danh mục phụ tương ứng
        data = self.data or self.initial
        selected_main = data.get("DanhMucChinh")
        if selected_main:
            subs = (
                LoaiSanPham.objects.filter(DanhMucChinh=selected_main)
                .values_list("DanhMucPhu", flat=True)
                .distinct()
            )
            self.fields["DanhMucPhu"].choices = [("", "Chọn danh mục phụ")] + [
                (s, s.capitalize()) for s in subs
            ]
        else:
            self.fields["DanhMucPhu"].choices = [("", "Chọn danh mục phụ")]


class DatHangForm(forms.ModelForm):
    class Meta:
        model = DonHang
        fields = ["TenNguoiNhan", "SDTNguoiNhan", "DiaChi"]
        widgets = {
            "TenNguoiNhan": forms.TextInput(
                attrs={
                    "class": "FormControl",
                    "placeholder": "Nhập tên người nhận",
                }
            ),
            "SDTNguoiNhan": forms.TextInput(
                attrs={
                    "class": "FormControl",
                    "placeholder": "Nhập số điện thoại",
                }
            ),
            "DiaChi": forms.TextInput(
                attrs={
                    "class": "FormControl",
                    "placeholder": "Nhập địa chỉ",
                }
            ),
        }
        error_messages = {
            "TenNguoiNhan": {"required": "Không được để trống"},
            "SDTNguoiNhan": {
                "required": "Không được để trống",
            },
            "DiaChi": {
                "required": "Không được để trống",
            },
        }

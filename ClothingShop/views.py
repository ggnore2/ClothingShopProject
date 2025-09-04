from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from .forms import *
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
import json
from django.contrib import messages
import re

# Create your views here.


def IndexView(request):
    template_name = "base.html"
    dangKyForm = DangKyForm()
    context = {"dangKyForm": dangKyForm}
    return render(request=request, template_name=template_name, context=context)


def DangKyView(request):
    template_name = "signup.html"
    form = None
    if request.method == "POST":
        form = DangKyForm(request.POST)
        if form.is_valid():
            taiKhoan = form.save(commit=False)
            taiKhoan.MatKhau = make_password(form.cleaned_data["MatKhau"])
            taiKhoan.save()
            messages.success(request=request, message="Đăng ký thành công")
            redirect(reverse("ClothingShop:TimKiemSanPham"))
    else:
        form = DangKyForm()
    context = {"dangKyForm": form}
    return render(request=request, template_name=template_name, context=context)


def DangNhapView(request):
    template_name = "login.html"
    template_name_for_index = ""
    form = None
    if request.method == "POST":
        form = DangNhapForm(request.POST)
        if form.is_valid():
            TenNguoiDungHayEmail = form.cleaned_data["TenNguoiDungHayEmail"]
            MatKhau = form.cleaned_data["MatKhau"]
            taiKhoan = TaiKhoan.objects.filter(
                Q(TenNguoiDung=TenNguoiDungHayEmail) | Q(Email=TenNguoiDungHayEmail)
            ).first()
            if taiKhoan:
                if check_password(MatKhau, taiKhoan.MatKhau):
                    request.session["taiKhoanID"] = taiKhoan.id
                    messages.success(request=request, message="Đăng nhập thành công")
                    redirect(reverse("ClothingShop:TimKiemSanPham"))
                else:
                    form.add_error("MatKhau", "Sai thông tin đăng nhập")
            else:
                form.add_error("MatKhau", "Sai thông tin đăng nhập")
    else:
        form = DangNhapForm()
    context = {"dangNhapForm": form}
    return render(request=request, template_name=template_name, context=context)


def TimSanPhamView(request):
    template_name = "searchProduct.html"
    form = TimSanPhamForm(request.GET or None)
    page_obj = None
    page_window = []
    query_string = ""

    if form.is_valid():
        ten_san_pham = form.cleaned_data["TenSanPham"]
        danhMucChinh = form.cleaned_data["DanhMucChinh"]
        danhMucPhu = form.cleaned_data["DanhMucPhu"]
        gia_nho_nhat = form.cleaned_data["GiaNhoNhat"]
        gia_lon_nhat = form.cleaned_data["GiaLonNhat"]

        if gia_nho_nhat > gia_lon_nhat:
            form.add_error("GiaLonNhat", "Giá lớn nhất nhỏ hơn giá nhỏ nhất")
        else:
            products = SanPham.objects.filter(
                TenSanPham__icontains=ten_san_pham,
                LoaiSanPham__DanhMucChinh__icontains=danhMucChinh,
                LoaiSanPham__DanhMucPhu__icontains=danhMucPhu,
                Gia__gte=gia_nho_nhat,
                Gia__lte=gia_lon_nhat,
            )

            # Pagination
            paginator = Paginator(products, 5)
            page_number = request.GET.get("page", 1)
            page_obj = paginator.get_page(page_number)

            index = page_obj.number - 1
            max_index = len(paginator.page_range)
            start_index = index - 2 if index >= 2 else 0
            end_index = index + 3 if index <= max_index - 3 else max_index
            page_window = paginator.page_range[start_index:end_index]

            querydict = request.GET.copy()
            if "page" in querydict:
                querydict.pop("page")
            query_string = querydict.urlencode()

    context = {
        "timSanPhamForm": form,
        "pageObj": page_obj,
        "page_window": page_window,
        "query_string": query_string,
    }

    return render(request, template_name, context)


def GetDanhMucPhu(request):
    if request.method == "POST":
        danhMucChinh = json.loads(request.body)["DanhMucChinh"]
        print(danhMucChinh)
        return JsonResponse(
            list(
                LoaiSanPham.objects.filter(DanhMucChinh=danhMucChinh).values_list(
                    "DanhMucPhu", flat=True
                )
            ),
            safe=False,
        )


def BoVaoGioHang(request):
    if request.method == "POST":
        boVaoGioHangJSON = json.loads(request.body)
        cart = request.session.get("cart", [])

        index = next(
            (
                i
                for i, x in enumerate(cart)
                if x["idSanPham"] == boVaoGioHangJSON["idSanPham"]
            ),
            -1,
        )
        if index != -1:
            cart[index]["soLuongSanPham"] += boVaoGioHangJSON["soLuongSanPham"]
        else:
            cart.append(boVaoGioHangJSON)

        request.session["cart"] = cart
        return JsonResponse({"status": "ok", "cart": cart})
    return JsonResponse({"error": "Invalid method"}, status=405)


def DatHangView(request):
    template_name = "datHang.html"
    form = DatHangForm()
    donHang = request.session["cart"]
    if donHang == None or len(donHang) == 0:
        messages.error(request=request, message="Chưa đặt hàng")
        return redirect(reverse("ClothingShop:TimKiemSanPham"))
    if request.method == "POST":
        if request.session["taiKhoanID"] == None:
            messages.error(request=request, message="Chưa đăng nhập")
            return redirect(reverse("ClothingShop:TimKiemSanPham"))
        form = DatHangForm(request.POST)
        if form.is_valid():
            SDTNguoiNhan = form.cleaned_data["SDTNguoiNhan"]
            if not re.findall("\d{10}", SDTNguoiNhan):
                form.add_error("SDTNguoiNhan", "Sai định dang: phải là 10 ký tự số")
            else:
                donHang = form.save(commit=False)
                taiKhoanID = request.session["taiKhoanID"]
                taiKhoan = TaiKhoan.objects.get(id=taiKhoanID)
                donHang.NguoiDat = taiKhoan
                donHang.save()
                for item in request.session["cart"]:
                    idSanPham = item["idSanPham"]
                    soLuongSanPham = item["soLuongSanPham"]
                    sanPham = SanPham.objects.get(id=idSanPham)
                    ChiTietDonHang.objects.create(
                        DonHang=donHang, SanPham=sanPham, SoLuong=soLuongSanPham
                    )
                request.session["cart"] = []
                messages.success(request=request, message="Đặt hàng thành công")
                return redirect(reverse("ClothingShop:TimKiemSanPham"))

    displayedDonHang = []
    for donHangRow in donHang:
        idSanPham = donHangRow["idSanPham"]
        soLuongSanPham = donHangRow["soLuongSanPham"]
        sanPham = SanPham.objects.filter(id=idSanPham).values().first()
        sanPham["soLuongSanPham"] = soLuongSanPham
        try:
            sp = SanPham.objects.get(id=idSanPham)
            sanPham["hinhAnhURL"] = sp.HinhAnh.url
        except SanPham.DoesNotExist:
            sanPham["hinhAnhURL"] = None
        displayedDonHang.append(sanPham)

    context = {}
    context["datHangForm"] = form
    context["donHang"] = displayedDonHang
    return render(request=request, template_name=template_name, context=context)


def SuaSoLuongSanPhamTrongDonHang(request):
    if request.method == "POST":
        suaSoLuongSanPhamJSON = json.loads(request.body)
        print(suaSoLuongSanPhamJSON)
        cart = request.session.get("cart", [])

        index = next(
            (
                i
                for i, x in enumerate(cart)
                if x["idSanPham"] == suaSoLuongSanPhamJSON["idSanPham"]
            ),
            -1,
        )
        if index != -1:
            cart[index]["soLuongSanPham"] = suaSoLuongSanPhamJSON["soLuongSanPham"]

        else:
            return JsonResponse({"ok": False})

        request.session["cart"] = cart
        print(request.session["cart"])
        return JsonResponse({"ok": True})


def XoaSanPhamTrongDonHang(request):
    if request.method == "POST":
        xoaSanPhamTrongGioHangJSON = json.loads(request.body)
        cart = request.session.get("cart", [])

        index = next(
            (
                i
                for i, x in enumerate(cart)
                if x["idSanPham"] == xoaSanPhamTrongGioHangJSON["idSanPham"]
            ),
            -1,
        )

        if index != -1:
            cart.pop(index)
        else:
            return JsonResponse({"ok": False})

        request.session["cart"] = cart
        print(request.session["cart"])
        return JsonResponse({"ok": True})

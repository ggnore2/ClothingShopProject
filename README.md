# Clothing Shop Project

Web bán quần áo đơn giản, làm bằng Django + MySQL (backend) và HTML/CSS/JS (frontend).

## Chức năng
- Đăng ký, đăng nhập
- Xem sản phẩm, thêm vào giỏ, đặt hàng
- Quản lý sản phẩm, đơn hàng, tài khoản (admin)

## Công nghệ
- Django (Python)
- MySQL
- HTML, CSS, JavaScript

## Cách chạy
```bash
git clone https://github.com/ggnore2/ClothingShopProject.git
cd ClothingShopProject
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # Mac/Linux
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

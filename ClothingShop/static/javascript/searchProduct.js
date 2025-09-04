document.addEventListener('DOMContentLoaded', function () {
    const danhMucChinhField = document.querySelector(".DanhMucChinh");
    const danhMucPhuField = document.querySelector(".DanhMucPhuField");

    function selectByText(field, text) {
        if (typeof text !== 'string' || !text) return;
        const options = field.options;
        for (let i = 0; i < options.length; i++) {
            if (options[i].text.toLowerCase() === text.toLowerCase()) {
                options[i].selected = true;
                break;
            }
        }
    }

    async function populateDanhMucPhu(selectedDanhMucPhu = null) {
        try {
            const danhMucChinh = danhMucChinhField.value || "";
            if (!danhMucChinh) {
                danhMucPhuField.innerHTML = '<option value="">Chọn danh mục phụ</option>';
                return;
            }

            const response = await postJSONData("/getdanhmucphu/", { DanhMucChinh: danhMucChinh });
            if (!response.ok) throw new Error(`Network error: ${response.status}`);

            const danhMucPhus = await response.json();
            danhMucPhuField.innerHTML = '';
            danhMucPhuField.append(new Option("Chọn danh mục phụ", ""));

            danhMucPhus.forEach(element => {
                danhMucPhuField.append(new Option(capitalizeFirstLetter(element), element));
            });

            if (typeof selectedDanhMucPhu === 'string' && selectedDanhMucPhu) {
                selectByText(danhMucPhuField, selectedDanhMucPhu);
            } else {
                const urlParams = new URLSearchParams(window.location.search);
                selectByText(danhMucPhuField, urlParams.get("DanhMucPhu"));
            }
        } catch (error) {
            console.error("Fetch failed:", error);
            danhMucPhuField.innerHTML = '<option value="">Lỗi khi tải</option>';
        }
    }

    // Initial load
    populateDanhMucPhu();

    // IMPORTANT: don't pass the event as the first arg
    danhMucChinhField.addEventListener('change', () => populateDanhMucPhu());
});


let soLuongSanPhamInput = document.querySelector(".SoLuongSanPhamInput");
let boVaoGioHangButtons = document.querySelectorAll(".BoVaoGioHangButton");

boVaoGioHangButtons.forEach(boVaoGioHangButton => {

    boVaoGioHangButton.onclick = async function () {
        let soLuongSanPham = parseInt(soLuongSanPhamInput.value);
        let idSanPham = parseInt(boVaoGioHangButton.getAttribute("data-product-id"));
        let response = await postJSONData("/bovaogiohang/", {
            idSanPham: idSanPham,
            soLuongSanPham: soLuongSanPham
        });
        let json = await response.json();

        showMessage("Bỏ vào giỏ hàng thành công");
    }
});
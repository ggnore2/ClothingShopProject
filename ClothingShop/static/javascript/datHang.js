let ChangeQuantityInputs = document.querySelectorAll(".ChangeQuantityInput");
let RemoveFromCartButtons = document.querySelectorAll(".RemoveFromCartButton");
ChangeQuantityInputs.forEach(ChangeQuantityInput => {
    ChangeQuantityInput.onchange = async function () {
        let idSanPham = parseInt(ChangeQuantityInput.getAttribute("data-idSanPham"));
        let soLuongSanPham = parseInt(ChangeQuantityInput.value);
        if (soLuongSanPham === "" || soLuongSanPham == null) {
            ChangeQuantityInput.value = 1;
            soLuongSanPham = 1;
        }
        await postJSONData("/suasoluongsanphamtrongdonhang/", {
            "idSanPham": idSanPham,
            "soLuongSanPham": soLuongSanPham
        });
    }

});

RemoveFromCartButtons.forEach(RemoveFromCartButton => {
    RemoveFromCartButton.onclick = async function () {
        let idSanPham = parseInt(RemoveFromCartButton.getAttribute("data-idSanPham"));
        await postJSONData("/xoasanphamtrongdonhang/", {
            "idSanPham": idSanPham
        });
        window.location.reload();
    }
})
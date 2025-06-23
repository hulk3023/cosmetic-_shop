document.querySelector("form[action*='add_to_cart']").addEventListener("submit", function(e) {
    e.preventDefault();
    this.submit();
    alert("Mahsulot savatchaga qo'shildi!");
});
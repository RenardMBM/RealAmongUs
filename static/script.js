const show = document.getElementById("show");
const show_txt = document.getElementById("show-text");
const r = document.getElementById("role")
const b = document.getElementById("shield")

show.onclick = function() {
    r.style.display = (r.style.display === 'block') ? 'none' : 'block';
    b.style.display = (r.style.display === 'block') ? 'none' : 'block';
    show_txt.textContent = (r.style.display === 'block') ? 'Спрятать роль' : 'Показать роль';
}
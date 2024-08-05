$(document).ready(function () {
  $("#sidebarCollapse").on("click", function () {
    $("#sidebar, #content").toggleClass("active");
  });
});

window.addEventListener('load', function () {
  document.getElementById('loader').style.display = 'none';
  document.getElementById('content').style.display = 'block';
});
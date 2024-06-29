// static/js/upload.js

// Get the modal
var modal = document.getElementById("myModal");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// Function to open the modal
function openModal(prediction) {
  document.getElementById("prediction-result").innerText = prediction;
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

document.querySelector('form').addEventListener('submit', function(e) {
  e.preventDefault(); // Prevent the default form submission

  var formData = new FormData(this);

  fetch("/your-form-url/", {
    method: 'POST',
    body: formData,
    headers: {
      'X-Requested-With': 'XMLHttpRequest'
    }
  })
  .then(response => response.json())
  .then(data => {
    openModal(data.prediction);
  })
  .catch(error => console.error('Error:', error));
});

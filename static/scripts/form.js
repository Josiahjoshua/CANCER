document.getElementById('uploadForm').addEventListener('submit', function(e) {
  e.preventDefault(); // Prevent default form submission

  var formData = new FormData(this);

  fetch("/upload-and-predict/", {
      method: 'POST',
      body: formData,
      headers: {
          'X-Requested-With': 'XMLHttpRequest'
      }
  })
  .then(response => response.json())
  .then(data => {
      if (data.error) {
          alert(data.error);
      } else {
          openResultsModal(data);
      }
  })
  .catch(error => console.error('Error:', error));
});

function openResultsModal(data) {
  document.getElementById("predictedClass").innerText = data.predicted_class;
  document.getElementById("cancerProbability").innerText = (data.cancer_probability * 100).toFixed(2) + '%';
  document.getElementById("calcificationType").innerText = data.calcification_type;
  document.getElementById("resultsModal").style.display = "block";
}

document.getElementsByClassName("close")[0].onclick = function() {
  document.getElementById("resultsModal").style.display = "none";
};

window.onclick = function(event) {
  if (event.target === document.getElementById("resultsModal")) {
      document.getElementById("resultsModal").style.display = "none";
  }
};

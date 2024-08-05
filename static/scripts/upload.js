document.addEventListener('DOMContentLoaded', function() {
    const uploadBtn = document.getElementById('uploadBtn');
    const uploadModal = document.getElementById('uploadModal');
    const resultsModal = document.getElementById('resultsModal');
    const uploadForm = document.getElementById('uploadForm');
    const loading = document.getElementById('loading');
  
    uploadBtn.onclick = function(event) {
        event.preventDefault();
        uploadModal.style.display = "block";
    };
  
    document.querySelectorAll('.close').forEach(function(closeBtn) {
        closeBtn.onclick = function() {
            this.closest('.modal').style.display = "none";
        };
    });
  
    window.onclick = function(event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = "none";
        }
    };
  
    uploadForm.onsubmit = function(e) {
        e.preventDefault();
        loading.style.display = "block";
        
        fetch("/upload-and-predict/", {
            method: 'POST',
            body: new FormData(this),
        })
        .then(response => response.json())
        .then(data => {
            loading.style.display = "none";
            uploadModal.style.display = "none";
            
            if (data.error) {
                alert(data.error);
            } else {
                document.getElementById('predictedClass').textContent = data.predicted_class;
                document.getElementById('cancerProbability').textContent = (data.cancer_probability * 100).toFixed(2) + '%';
                document.getElementById('calcificationType').textContent = data.calcification_type;
                
                resultsModal.style.display = "block";
            }
        })
        .catch(error => {
            console.error('Error:', error);
            loading.style.display = "none";
            alert('An error occurred during analysis.');
        });
    };
  });
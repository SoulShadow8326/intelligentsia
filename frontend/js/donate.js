document.addEventListener('DOMContentLoaded', function(){
    var donateBtn = document.querySelector('.donate-cta');
    var modal = document.getElementById('donate-modal');
    var cancel = document.getElementById('cancel-upload');
    var confirm = document.getElementById('confirm-upload');
    var fileInput = document.getElementById('id-upload');
    var fileName = document.getElementById('file-name');
    var defaultText = 'No file selected';

    fileName.textContent = defaultText;

    function openModal(){
        modal.classList.add('show');
    }
    function closeModal(){
        modal.classList.remove('show');
        fileInput.value = '';
        fileName.textContent = defaultText;
    }

    donateBtn.addEventListener('click', function(e){
        e.preventDefault();
        openModal();
    });

    cancel.addEventListener('click', function(){
        closeModal();
    });

    fileInput.addEventListener('change', function(){
        if(fileInput.files && fileInput.files[0]){
            var name = fileInput.files[0].name;
            if(name.length > 48) name = name.slice(0, 20) + '…' + name.slice(-20);
            fileName.textContent = name;
        } else {
            fileName.textContent = defaultText;
        }
    });

    confirm.addEventListener('click', function(){
        if(!fileInput.files || !fileInput.files[0]){
            fileName.textContent = 'Please select a file first';
            return;
        }
        confirm.disabled = true;
        confirm.textContent = 'Uploading...';
        var fd = new FormData();
        fd.append('file', fileInput.files[0]);
        fetch('/upload-id', { method: 'POST', body: fd })
            .then(function(r){ return r.json(); })
            .then(function(json){
                confirm.disabled = false;
                confirm.textContent = 'Upload & Continue';
                if(json && json.ok){
                    closeModal();
                    if(json.match){
                        alert('ID verified. Thank you. Proceeding to payment.');
                    } else {
                        alert('Uploaded ID does not match the expected image. Please contact support.');
                    }
                } else {
                    alert('Upload failed: ' + (json && json.error ? json.error : 'unknown'));
                }
            })
            .catch(function(err){
                confirm.disabled = false;
                confirm.textContent = 'Upload & Continue';
                alert('Upload failed');
            });
    });
});

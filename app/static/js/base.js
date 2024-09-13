function triggerFileInput() {
    document.getElementById('file-input').click();
}

function uploadFile() {
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];
    const loadingMessage = document.getElementById('loading-message');

    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        loadingMessage.style.display = 'block';

        fetch('/upload', {
            method: 'POST',
            body: formData
        }).then(response => {
            if (response.ok) {
                loadingMessage.style.display = 'none';
                window.location.reload();
            } else {
                alert('Ошибка при загрузке файла');
                loadingMessage.style.display = 'none';
            }
        }).catch(error => {
            console.error('Ошибка:', error);
            alert('Ошибка при отправке запроса');
            loadingMessage.style.display = 'none';
        });
    }
}
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        alert("Ссылка скопирована в буфер обмена");
    }, function(err) {
        console.error('Ошибка копирования', err);
    });
}
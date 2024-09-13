function triggerFileInput() {
    document.getElementById('file-input').click();
}

function uploadFile() {
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];

    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        fetch('/upload', {
            method: 'POST',
            body: formData
        }).then(response => {
            if (response.ok) {
                window.location.reload();
            } else {
                alert('Ошибка при загрузке файла');
            }
        }).catch(error => {
            console.error('Ошибка:', error);
            alert('Ошибка при отправке запроса');
        });
    }
}
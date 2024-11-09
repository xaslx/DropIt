function openModal(fileId) {
    console.log(fileId);
    const modal = document.getElementById('reportModal-open');
    
    if (modal) {
        modal.style.display = 'flex';
        document.getElementById('confirmReport').onclick = function() {
            sendReport(fileId);
        };
    } else {
        console.error('Модальное окно не найдено!');
    }
}


function closeModal() {
    const modal = document.getElementById('reportModal-open');
    
    if (modal) {
        modal.style.display = 'none';
    } else {
        console.error('Модальное окно не найдено!');
    }
}


function deleteFile(fileId) {
    if (confirm('Вы уверены, что хотите удалить файл?')) {
        fetch(`${fileId}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                alert('Файл успешно удален');
                window.location.href = '/';
            } else {
                alert('Ошибка при удалении файла');
            }
        })
        .catch(error => console.error('Ошибка:', error));
    }
}
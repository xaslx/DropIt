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



function sendReport(fileId) {
    const notyf = new Notyf({
        duration: 2000,
        dismissible: true,
        position: {
            x: 'center',
            y: 'top'
        },
        types: [
            {
                type: 'success',
                background: '#8BC34A',
                icon: {
                    className: 'fas fa-check',
                    tagName: 'i',
                    text: ''
                }
            },
            {
                type: 'error',
                background: 'red',
                icon: {
                    className: 'fas fa-exclamation-triangle',
                    tagName: 'i',
                    text: ''
                }
            }
        ]
    });
    fetch(`/report/${fileId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(response => {
        if (response.ok) {
            notyf.success('Жалоба успешно отправлена.')
            closeModal();
        } else {
            notyf.error('Не удалось отправить жалобу')
        }
    })
    .catch(error => {
        alert('Ошибка: ' + error.message);
    });
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
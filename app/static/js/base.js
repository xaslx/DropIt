function triggerFileInput() {
    document.getElementById('file-input').click();
}

const notyf = new Notyf({
    duration: 1500,
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


function uploadFile() {
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];
    const loadingMessage = document.getElementById('loading-message');
    const maxFileSize = 100 * 1024 * 1024;

    if (file) {
        if (file.size > maxFileSize) {
            notyf.error('Файл слишком большой. Максимальный размер: 100 МБ.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);
        loadingMessage.style.display = 'block';

        fetch('/upload', {
            method: 'POST',
            body: formData
        }).then(response => {
            loadingMessage.style.display = 'none';
            if (response.ok) {
                sessionStorage.setItem('notification', 'success');
                sessionStorage.setItem('message', 'Файл успешно загружен!');
                window.location.reload();
            } else if (response.status === 413) {
                notyf.error('Файл слишком большой.');
            } else if (response.status === 400) {
                notyf.error('Перезагрузите страницу, и попробуйте снова.');
            } else if (response.status === 409) {
                notyf.error('Вы не можете загружать файлы, так как вы заблокированы.');
            } else {
                notyf.error('Ошибка при загрузке файла.');
            }
        }).catch(error => {
            console.error('Ошибка:', error);
            loadingMessage.style.display = 'none';
            notyf.error('Ошибка при отправке запроса. Попробуйте позже.');
        });
    }
}


document.addEventListener('DOMContentLoaded', function() {
    const notification = sessionStorage.getItem('notification');
    const message = sessionStorage.getItem('message');

    if (notification && message) {
        if (notification === 'success') {
            notyf.success(message);
        } else if (notification === 'error') {
            notyf.error(message);
        }
        sessionStorage.removeItem('notification');
        sessionStorage.removeItem('message');
    }
});




function copyToClipboard(inputId) {
    var input = document.getElementById(inputId);
    
    navigator.clipboard.writeText(input.value).then(function() {
        notyf.success('Ссылка скопирована');
    }, function(err) {
        console.error('Ошибка копирования', err);
    });
}


let fileIdToDelete = null;


function openModal(fileId) {
    fileIdToDelete = fileId;
    document.getElementById("modal").style.display = "block";
}

function closeModal() {
    fileIdToDelete = null;
    document.getElementById("modal").style.display = "none";
}


function confirmDeletion() {
    if (fileIdToDelete) {
        fetch(`${fileIdToDelete}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                
                sessionStorage.setItem('notification', 'success');
                sessionStorage.setItem('message', 'Файл был успешно удален.');
                
                closeModal();
                window.location.reload();
            } else {
       
                notyf.error('Ошибка при удалении файла.');
            }
        })
        .catch(error => {
            console.error("Произошла ошибка:", error);

            notyf.error('Ошибка при отправке запроса на удаление. Попробуйте позже.');
        });
    }
}

document.querySelectorAll('.delete-button').forEach(button => {
    button.addEventListener('click', function() {
        const fileId = this.getAttribute('data-file-id');
        openModal(fileId);
    });
});

function openTermsModal() {
    document.getElementById('modal-terms').style.display = 'block';
}

function closeTermsModal() {
    document.getElementById('modal-terms').style.display = 'none';
}
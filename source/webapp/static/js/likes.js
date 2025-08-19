window.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.like-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const type = btn.dataset.type;
            const id = btn.dataset.id;
            if (!type || !id) return;

            try {
                const response = await fetch(`/${type}/${id}/like/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                        'Content-Type': 'application/json'
                    }
                });
                const data = await response.json();
                btn.textContent = data.liked ? 'Анлайк' : 'Лайк';
                btn.nextElementSibling.textContent = data.likes_count;
            } catch (err) {
                console.error('Ошибка:', err);
            }
        });
    });
});

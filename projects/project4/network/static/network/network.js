document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('.js-edit-button').forEach((button)=> {
        button.addEventListener('click', () => {
            const post = button.parentElement;

            // Replaces the post content with a textarea that prefills with the old content
            const post_content = post.querySelector('.js-post-content');
            const textarea = create_text_area(post_content.innerHTML);
            post_content.replaceWith(textarea);

            // Replace the edit button with a newly created save button
            button.style.display = 'none';
            const save_button = create_save_button();
            timestamp_div = post.querySelector('.post-timestamp');
            post.insertBefore(save_button, timestamp_div);

            // Clicking the save button updates the post content in both frontend and backend
            const post_id = button.dataset.postId;
            save_button.addEventListener('click', ()=>{
                // Update the post content in the frontend
                textarea_new = post.querySelector('textarea');
                post_content.innerHTML = textarea_new.value;
                textarea_new.replaceWith(post_content);
                // Update the post content in the backend
                fetch('/edit/' + post_id, {
                    method: 'PUT',
                    body: JSON.stringify({
                        content: textarea_new.value
                    })
                })
                .then(result => {
                    console.log(result);
                })
                .catch(error => {
                    console.log('Error:', error);
                });
                // Replace the save button with the edit button.
                button.style.display = 'block';
                save_button.remove();
            });
        });
    });

    document.querySelectorAll('.js-heart').forEach((button)=> {
        button.addEventListener('click', () => {
            let likes_count_span = button.parentElement.querySelector('.post-like-count');
            let likes_count = Number(likes_count_span.innerHTML);
            if (button.innerHTML.trim() === "🤍"){
                button.innerHTML = "❤️";
                likes_count++;
            }
            else {
                button.innerHTML = "🤍";
                likes_count--;
            }
            likes_count_span.innerHTML = likes_count;
        });
    });
});

function create_text_area(content) {
    const textarea = document.createElement('textarea');
    textarea.style.display = 'block';
    textarea.style.marginBottom = '10px';
    textarea.textContent = content;
    textarea.autofocus = true;
    textarea.rows = "5";
    textarea.cols = "60";
    return textarea;
}

function create_save_button() {
    const save_button = document.createElement('button');
    save_button.textContent = 'save';
    save_button.className = 'btn btn-sm btn-danger';
    return save_button;
}
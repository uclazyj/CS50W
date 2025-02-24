document.addEventListener('DOMContentLoaded', function() {

    // document.querySelector('#edit_button').addEventListener();
    document.querySelectorAll('.js-edit_button').forEach((button)=> {
        button.addEventListener('click', (event)=>{
            event.preventDefault();
            const post = button.parentElement;
            const post_content = post.querySelector('.js-post-content');
            
            const textarea = document.createElement('textarea');
            textarea.style.display = 'block';
            textarea.style.marginBottom = '10px';
            textarea.textContent = post_content.innerHTML;
            textarea.autofocus = true;
            textarea.rows = "5";
            textarea.cols = "60";

            post_content.replaceWith(textarea);
            button.style.display = 'none';

            const save_button = document.createElement('button');
            save_button.textContent = 'save';
            save_button.className = 'btn btn-sm btn-danger';

            timestamp_div = post.querySelector('.post-timestamp');
            post.insertBefore(save_button, timestamp_div);

            const post_id = button.dataset.postId;
            
            save_button.addEventListener('click', (e)=>{
                // e.preventDefault();
                textarea_new = post.querySelector('textarea');
                post_content.innerHTML = textarea_new.value;
                textarea_new.replaceWith(post_content);
                button.style.display = 'block';
                save_button.remove();

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

            });
        });
    });
});

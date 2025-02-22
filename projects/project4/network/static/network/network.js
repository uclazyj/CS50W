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

            save_button.addEventListener('click', (e)=>{
                // e.preventDefault();
                textarea_new = post.querySelector('textarea');
                console.log(textarea_new.value);
                post_content.innerHTML = textarea_new.value.replace(/\n/g, '<br>');
                textarea_new.replaceWith(post_content);
                save_button.remove();
                button.style.display = 'block';
            });
        });
    });
});


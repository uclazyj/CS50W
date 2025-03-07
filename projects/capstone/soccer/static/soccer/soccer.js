document.addEventListener('DOMContentLoaded', (event) => {
    
    document.querySelectorAll('.draggable').forEach(draggable => {

        const id=draggable.id;
        // Retrieve the saved position from localStorage
        const savedPosition = JSON.parse(localStorage.getItem('draggablePosition_' + id));
        if (savedPosition) {
            draggable.style.left = savedPosition.left;
            draggable.style.top = savedPosition.top;
        }

        draggable.addEventListener('mousedown', function(e) {
            const mouse_initial_x = e.clientX;
            const mouse_initial_y = e.clientY;
            const draggable_initial = draggable.getBoundingClientRect();

            function onMouseMove(event) {
                const mouse_current_x = event.pageX;
                const mouse_current_y = event.pageY;
                draggable_final_left = draggable_initial.left + mouse_current_x - mouse_initial_x;
                draggable_final_top = draggable_initial.top + mouse_current_y - mouse_initial_y;

                draggable_final_left = Math.max(draggable_final_left, 0);
                draggable_final_left = Math.min(draggable_final_left, window.innerWidth - draggable.offsetWidth);

                draggable_final_top = Math.max(draggable_final_top, 0);
                draggable_final_top = Math.min(draggable_final_top, window.innerHeight - draggable.offsetHeight);

                draggable.style.left = draggable_final_left + 'px';
                draggable.style.top = draggable_final_top + 'px';
            }

            document.addEventListener('mousemove', onMouseMove);

            function onMouseUp() {
                document.removeEventListener('mousemove', onMouseMove);
                document.removeEventListener('mouseup', onMouseUp);
                // Save the new position to localStorage
                localStorage.setItem('draggablePosition_' + id, JSON.stringify({
                    left: draggable.style.left,
                    top: draggable.style.top
                }));
            }
            
            document.addEventListener('mouseup', onMouseUp);

        });

    });

});
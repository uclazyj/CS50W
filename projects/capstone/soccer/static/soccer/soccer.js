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
            const draggable_initial_x = draggable.getBoundingClientRect().left;
            const draggable_initial_y = draggable.getBoundingClientRect().top;

            function onMouseMove(event) {
                const mouse_current_x = event.pageX;
                const mouse_current_y = event.pageY;
                draggable.style.left = draggable_initial_x + mouse_current_x - mouse_initial_x + 'px';
                draggable.style.top = draggable_initial_y + mouse_current_y - mouse_initial_y + 'px';
            }

            document.addEventListener('mousemove', onMouseMove);

            function onMouseUp() {
                document.removeEventListener('mousemove', onMouseMove);
                // Save the new position to localStorage
                localStorage.setItem('draggablePosition_' + id, JSON.stringify({
                    left: draggable.style.left,
                    top: draggable.style.top
                }));
            }
            
            draggable.addEventListener('mouseup', onMouseUp);

        });

    });

});
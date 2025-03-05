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
            // shiftX is the mouse's x coordinate in the viewport minus the draggable's x coordinate in the viewport.
            let shiftX = e.clientX - draggable.
            getBoundingClientRect().left;
            let shiftY = e.clientY - draggable.getBoundingClientRect().top;

            function onMouseMove(event) {
                // The final position of the draggable is determined by the coordinates in the document (not the viewport), making dragging in a long document across several viewports possible.
                draggable.style.left = event.pageX - shiftX + 'px';
                draggable.style.top = event.pageY - shiftY + 'px';
            }

            document.addEventListener('mousemove', onMouseMove);

            draggable.addEventListener('mouseup', function() {
                document.removeEventListener('mousemove', onMouseMove);

                // Save the new position to localStorage
                localStorage.setItem('draggablePosition_' + id, JSON.stringify({
                    left: draggable.style.left,
                    top: draggable.style.top
                }));
            });
            
        });

    });

});
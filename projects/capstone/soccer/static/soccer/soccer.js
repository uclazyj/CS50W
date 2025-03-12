let player_id = 1;
const add_player_button = document.getElementById('add_button');
const list = document.getElementById('list');

const upper_boundary_position = document.getElementById('upper_boundary').getBoundingClientRect().top;
const lower_boundary_position = document.getElementById('lower_boundary').getBoundingClientRect().top;
const team_boundary_position = document.getElementById('team1').getBoundingClientRect().right;

// Initialize existing draggable elements
document.querySelectorAll('.draggable').forEach(draggable => {
    initializeDraggable(draggable);
});

function updateTeam(draggable) {
    const rect = draggable.getBoundingClientRect();
    // No team assigned
    if (rect.bottom <= lower_boundary_position) {
        draggable.style.backgroundColor = 'lightgreen';
        return 0;
    }
    // Assigned to team 1
    else if (rect.top >= lower_boundary_position && rect.right <= team_boundary_position) {
        draggable.style.backgroundColor = 'lightpink';
        return 1;
    }
    // Assigned to team 2
    else if (rect.top >= lower_boundary_position && team_boundary_position <= rect.left) {
        draggable.style.backgroundColor = 'lightblue';
        return 2;
    }
    // No change in team
    return -1;
}


function initializeDraggable(draggable) {
    const id = draggable.dataset.id;
    
    const closeBtn = draggable.querySelector('.close');
    // Prevent the parent element's event listeners from being triggered when clicking the close button
    closeBtn.addEventListener('mousedown', (mousedown_event) => {
        mousedown_event.stopPropagation();
    });
    closeBtn.addEventListener('mousemove', (mousemove_event) => {
        mousemove_event.stopPropagation();
    });
    closeBtn.addEventListener('mouseup', (mouseup_event) => {
        mouseup_event.stopPropagation();
    });

    closeBtn.addEventListener('click', (event) => {
        // Prevent the 'mouseup' event from being triggered
        event.stopPropagation();
        draggable.remove();
        fetch('/team_split', {
            method: 'DELETE',
            body: JSON.stringify({
                player_id: id
            })
        })
        .then(result => {
            console.log(result);
        })
        .catch(error => {
            console.log('Error:', error);
        });
    });

    // Retrieve the saved position and team info from backend
    const team_id = parseInt(draggable.dataset.teamId);
    if (team_id > 0) {
        draggable.style.left = draggable.dataset.x + 'px';
        draggable.style.top = draggable.dataset.y + 'px';
        draggable.style.position = 'absolute';
        if (team_id == 1) {
            draggable.style.backgroundColor = 'lightpink';
        }
        else {
            draggable.style.backgroundColor = 'lightblue';
        }
    }

    draggable.addEventListener('mousedown', function(e) {
        const mouse_initial_x = e.clientX;
        const mouse_initial_y = e.clientY;
        const draggable_initial = draggable.getBoundingClientRect();
        
        function onMouseMove(event) {
            draggable.style.position = 'absolute';
            const mouse_current_x = event.pageX;
            const mouse_current_y = event.pageY;
            let draggable_final_left = draggable_initial.left + mouse_current_x - mouse_initial_x;
            let draggable_final_top = draggable_initial.top + mouse_current_y - mouse_initial_y;

            // Boundary checks
            draggable_final_left = Math.max(draggable_final_left, 0);
            draggable_final_left = Math.min(draggable_final_left, window.innerWidth - draggable.offsetWidth);

            
            draggable_final_top = Math.max(draggable_final_top, upper_boundary_position);
            draggable_final_top = Math.min(draggable_final_top, window.innerHeight - draggable.offsetHeight);

            draggable.style.left = draggable_final_left + 'px';
            draggable.style.top = draggable_final_top + 'px';

            updateTeam(draggable);
        }

        document.addEventListener('mousemove', onMouseMove);

        function onMouseUp() {
            document.removeEventListener('mousemove', onMouseMove);
            document.removeEventListener('mouseup', onMouseUp);

            draggable_updated_position = draggable.getBoundingClientRect();

            const team_id = updateTeam(draggable);
            if (team_id === 0) {
                draggable.style.position = 'static';
            }

            // Save the new position to backend
            fetch('/team_split', {
                method: 'PUT',
                body: JSON.stringify({
                    player_id: id,
                    x: draggable_updated_position.left,
                    y: draggable_updated_position.top,
                    team_id: team_id
                })
            })
            .then(result => {
                console.log(result);
            })
            .catch(error => {
                console.log('Error:', error);
            });

        }

        document.addEventListener('mouseup', onMouseUp);

        // draggable.ondragstart = function() {
        //     return false;
        // };
    });
}


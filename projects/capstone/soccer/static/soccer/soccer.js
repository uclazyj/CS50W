let player_id = 1;
const list = document.getElementById('list');

// Initialize existing draggable elements
document.querySelectorAll('.draggable').forEach(draggable => {
    initializeDraggable(draggable);
});

// Start polling when page loads
setInterval(pollForUpdates, 1000);  // Check every second

function updateTeam(draggable) {
    const rect = draggable.getBoundingClientRect();
    const lower_boundary_position = document.getElementById('lower_boundary').getBoundingClientRect().top;
    const team_boundary_position = document.getElementById('team1').getBoundingClientRect().right;
    // No team assigned
    if (rect.bottom <= lower_boundary_position) {
        draggable.style.position = 'static';
        draggable.style.backgroundColor = 'lightgreen';
        return 0;
    }
    // Assigned to team 1
    else if (rect.top >= lower_boundary_position && rect.right <= team_boundary_position) {
        draggable.style.position = 'absolute';
        draggable.style.backgroundColor = 'lightpink';
        return 1;
    }
    // Assigned to team 2
    else if (rect.top >= lower_boundary_position && team_boundary_position <= rect.left) {
        draggable.style.position = 'absolute';
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
        // Update count immediately when deleting
        const currentCount = document.querySelectorAll('.draggable').length;
        updatePlayerCount(currentCount);

        fetch('/player/delete', {
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
        const teams_container = document.querySelector('.teams-container');
        draggable.style.left = draggable.dataset.xProportion * teams_container.offsetWidth - draggable.offsetWidth / 2 + 'px';
        const lower_boundary_position = document.getElementById('lower_boundary').getBoundingClientRect().bottom;
        draggable.style.top = lower_boundary_position + draggable.dataset.yProportion * teams_container.offsetHeight - draggable.offsetHeight / 2 + 'px';

        draggable.style.position = 'absolute';
        if (team_id == 1) {
            draggable.style.backgroundColor = 'lightpink';
        }
        else {
            draggable.style.backgroundColor = 'lightblue';
        }
    }

    draggable.addEventListener('mousedown', onMouseDown);

    function onMouseDown(e) {
        const draggable_initial = draggable.getBoundingClientRect();
        draggable.pointer_offset_x = e.clientX - draggable_initial.left;
        draggable.pointer_offset_y = e.clientY - draggable_initial.top;
        
        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp);

        // draggable.ondragstart = function() {
        //     return false;
        // };
    }



    function onMouseMove(event) {
        draggable.isDragging = true;
        draggable.style.position = 'absolute';

        let draggable_final_left = event.pageX - draggable.pointer_offset_x;
        let draggable_final_top = event.pageY - draggable.pointer_offset_y;

        // Boundary checks
        draggable_final_left = Math.max(draggable_final_left, 0);
        draggable_final_left = Math.min(draggable_final_left, window.innerWidth - draggable.offsetWidth);

        const upper_boundary_position = document.getElementById('upper_boundary').getBoundingClientRect().top + window.scrollY;
        draggable_final_top = Math.max(draggable_final_top, upper_boundary_position);

        const lower_boundary_position = window.innerHeight + window.scrollY - draggable.offsetHeight
        draggable_final_top = Math.min(draggable_final_top, lower_boundary_position);

        draggable.style.left = draggable_final_left + 'px';
        draggable.style.top = draggable_final_top + 'px';

        updateTeam(draggable);
    }

    function onMouseUp() {
        draggable.isDragging = false;
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);

        const x_center = draggable.offsetLeft + draggable.offsetWidth / 2;
        const y_center = draggable.offsetTop + draggable.offsetHeight / 2;
        const teams_container = document.querySelector('.teams-container');
        const x_proportion = x_center / teams_container.offsetWidth;

        const lower_boundary_position = document.getElementById('lower_boundary').getBoundingClientRect().bottom;
        const y_proportion = (y_center - lower_boundary_position) / teams_container.offsetHeight;

        const team_id = updateTeam(draggable);

        // Save the new position to backend
        fetch('/player/update', {
            method: 'PUT',
            body: JSON.stringify({
                player_id: id,
                x_proportion: x_proportion,
                y_proportion: y_proportion,
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
}

function updatePlayerCount(count) {
    const countElement = document.querySelector('#player-count strong');
    if (countElement) {
        countElement.textContent = count;
        if (count === 1){
            document.querySelector('#player-count span').innerHTML = 'player';
        }
    }
}

// In your pollForUpdates function, add:
function pollForUpdates() {
    fetch('/players')
        .then(response => response.json())
        .then(data => {
            // First, get all current draggable elements
            const currentDraggables = document.querySelectorAll('.draggable');
            
            // Remove elements that no longer exist in the backend
            currentDraggables.forEach(draggable => {
                const exists = data.players.some(player => player.id === parseInt(draggable.dataset.id));
                if (!exists) {
                    draggable.remove();
                }
            });

            // Add new players and update existing ones
            data.players.forEach(playerData => {
                let draggable = document.querySelector(`[data-id="${playerData.id}"]`);
                
                // Create new player if it doesn't exist
                if (!draggable) {
                    draggable = document.createElement('div');
                    draggable.className = 'draggable';
                    draggable.dataset.id = playerData.id;
                    draggable.dataset.teamId = playerData['team_id'];

                    const nameDiv = document.createElement('div');
                    nameDiv.className = 'name';
                    nameDiv.innerText = playerData.name;
                    draggable.appendChild(nameDiv);

                    const closeBtn = document.createElement('div');
                    closeBtn.className = 'close';
                    closeBtn.textContent = '❌';
                    draggable.appendChild(closeBtn);

                    list.appendChild(draggable);
                    initializeDraggable(draggable);
                }

                // Update player if not being dragged
                if (!draggable.isDragging) {
                    const team_id = parseInt(playerData['team_id']);
                    if (team_id === 0) {
                        draggable.style.position = 'static';
                        draggable.style.backgroundColor = 'lightgreen';
                    } else {
                        const teams_container = document.querySelector('.teams-container');
                        draggable.style.left = playerData['x_proportion'] * teams_container.offsetWidth - draggable.offsetWidth / 2 + 'px';
                        lower_boundary_position = document.getElementById('lower_boundary').getBoundingClientRect().bottom;
                        draggable.style.top = lower_boundary_position + playerData['y_proportion'] * teams_container.offsetHeight - draggable.offsetHeight / 2 + 'px';
                        draggable.style.position = 'absolute';
                        if (team_id === 1) {
                            draggable.style.backgroundColor = 'lightpink';
                        } else if (team_id === 2) {
                            draggable.style.backgroundColor = 'lightblue';
                        }
                    }
                }
            });
            
            // Update player count
            updatePlayerCount(data.players.length);
        });
}

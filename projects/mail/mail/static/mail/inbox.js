document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Add submit button listener here, once
  document.querySelector('.btn-primary').addEventListener('click', (event)=>{
    event.preventDefault();
    post_email();
  })

  // By default, load the inbox
  load_mailbox('inbox');
});

function post_email() {

  let recipients = document.querySelector('#compose-recipients').value;
  let subject = document.querySelector('#compose-subject').value;
  let body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // // Print result
      console.log(result);
      load_mailbox('sent');
  })
  .catch(error => {
    console.log('Error:', error);
  });
}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function createEmailRow(sender, subject, timestamp) {
  // Create the main elements
  const emailRow = document.createElement('div');
  emailRow.className = 'email-row';

  const leftGroup = document.createElement('div');
  leftGroup.className = 'left-group';

  const emailSpan = document.createElement('span');
  emailSpan.className = 'email-address';
  emailSpan.textContent = sender;

  const subjectSpan = document.createElement('span');
  subjectSpan.className = 'email-subject';
  subjectSpan.textContent = subject;

  const timestampSpan = document.createElement('span');
  timestampSpan.className = 'timestamp';
  timestampSpan.textContent = timestamp;

  // Assemble the elements
  leftGroup.appendChild(emailSpan);
  leftGroup.appendChild(subjectSpan);
  emailRow.appendChild(leftGroup);
  emailRow.appendChild(timestampSpan);

  return emailRow;
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch('/emails/' + mailbox)
  .then(response => response.json())
  .then(emails => {
      emails.forEach(email => {
        const email_row = createEmailRow(email.sender, email.subject, email.timestamp);
        document.querySelector('#emails-view').appendChild(email_row);
      });
  });
}
document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Add submit button listener here, once
  document.querySelector('#compose-form').addEventListener('submit', (event)=>{
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
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function createEmailRow(email) {
  // Create the main elements
  const emailRow = document.createElement('div');
  emailRow.className = 'email-row';
  emailRow.style.cursor = 'pointer';
  emailRow.style.backgroundColor = email.read ? 'lightgray' : 'white';
  const leftGroup = document.createElement('div');
  leftGroup.className = 'left-group';

  const emailSpan = document.createElement('span');
  emailSpan.className = 'email-address';
  emailSpan.textContent = email.sender;

  const subjectSpan = document.createElement('span');
  subjectSpan.className = 'email-subject';
  subjectSpan.textContent = email.subject;

  const timestampSpan = document.createElement('span');
  timestampSpan.className = 'timestamp';
  timestampSpan.textContent = email.timestamp;

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
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch('/emails/' + mailbox)
  .then(response => response.json())
  .then(emails => {
      emails.forEach(email => {
        const email_row = createEmailRow(email);
        document.querySelector('#emails-view').appendChild(email_row);
        email_row.addEventListener('click', () => {
          fetch('/emails/' + email.id, {
            method: 'PUT',
            body: JSON.stringify({
                read: true
            })
          })
          .then(() => {
            load_email(email.id);
          });
        });
      });
  });
}

function load_email(email_id) {
    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';

    fetch('/emails/' + email_id)
    .then(response => response.json())
    .then(email => {
      console.log(email);
      document.querySelector('#email-view').replaceChildren(create_email_div(email));
    });
}

function create_email_div(email) {
  const email_div = document.createElement('div');

  email_div.appendChild(create_info_div('From: ', email.sender));
  email_div.appendChild(create_info_div('To: ', email.recipients.join(', ')));
  email_div.appendChild(create_info_div('Subject: ', email.subject));
  email_div.appendChild(create_info_div('Timestamp: ', email.timestamp));

  const reply_button = document.createElement('button');
  reply_button.textContent = 'Reply';
  reply_button.className = 'btn btn-sm btn-primary button-spacing';
  email_div.appendChild(reply_button);
  reply_button.addEventListener('click', () => {
    reply_email(email);
  });

  const archive_button = document.createElement('button');
  archive_button.textContent = email.archived ? 'Unarchive' : 'Archive';
  archive_button.className = 'btn btn-sm btn-warning button-spacing';
  email_div.appendChild(archive_button);
  archive_button.addEventListener('click', () => {
    fetch('/emails/' + email.id, {
      method: 'PUT',
      body: JSON.stringify({
        archived: !email.archived
      })
    })
    .then(() => {
      load_mailbox('inbox');
    });
  });
  
  const hr = document.createElement('hr');
  email_div.appendChild(hr);
  const body_div = document.createElement('div');
  body_div.textContent = email.body;
  email_div.appendChild(body_div);
  return email_div;
}

function create_info_div(bold_text, text) {
  const info_div = document.createElement('div');

  const bold_span = document.createElement('span');
  bold_span.textContent = bold_text;
  bold_span.style.fontWeight = 'bold';

  const text_span = document.createElement('span');
  text_span.textContent = text;

  info_div.appendChild(bold_span);
  info_div.appendChild(text_span);
  return info_div;
}

function reply_email(email) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Pre-fill the form
  document.querySelector('#compose-recipients').value = email.sender;
  if (email.subject.startsWith('Re:')) {
    document.querySelector('#compose-subject').value = email.subject;
  } else {
    document.querySelector('#compose-subject').value = 'Re: ' + email.subject;
  }
  document.querySelector('#compose-body').value = 'On ' + email.timestamp + ', ' + email.sender + ' wrote: \n\n' + email.body;
}
document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  //For Forum of compose
  document.querySelector('#compose-form').onsubmit = submited;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function submited() {
  const compose_recipients = document.querySelector('#compose-recipients').value;
  const compose_subject = document.querySelector('#compose-subject').value;
  const compose_body = document.querySelector('#compose-body').value;
  // console.log(compose_recipients, compose_subject, compose_body);

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: compose_recipients,
      subject: compose_subject,
      body: compose_body
    })
  })
  .then(response => response.json())
  .then(result => {
    load_mailbox('sent');
  });

  // load_mailbox('sent');
  return false; // To prevent submitting the forum
}

function load_mailbox(mailbox) {
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails)
    for (let i of Object.keys(emails)) {
      const element = document.createElement('div');
      element.classList.add('email');
      if (emails[i].read === false) {
        element.classList.add('to_read');
      }
      // console.log(i)
      element.innerHTML = `
        <div>Subject: ${emails[i].subject}</div>
        <div>Sender: ${emails[i].sender}</div>
        <div>Date: ${emails[i].timestamp}</div>
      ` ;
      // console.log(emails[i].id)
      element.addEventListener('click', () => load_email(emails[i].id, mailbox));

      // console.log(element)
      document.querySelector('#emails-view').append(element);
    };
  });
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}

function load_email(id, mailbox){
  let sent = false;
  console.log(mailbox)
  if (mailbox==="sent"){
    sent = true;
  }

  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);
    document.querySelector('#email-view').innerHTML = `
    <div>From: ${email.sender}</div>
    <div>To: ${email.recipients}</div>
    <div>Subject: ${email.subject}</div>
    <div>Timestamp: ${email.timestamp}</div>            
    
    <div class="email-buttons">
      <button class="btn-email" id="reply">Reply</button>
      <button class="btn-email" id="archive">${email["archived"] ? "Unarchive" : "Archive"}</button>
    </div>
    <hr>
    <div>
      ${email.body.replaceAll('\n','<br>')}
    </div>
    `;
  
    console.log(sent)
    if (sent) 
    {
      document.querySelector('.email-buttons').style.display = 'none';
    }

    document.querySelector('#archive').addEventListener('click', () => {
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: !email.archived
        })
      })
      .then(result =>{
        load_email(email.id, mailbox);
      })
    })

    document.querySelector('#reply').addEventListener('click', () => {

      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'block';
      document.querySelector('#email-view').style.display = 'none';

      document.querySelector('#compose-recipients').value = email.sender;

      //console.log(email.subject.slice(0,3))
      //console.log(email.subject.slice(0,3) != "Re:")
      if (email.subject.slice(0,3) != "Re:") {
        document.querySelector('#compose-subject').value = "Re:" + email.subject;
      }
      else {
        document.querySelector('#compose-subject').value = email.subject;
      }
      document.querySelector('#compose-body').value = `\n \n \nOn ${email.timestamp} ${email.sender} wrote:\n${email.body}\n\n`;
    })
  })
}

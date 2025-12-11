async function checkNewEvent() {

  if (document.querySelector("dialog")) return;

  try {


    const response = await fetch(`http://localhost:5000/new_event/${player}/?t=${Date.now()}`);
    const data = await response.json();


    if (data !== 0) {


      if (!isPaused) {
        await fetch('http://localhost:5000/pause', {method: 'POST'});
        isPaused = true;
        pauseBtn.classList.remove('pause');
        pauseBtn.classList.add('play');
      }


      const body = document.querySelector('body');
      const dialog = document.createElement('dialog');
      const span = document.createElement('span');
      const img = document.createElement('img');
      const heading = document.createElement('h2');
      const description = document.createElement('p');


      if (data[0] === 1) img.src = 'images/meteorite.jpeg';
      else if (data[0] === 2) img.src = 'images/stadium.jpeg';
      else if (data[0] === 3) img.src = 'images/storm.jpeg';
      else if (data[0] === 4) img.src = 'images/baggage.jpeg';
      else img.src = 'images/plane.jpeg';

      heading.textContent = data[1];
      description.textContent = data[2];
      span.innerHTML = "&#x2715;";
      span.style.float = "right";
      span.style.cursor = "pointer";
      span.style.fontSize = "20px";


      dialog.appendChild(span);
      dialog.appendChild(heading);
      dialog.appendChild(img);
      dialog.appendChild(description);
      body.appendChild(dialog);

      dialog.showModal();


      span.addEventListener('click', async () => {
        dialog.close();
        body.removeChild(dialog);


        await fetch('http://localhost:5000/resume', {method: 'POST'});
        isPaused = false;
        pauseBtn.classList.remove('play');
        pauseBtn.classList.add('pause');
      });
    }
  } catch (err) {
    console.error('Check New Event Error:', err);
  }
}
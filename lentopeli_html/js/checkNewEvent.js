'use strict';

// tarkastaa onko uutta eventtiä, jos on tulee showmodali siitä

async function checkNewEvent() {
  if (document.querySelector("dialog")) return;

  try {
    const response = await fetch(`http://localhost:5000/new_event/${player}/`);
    const data = await response.json();

    if (data !== 0) {

      // pausettaa pelin jos ei ole jo

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


      body.appendChild(dialog);
      dialog.appendChild(span)
      dialog.appendChild(img);


      if (data[0] === 1) {
        img.src = 'images/meteorite.jpeg'
      }
      else if (data[0] === 2) {
        img.src = 'images/stadium.jpeg'
      }
      else if (data[0] === 3) {
        img.src = 'images/storm.jpeg'
      }
      else if (data[0] === 4) {
        img.src = 'images/baggage.jpeg'
      }
      else {
        img.src = 'images/plane.jpeg'
      }

      img.alt = 'image'

      heading.textContent = data[1]

      description.textContent = data[2]
      span.innerHTML = "&#x2715;";

      dialog.appendChild(heading);
      dialog.appendChild(description);
      console.log('showing modal for event', data)
      dialog.showModal()

      const close_button = dialog.querySelector('span');
      close_button.style.cursor = 'pointer';
      close_button.addEventListener('click', async () => {

        dialog.close();
        body.removeChild(dialog);

        //jatkaa peliä
        await fetch('http://localhost:5000/resume', {method: 'POST'});
        isPaused = false;
        pauseBtn.classList.remove('play');
        pauseBtn.classList.add('pause');
      })

    }

  }catch(err) {
    console.error('Server not responding:', err);
  }
}
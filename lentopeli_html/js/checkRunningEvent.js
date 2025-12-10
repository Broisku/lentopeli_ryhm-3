'use strict';

// tarkastaa jos eventti on päättynyt, jos on tulee alertti siitä

async function checkRunningEvent() {

  try {
    const response = await fetch(`http://localhost:5000/running_event/${player}/`);
    const data = await response.json();

    if (data === 2) {
      alert('Event has finished.')
    }
  } catch (error) {
    console.error('Server not responding:', error);
  }
}
async function checkRunningEvent() {
  try {

    const response = await fetch(`http://localhost:5000/running_event/${player}/?t=${Date.now()}`);
    const data = await response.json();

    if (data === 2) {
      alert('Event has finished.');

      updateStats();
    }
  } catch (error) {
    console.error('Check Running Event Error:', error);
  }
}
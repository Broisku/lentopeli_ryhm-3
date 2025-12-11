'use strict';

const map = L.map('map').setView([52.52, 13.4], 4);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

const allAirportsLayer = L.layerGroup().addTo(map);

// haetaan lentokentät python apista
fetch('http://localhost:5000/airports').
    then(res => res.json()).
    then(airports => {
      console.log('Owned airports loaded:', airports);

      airports.forEach(airport => {

        const name = airport[3];
        const type = airport[2];
        const lat = parseFloat(airport[4]);
        const lon = parseFloat(airport[5]);
        const country = airport[8];
        const municipality = airport[10];
        const iata = airport[12];
        const icao = airport[11];

        if (!isNaN(lat) && !isNaN(lon)) {

          const marker = L.marker([lat, lon]);

          marker.bindPopup(`
            <b>${name}</b><br>
            Type: ${type}<br>
            City: ${municipality}<br>
            Country: ${country}<br>
            IATA: ${iata || 'N/A'}<br>
            ICAO: ${icao || 'N/A'}<br>
            Lat: ${lat}<br>
            Lon: ${lon}
            
            <button class="buyBtn">Buy</button>
          `);

          allAirportsLayer.addLayer(marker);
          console.log('Owned airports loaded:', airports);

          marker.on('popupopen', (e) => {
            const btn = e.popup.getElement().querySelector('.buyBtn');

            btn.addEventListener('click', () => {
              alert(`Airport purchased: ${name}`);
              console.log({name, iata, icao, lat, lon});
            });
          });

        }
      });
    }).
    catch(error => console.error(error));

function getPlayerName() {
  const params = new URLSearchParams(window.location.search);
  return params.get('name');
}

const ownedLayer = L.layerGroup();

let showingOwned = false;

let isPaused = false;
const pauseBtn = document.getElementById('pause');


const toggle1 = document.getElementById('toggle1');

const player = getPlayerName();

document.getElementById('player_name').textContent = player;

toggle1.addEventListener('click', () => {

  if (!showingOwned) {
    if (map.hasLayer(allAirportsLayer)) map.removeLayer(allAirportsLayer);
    ownedLayer.clearLayers();

    const ownedUrl = `http://localhost:5000/airports/owned/${player}`;

    function fetchOwned(url) {
      fetch(url).
          then(res => res.json()).
          then(airports => {

            airports.forEach(airport => {
              const type = airport[0];
              const name = airport[1];
              const icao = airport[3];
              const iata = airport[4];
              const lat = parseFloat(airport[6]);
              const lon = parseFloat(airport[7]);
              const profit = parseFloat(airport[8]);
              const country = airport[9];
              const runways = airport[10];
              const runway_construction = airport[11];
              const runway_state = airport[12];
              const terminals = airport[13];
              const terminals_construction = airport[14];
              const terminals_state = airport[15];

              let size;
              if (type === 'small_airport') size = 'small airport';
              else if (type === 'medium_airport') size = 'medium airport';
              else size = 'large airport';

              let maxRunways, maxTerminals;
              let con_time, cost;
              if (type === 'small_airport') {
                maxRunways = 2;
                maxTerminals = 1;
                con_time = "<b>Construction time:</b> 12 weeks";
                cost = "<b>Cost:</b> 3,000,000";
              } else if (type === 'medium_airport') {
                maxRunways = 3;
                maxTerminals = 2;
                con_time = "<b>Construction time:</b> 12 weeks";
                cost = "<b>Cost:</b> 6,000,000";
              } else {
                maxRunways = 4;
                maxTerminals = 3;
                con_time = "<br>Construction time:</br> 12 weeks";
                cost = "<b>Cost:</b> 9,000,000";
              }

              const ownedRunways = runways || 0;
              const ownedTerminals = terminals || 0;

              const runwayBtnLabel = ownedRunways < maxRunways ?
                  'Buy' :
                  'Owned';
              const runwayBtnClass = ownedRunways < maxRunways ?
                  '' :
                  'disabled';

              const termBtnLabel = ownedTerminals < maxTerminals ?
                  'Buy' :
                  'Owned';
              const termBtnClass = ownedTerminals < maxTerminals ?
                  '' :
                  'disabled';


              if (!isNaN(lat) && !isNaN(lon)) {

                const marker = L.marker([lat, lon]);

                marker.bindPopup(`
              <div class="airport-popup">
                <div class="popup-left">
                  <h3>${name}, ${country}</h3>
                  <p><b>Size:</b> ${size}</p>
                  <p><b>Terminals:</b> <span id="owned-terminals">${ownedTerminals}</span> / ${maxTerminals}
                    <span id="ter-con-time">${con_time}</span><br>
                    <span id="ter-cost">${cost}</span><br>
                    <button class="terminalBtn ${termBtnClass}"><span id="terBtnLabel">${termBtnLabel}</span></button>
                  </p>
                </div>

                <div class="popup-right">
                  <p><b>${iata || 'N/A'} / ${icao || 'N/A'}</b></p>
                  <p><b>Profit:</b> ${profit || 0}</p>
                  <p><b>Runways:</b> <span id="owned-runways">${ownedRunways}</span> / ${maxRunways}
                    <span id="run-con-time">${con_time}</span><br>
                    <span id="run-cost">${cost}</span><br>
                    <button class="runwayBtn ${runwayBtnClass}"><span id="runBtnLabel">${runwayBtnLabel}</span></button>
                  </p>
                </div>
              </div>
            `, {maxWidth: 800});

                marker.on('popupopen', (e) => {

                  const popupEl = e.popup.getElement();
                  const runBtn = popupEl.querySelector('.runwayBtn');
                  const termBtn = popupEl.querySelector('.terminalBtn');

                  if (ownedRunways === maxRunways) {
                    popupEl.querySelector('#run-con-time').remove();
                    popupEl.querySelector('#run-cost').remove();
                  }
                  if (ownedTerminals === maxTerminals) {
                    popupEl.querySelector('#ter-con-time').remove();
                    popupEl.querySelector('#ter-cost').remove();
                  }

                  if (runBtn && !runBtn.classList.contains('disabled')) {
                    runBtn.addEventListener('click', async () => {
                      if (!runBtn.classList.contains('disabled')) {
                        fetch(
                            `http://localhost:5000/buyrunway/${player}/${icao}`).
                            then(res => res.json()).then(result => {
                          if (result.purchased !==
                              'You don\'t have enough money!') {
                            const ownedRun = popupEl.querySelector(
                                '#owned-runways');
                            const currentRun = parseInt(ownedRun.textContent);
                            if (currentRun < maxRunways) {
                              ownedRun.textContent = `${currentRun + 1}`;
                            }
                            if (parseInt(ownedRun.textContent) === maxRunways) {
                              runBtn.querySelector(
                                  '#runBtnLabel').textContent = 'Owned';
                              popupEl.querySelector('#run-con-time').remove();
                              popupEl.querySelector('#run-cost').remove();
                              runBtn.classList.add('disabled');
                            }
                          } else {
                            alert(result.purchased);
                          }
                        });
                      }

                    });
                  }

                  if (termBtn && !termBtn.classList.contains('disabled')) {
                    termBtn.addEventListener('click', async () => {
                      if (!termBtn.classList.contains('disabled')) {
                        fetch(
                            `http://localhost:5000/buyterminal/${player}/${icao}`).
                            then(res => res.json()).then(result => {
                          if (result.purchased !==
                              'You don\'t have enough money!') {
                            const ownedTer = popupEl.querySelector('#owned-terminals');
                            const currentTer = parseInt(ownedTer.textContent);
                            if (currentTer < maxTerminals) {
                              ownedTer.textContent = `${currentTer + 1}`;
                            }
                            if (parseInt(ownedTer.textContent) === maxTerminals) {
                              termBtn.querySelector(
                                  '#terBtnLabel').textContent = 'Owned';
                              popupEl.querySelector('#ter-con-time').remove();
                              popupEl.querySelector('#ter-cost').remove();
                              termBtn.classList.add('disabled');
                            }
                          } else {
                            alert(result.purchased);
                          }
                        });
                      }
                    });
                  }
                });

                marker.on('popupclose', (e) => {
                  ownedLayer.clearLayers();
                  fetchOwned(ownedUrl);
                });

                ownedLayer.addLayer(marker);
              }
            });

            if (!map.hasLayer(ownedLayer)) map.addLayer(ownedLayer);
            showingOwned = true;

          }).
          catch(err => console.error(err));

    }

    fetchOwned(ownedUrl);
  } else {
    ownedLayer.clearLayers();
    if (!map.hasLayer(allAirportsLayer)) map.addLayer(allAirportsLayer);
    showingOwned = false;
  }
});


// nappi 2:

const affordableLayer = L.layerGroup();

let showingAffordable = false;

const toggle2 = document.getElementById('toggle2');

toggle2.addEventListener('click', () => {

  if (!showingAffordable) {
    if (map.hasLayer(allAirportsLayer)) map.removeLayer(allAirportsLayer);
    if (map.hasLayer(ownedLayer)) map.removeLayer(ownedLayer);
    affordableLayer.clearLayers();

    fetch(`http://localhost:5000/airports/afford/${player}`).
        then(res => res.json()).
        then(airports => {
          airports.forEach(airport => {
            const name = airport[3];
            const type = airport[2];
            const lat = parseFloat(airport[4]);
            const lon = parseFloat(airport[5]);
            const country = airport[8];
            const municipality = airport[10];
            const iata = airport[12];
            const icao = airport[11];

            if (!isNaN(lat) && !isNaN(lon)) {

              const marker = L.marker([lat, lon]);

              marker.bindPopup(`
            <b>${name}</b><br>
            Type: ${type}<br>
            City: ${municipality}<br>
            Country: ${country}<br>
            IATA: ${iata || 'N/A'}<br>
            ICAO: ${icao || 'N/A'}<br>
            Lat: ${lat}<br>
            Lon: ${lon}
            
            <button class="buyBtn">Buy</button>
          `);
              marker.on('popupopen', (e) => {
                const buyBtn = e.popup.getElement().querySelector('.buyBtn');
                if (buyBtn) {
                  buyBtn.addEventListener('click', () => {
                    alert(`Airport purchased: ${name}`);
                    fetch(
                        `http://localhost:5000/buyairports/${player}/${icao}`).
                        then(res => res.json()).then(data => console.log(data));
                  }, {once: true});
                }
              });
              affordableLayer.addLayer(marker);
            }
          });

          if (!map.hasLayer(affordableLayer)) map.addLayer(affordableLayer);
          showingAffordable = true;
        }).
        catch(err => console.error(err));

  } else {
    affordableLayer.clearLayers();
    if (!map.hasLayer(allAirportsLayer)) map.addLayer(allAirportsLayer);
    showingAffordable = false;
  }
});

const moneyEl = document.getElementById('money');
const profitEl = document.getElementById('profit');
const timeEl = document.getElementById('time');

async function updateStats() {
  try {
    const response = await fetch(`http://localhost:5000/status/${player}`);
    const data = await response.json();

    moneyEl.textContent = Number(data.money).toLocaleString();
    profitEl.textContent = Number(data.profit).toLocaleString();
    timeEl.textContent = Number(data.week).toLocaleString();

  } catch (error) {
    console.error('Server not responding:', error);
  }
}


setInterval(updateStats, 1000);

// pause nappi

pauseBtn.addEventListener('click', async () => {
  // pause
  if (!isPaused) {
    await fetch('http://localhost:5000/pause', {method: 'POST'});

    pauseBtn.classList.remove('pause');
    pauseBtn.classList.add('play');
    isPaused = true;

  } else {
    // resume
    await fetch('http://localhost:5000/resume', {method: 'POST'});

    pauseBtn.classList.remove('play');
    pauseBtn.classList.add('pause');

    isPaused = false;
  }
});

pauseBtn.classList.add('pause');

//nopeus nappi

const speedBtn = document.getElementById('speed');
let slowMode = false;

speedBtn.addEventListener('click', () => {
  slowMode = !slowMode;

  if (slowMode) {
    // nopeampi
    speedBtn.classList.remove('normal');
    speedBtn.classList.add('slow');

    fetch('http://localhost:5000/set_speed/slow');
  } else {
    // vaihtaa takaisin normaaliin nopeuteen
    speedBtn.classList.remove('slow');
    speedBtn.classList.add('normal');

    fetch('http://localhost:5000/set_speed/normal');
  }

});

async function tickPoll() {
  if (!isPaused) {
    await checkRunningEvent();
    await checkNewEvent();
  }
}

if (slowMode) {
  setInterval(tickPoll, 10000);
}
else {
  setInterval(tickPoll, 3000);
}
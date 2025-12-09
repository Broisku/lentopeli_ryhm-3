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

const toggle1 = document.getElementById('toggle1');

const player = getPlayerName();

document.getElementById('player_name').textContent = player;

toggle1.addEventListener('click', () => {

  if (!showingOwned) {
    if (map.hasLayer(allAirportsLayer)) map.removeLayer(allAirportsLayer);
    ownedLayer.clearLayers();

    fetch(`http://localhost:5000/airports/owned/${player}`).
        then(res => res.json()).
        then(airports => {
          airports.forEach(airport => {
            const type = airport[0];
            const name = airport[1];
            const municipality = airport[2];
            const icao = airport[3];
            const iata = airport[4];
            const lat = parseFloat(airport[6]);
            const lon = parseFloat(airport[7]);

            if (!isNaN(lat) && !isNaN(lon)) {
              const marker = L.marker([lat, lon]);
              marker.bindPopup(`
              <b>${name}</b><br>
              Type: ${type}<br>
              City: ${municipality}<br>
              IATA: ${iata || 'N/A'}<br>
              ICAO: ${icao}<br>
              Lat: ${lat}<br>
              Lon: ${lon}
              <button class="runwayBtn">Buy runway</button>
            `);
              marker.on('popupopen', (e) => {
                const btn = e.popup.getElement().querySelector('.runwayBtn');
                if (btn) {
                  btn.addEventListener('click', () => {
                    alert(`Runway purchased for airport: ${name}`);
                  }, {once: true});
                }
              });
              ownedLayer.addLayer(marker);
            }
          });

          if (!map.hasLayer(ownedLayer)) map.addLayer(ownedLayer);
          showingOwned = true;
        }).
        catch(err => console.error(err));

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
    timeEl.textContent = data.week;

  } catch (error) {
    console.error('Server not responding:', error);
  }
}

setInterval(updateStats, 1000);

// pause nappi

const pauseBtn = document.getElementById('pause');
let isPaused = false;

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
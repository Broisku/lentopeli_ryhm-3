'use strict';

const map = L.map('map').setView([52.52, 13.4], 4);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);



// pause nappi

let slowMode = false;

let isPaused = false;
const pauseBtn = document.getElementById('pause');

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



function getCountryName(isoCode) {
  try {
    const regionNames = new Intl.DisplayNames(['en'], {type: 'region'});
    return regionNames.of(isoCode);
  } catch (e) {
    return isoCode;
  }
}

function getAirportRules(type) {
  if (type === 'small_airport') {
    return {
      name: 'Small Airport',
      price: 3_000_000,
      maxRun: 2, runCost: 1_500_000,
      maxTerm: 1, termCost: 1_500_000,
      conTime: "12 weeks"
    };
  } else if (type === 'medium_airport') {
    return {
      name: 'Medium Airport',
      price: 8_000_000,
      maxRun: 3, runCost: 3_000_000,
      maxTerm: 2, termCost: 6_000_000,
      conTime: "12 weeks"
    };
  } else {

    return {
      name: 'Large Airport',
      price: 15_000_000,
      maxRun: 4, runCost: 4_500_000,
      maxTerm: 3, termCost: 12_000_000,
      conTime: "12 weeks"
    };
  }
}





let isFastMode = false;

const speedBtn = document.getElementById('speed');


speedBtn.classList.add('slow');
speedBtn.classList.remove('normal');

speedBtn.addEventListener('click', () => {

  isFastMode = !isFastMode;

  if (isFastMode) {

    speedBtn.classList.remove('slow');
    speedBtn.classList.add('normal');


    fetch('http://localhost:5000/set_speed/fast');

  } else {

    speedBtn.classList.remove('normal');
    speedBtn.classList.add('slow');


    fetch('http://localhost:5000/set_speed/slow');
  }


  startPolling();
});




let constructionState = {};


async function checkConstructions() {
  try {
    const response = await fetch(`http://localhost:5000/airports/owned/${player}`);
    const airports = await response.json();

    let needsRefresh = false;

    airports.forEach(airport => {


      const name = airport[1];
      const icao = airport[3];
      const runStatus = airport[11];
      const termStatus = airport[14];

      if (constructionState[icao]) {

        if (constructionState[icao].run === 1 && runStatus === 0) {
          alert(`CONSTRUCTION FINISHED: \nRunway at ${name} is now operational!`);
          needsRefresh = true;
        }

        if (constructionState[icao].term === 1 && termStatus === 0) {
          alert(`CONSTRUCTION FINISHED: \nTerminal at ${name} is now operational!`);
          needsRefresh = true;
        }
      }

      constructionState[icao] = { run: runStatus, term: termStatus };
    });

    if (needsRefresh && showingOwned) {

      fetchOwned(`http://localhost:5000/airports/owned/${player}`);
    }

  } catch (error) {
    console.error("Construction Check Error:", error);
  }
}




let pollTimeoutId = null;
let isFetching = false;

async function gameLoop() {

  if (isPaused) {
    pollTimeoutId = setTimeout(gameLoop, 1000);
    return;
  }

  isFetching = true;

  try {
    await updateStats();

    await checkConstructions();

    if (typeof checkRunningEvent === "function") {
      await checkRunningEvent();
    }

    if (typeof checkNewEvent === "function" && !document.querySelector("dialog")) {
      await checkNewEvent();
    }

  } catch (error) {
    console.error("Game Loop Error:", error);
  } finally {
    isFetching = false;
  }


  const delay = slowMode ? 1000 : 1000;
  pollTimeoutId = setTimeout(gameLoop, delay);
}

function startPolling() {

  if (!isFetching) {
    if (pollTimeoutId) clearTimeout(pollTimeoutId);
    gameLoop();
  }
}




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




const toggle1 = document.getElementById('toggle1');

const player = getPlayerName();

document.getElementById('player_name').textContent = player;



function updateButtonStyles() {
  toggle1.style.backgroundColor = showingOwned ? 'gold' : '';
  toggle2.style.backgroundColor = showingAffordable ? 'gold' : '';
}





function fetchOwned(url) {
  ownedLayer.clearLayers();
  fetch(url)
  .then(res => res.json())
  .then(airports => {
    airports.forEach(airport => {

      const [typeRaw, name, , icao, iata, , lat, lon, profit, isoCountry,
        ownedRun, isRunBuilding, , ownedTerm, isTermBuilding] = airport;

      const rules = getAirportRules(typeRaw);
      const countryName = getCountryName(isoCountry);

      const isRunMaxed = (ownedRun || 0) >= rules.maxRun;
      const isTermMaxed = (ownedTerm || 0) >= rules.maxTerm;

      let runBtnText = "Buy Runway";
      let runBtnClass = "";
      let runDisabled = false;
      let runStatusHTML = "";

      if (isRunBuilding === 1) {
        runBtnText = "Constructing...";
        runBtnClass = "disabled";
        runDisabled = true;
        runStatusHTML = `<div class="construction-status">Construction in progress...</div>`;
      } else if (isRunMaxed) {
        runBtnText = "Max Reached";
        runBtnClass = "disabled";
        runDisabled = true;
      }

      let termBtnText = "Buy Terminal";
      let termBtnClass = "";
      let termDisabled = false;
      let termStatusHTML = "";

      if (isTermBuilding === 1) {
        termBtnText = "Constructing...";
        termBtnClass = "disabled";
        termDisabled = true;
        termStatusHTML = `<div class="construction-status">Construction in progress...</div>`;
      } else if (isTermMaxed) {
        termBtnText = "Max Reached";
        termBtnClass = "disabled";
        termDisabled = true;
      }

      if (!isNaN(lat) && !isNaN(lon)) {
        const marker = L.marker([lat, lon]);

        marker.bindPopup(`
            <div class="airport-popup-grid">
              
              <div class="popup-header">
                <div class="header-left">
                  <h3>${name}</h3>
                  <div class="country-name">${countryName}</div>
                </div>
                <div class="header-right">
                  <p><b>${iata || '-'} / ${icao || '-'}</b></p>
                  <p>${rules.name}</p>
                  <p class="${profit >= 0 ? 'profit-positive' : 'profit-negative'}">
                    ${Number(profit).toLocaleString()} €
                  </p>
                </div>
              </div>

              <div class="popup-body">
                
                <div class="body-col">
                  <div class="section-title">Terminals</div>
                  <div class="stat-row">Owned: <b>${ownedTerm || 0} / ${rules.maxTerm}</b></div>
                  <div class="stat-row">Cost: ${Number(rules.termCost).toLocaleString()} €</div>
                  <div class="stat-row">Time: ${rules.conTime}</div>
                  ${termStatusHTML}
                  <button class="action-btn terminalBtn ${termBtnClass}">${termBtnText}</button>
                </div>

                <div class="body-col">
                  <div class="section-title">Runways</div>
                  <div class="stat-row">Owned: <b>${ownedRun || 0} / ${rules.maxRun}</b></div>
                  <div class="stat-row">Cost: ${Number(rules.runCost).toLocaleString()} €</div>
                  <div class="stat-row">Time: ${rules.conTime}</div>
                  ${runStatusHTML}
                  <button class="action-btn runwayBtn ${runBtnClass}">${runBtnText}</button>
                </div>

              </div>
            </div>
          `);

        marker.on('popupopen', (e) => {
          const popupEl = e.popup.getElement();
          const runBtn = popupEl.querySelector('.runwayBtn');
          const termBtn = popupEl.querySelector('.terminalBtn');

          if (runBtn && !runDisabled) {
            runBtn.addEventListener('click', () => {
              fetch(`http://localhost:5000/buyrunway/${player}/${icao}`)
              .then(res => res.json())
              .then(result => {
                if(result.purchased.includes("enough")) { alert(result.purchased); return; }
                alert("Runway construction started!");
                marker.closePopup();
                fetchOwned(url);
              });
            });
          }

          if (termBtn && !termDisabled) {
            termBtn.addEventListener('click', () => {
              fetch(`http://localhost:5000/buyterminal/${player}/${icao}`)
              .then(res => res.json())
              .then(result => {
                if(result.purchased.includes("enough")) { alert(result.purchased); return; }
                alert("Terminal construction started!");
                marker.closePopup();
                fetchOwned(url);
              });
            });
          }
        });

        ownedLayer.addLayer(marker);
      }
    });
    if (!map.hasLayer(ownedLayer)) map.addLayer(ownedLayer);
    showingOwned = true;
  })
  .catch(err => console.error(err));
}



toggle1.addEventListener('click', () => {

  if (map.hasLayer(allAirportsLayer)) map.removeLayer(allAirportsLayer);


  ownedLayer.clearLayers();
  affordableLayer.clearLayers();

  if (map.hasLayer(affordableLayer)) map.removeLayer(affordableLayer);

  if (!showingOwned) {

    showingOwned = true;
    showingAffordable = false;


    fetchOwned(`http://localhost:5000/airports/owned/${player}`);

  } else {

    showingOwned = false;


    if (!map.hasLayer(allAirportsLayer)) map.addLayer(allAirportsLayer);
  }

  updateButtonStyles();
});




// nappi 2:

const affordableLayer = L.layerGroup();

let showingAffordable = false;

const toggle2 = document.getElementById('toggle2');



toggle2.addEventListener('click', () => {
  if (map.hasLayer(allAirportsLayer)) map.removeLayer(allAirportsLayer);
  ownedLayer.clearLayers();
  affordableLayer.clearLayers();

  if (!showingAffordable) {
    fetch(`http://localhost:5000/airports/afford/${player}`)
    .then(res => res.json())
    .then(airports => {
      airports.forEach(airport => {

        const typeRaw = airport[2];
        const name = airport[3];
        const lat = parseFloat(airport[4]);
        const lon = parseFloat(airport[5]);
        const isoCountry = airport[8];
        const icao = airport[11];
        const iata = airport[12];

        const rules = getAirportRules(typeRaw);
        const countryName = getCountryName(isoCountry);

        if (!isNaN(lat) && !isNaN(lon)) {
          const marker = L.marker([lat, lon]);


          marker.bindPopup(`
                <div class="airport-popup-grid">
                  <div class="popup-header">
                    <div class="header-left">
                      <h3>${name}</h3>
                      <div class="country-name">${countryName}</div>
                    </div>
                    <div class="header-right">
                      <p><b>${iata || '-'} / ${icao || '-'}</b></p>
                      <p>${rules.name}</p>
                      <p>Price: <b>${Number(rules.price).toLocaleString()} €</b></p>
                    </div>
                  </div>

                  <div class="popup-body">
                    
                    <div class="body-col">
                      <div class="section-title">Potential Terminals</div>
                      <div class="stat-row">Max Capacity: <b>${rules.maxTerm}</b></div>
                      <div class="stat-row">Cost per unit: ${Number(rules.termCost).toLocaleString()} €</div>
                    </div>

                    <div class="body-col">
                      <div class="section-title">Potential Runways</div>
                      <div class="stat-row">Max Capacity: <b>${rules.maxRun}</b></div>
                      <div class="stat-row">Cost per unit: ${Number(rules.runCost).toLocaleString()} €</div>
                    </div>

                  </div>
                  <button class="action-btn buyAirportBtn" style="margin: 0 20px 20px 20px; width: auto;">
                    Buy Airport (${Number(rules.price).toLocaleString()} €)
                  </button>
                </div>
              `);

          marker.on('popupopen', (e) => {
            const buyBtn = e.popup.getElement().querySelector('.buyAirportBtn');
            if (buyBtn) {
              buyBtn.addEventListener('click', async () => {

                await fetch(`http://localhost:5000/buyairports/${player}/${icao}`);
                alert(`Airport purchased: ${name}`);


                affordableLayer.removeLayer(marker);
                ownedLayer.clearLayers();
                showingOwned = false;
              }, { once: true });
            }
          });

          affordableLayer.addLayer(marker);
        }
      });

      if (!map.hasLayer(affordableLayer)) map.addLayer(affordableLayer);
      showingAffordable = true;
      showingOwned = false;
      updateButtonStyles();
    })
    .catch(err => console.error(err));

  } else {
    showingAffordable = false;
    if (!map.hasLayer(allAirportsLayer)) map.addLayer(allAirportsLayer);
    updateButtonStyles();
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


startPolling();
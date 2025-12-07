'use strict';

const map = L.map('map').setView([52.52, 13.4], 4);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

const allAirportsLayer = L.layerGroup().addTo(map)

// haetaan lentokentät python apista
fetch("http://127.0.0.1:5000/airports")
.then(res => res.json())
.then(airports => {
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
            IATA: ${iata || "N/A"}<br>
            ICAO: ${icao || "N/A"}<br>
            Lat: ${lat}<br>
            Lon: ${lon}
            
            <button class="buyBtn">Buy</button>
          `)

          allAirportsLayer.addLayer(marker);
          console.log("Owned airports loaded:", airports);

          marker.on("popupopen", (e) => {
            const btn = e.popup.getElement().querySelector(".buyBtn");

            btn.addEventListener("click", () => {
              alert(`Airport purchased: ${name}`);
              console.log({ name, iata, icao, lat, lon });
        });
      })

  }
})
})
.catch(error => console.error(error));


function getPlayerName() {
  const params = new URLSearchParams(window.location.search);
  return params.get("name");
}

const ownedLayer = L.layerGroup();

let showingOwned = false;

const toggle1 = document.getElementById("toggle1");

toggle1.addEventListener("click", () => {
  const player = getPlayerName();
  if (!player) {
    alert("Player not found!");
    return;
  }

  if (!showingOwned) {
    if (map.hasLayer(allAirportsLayer)) map.removeLayer(allAirportsLayer);
    ownedLayer.clearLayers();

    fetch(`http://127.0.0.1:5000/airports/owned/${player}`)
    .then(res => res.json())
    .then(airports => {
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
              IATA: ${iata || "N/A"}<br>
              ICAO: ${icao}<br>
              Lat: ${lat}<br>
              Lon: ${lon}
              <button class="runwayBtn">Buy runway</button>
            `);
          marker.on("popupopen", (e) => {
            const btn = e.popup.getElement().querySelector(".runwayBtn");
            if (btn) {
              btn.addEventListener("click", () => {
                alert(`Runway purchased for airport: ${name}`);
              }, { once: true });
            }
          });
          ownedLayer.addLayer(marker);
        }
      });

      if (!map.hasLayer(ownedLayer)) map.addLayer(ownedLayer);
      showingOwned = true;
    })
    .catch(err => console.error(err));

  } else {
    ownedLayer.clearLayers();
    if (!map.hasLayer(allAirportsLayer)) map.addLayer(allAirportsLayer);
    showingOwned = false;
  }
});
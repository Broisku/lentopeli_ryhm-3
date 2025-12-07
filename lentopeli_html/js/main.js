'use strict';

const map = L.map('map').setView([52.52, 13.4], 4);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

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

      const marker = L.marker([lat, lon]).addTo(map);

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
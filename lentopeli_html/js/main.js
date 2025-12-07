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
    const lat = parseFloat(airport[4]);
    const lon = parseFloat(airport[5]);

    if (!isNaN(lat) && !isNaN(lon)) {
      L.marker([lat, lon])
          .addTo(map)
          .bindPopup(`<b>${airport.name}</b>`);
    }
  })
})
.catch(error => console.error(error));
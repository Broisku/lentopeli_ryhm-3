'use strict';

document.getElementById("name-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const player = document.getElementById("new-player").value.trim();
    if (!player) return alert("Enter your name!");

    try {
        const res = await fetch("http://localhost:5000/create_player", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({name: player})
        });
        const data = await res.json();
        console.log(data.message);

        window.location.href = `game.html?name=${encodeURIComponent(player)}&submit=Start`;
      } catch (err) {
          console.error(err);
          alert("Failed to create player.");
      }
});
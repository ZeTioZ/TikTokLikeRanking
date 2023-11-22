var like_ranking = document.getElementById("like_ranking");

function updater() {
  fetch('/data')
  .then(response => response.text())
  .then(text => (like_ranking.innerHTML = text));
}

setInterval(updater, 1000);
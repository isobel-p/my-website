window.addEventListener("load", (event) => {
  new cursoreffects.trailingCursor();
});

const audio = document.getElementById('music');
const btn = document.getElementById('music-button');

let playing = false;

  audio.src = "/music.mp3";

btn.addEventListener('click', () => {
    playing = !playing;
    if (playing) {
    audio.play();
    btn.textContent = '🥳';
    } else {
    audio.pause();
    btn.textContent = '🤫';
    }
});
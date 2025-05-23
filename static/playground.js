window.addEventListener("load", (event) => {
  new cursoreffects.trailingCursor();
});

const audio = document.getElementById('music');
const btn = document.getElementById('music-button');

let playing = false;

audio.src = 'https://cloud-dx9y4rk8f-hack-club-bot.vercel.app/5drunk_raccoon_audio.mp4';

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
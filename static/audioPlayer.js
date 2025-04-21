function toggleAudioPlayer() {
    const container = document.getElementById('audio-player-container');
    const audio = document.getElementById('chord-audio');
  
    if (container.classList.contains('hidden-audio')) {
        container.classList.remove('hidden-audio');
        container.classList.add('show-audio');
        audio.play();
    } else {
        audio.pause();
        audio.currentTime = 0;
        container.classList.remove('show-audio');
        container.classList.add('hidden-audio');
    }
}  
$(document).ready(function () {
    const localChordId = window.chordId;
    const entryTime = new Date();
    let audioPlayed = false;
    
    // Log entry time using jQuery AJAX
    $.ajax({
        url: '/log-chord-access',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            event: 'entered',
            chord_name: chordName,
            timestamp: entryTime.toLocaleTimeString('en-US')
        })
    });
    
    // Track when audio is played
    $('#play-audio').on('click', function() {
        audioPlayed = true;
        
        // Log audio playback
        $.ajax({
            url: '/log-chord-access',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                event: 'played_audio',
                chord_name: chordName,
                timestamp: new Date().toLocaleTimeString('en-US')
            })
        });
    });
    
    // Track audio completion
    $('#chord-audio').on('ended', function() {
        $.ajax({
            url: '/log-chord-access',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                event: 'completed_audio',
                chord_name: chordName,
                timestamp: new Date().toLocaleTimeString('en-US')
            })
        });
    });
    
    // Function to mark chord as completed
    function markChordCompleted(exitTime, formattedDuration) {
        // If they spent at least 5 seconds and/or played the audio, mark as completed
        const timeSpentMs = exitTime - entryTime;
        const seconds = Math.floor(timeSpentMs / 1000);
        
        if (seconds >= 5 || audioPlayed) {
            $.ajax({
                url: '/log-chord-access',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    event: 'completed',
                    chord_name: chordName,
                    timestamp: exitTime.toLocaleTimeString('en-US'),
                    duration: formattedDuration
                })
            });
        }
    }
    
    // Log exit time using sendBeacon with stringified data
    $(window).on('beforeunload', function () {
        const exitTime = new Date();
        const timeSpentMs = exitTime - entryTime;
        const seconds = Math.floor(timeSpentMs / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        const formattedDuration = `${hours}h ${minutes % 60}m ${seconds % 60}s`;
        
        // Mark as completed before leaving
        markChordCompleted(exitTime, formattedDuration);
        
        const payload = JSON.stringify({
            event: 'exited',
            chord_name: chordName,
            timestamp: exitTime.toLocaleTimeString('en-US'),
            duration: formattedDuration
        });
        
        const blob = new Blob([payload], { type: 'application/json' });
        navigator.sendBeacon('/log-chord-access', blob);
    });
});
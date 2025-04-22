$(document).ready(function () {
    const localChordId = window.chordId;
    const entryTime = new Date();

    // Log entry time using jQuery AJAX
    $.ajax({
        url: '/log-chord-access',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            event: 'entered',
            chord_id: chordId,
            timestamp: entryTime.toLocaleTimeString('en-US')
        })
    });

    // Log exit time using sendBeacon with stringified data
    $(window).on('beforeunload', function () {
        const exitTime = new Date();
        const timeSpentMs = exitTime - entryTime;
        const seconds = Math.floor(timeSpentMs / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        const formattedDuration = `${hours}h ${minutes % 60}m ${seconds % 60}s`;

        const payload = JSON.stringify({
            event: 'exited',
            chord_id: chordId,
            timestamp: exitTime.toLocaleTimeString('en-US'),
            duration: formattedDuration
        });

        const blob = new Blob([payload], { type: 'application/json' });
        navigator.sendBeacon('/log-chord-access', blob);
    });
});
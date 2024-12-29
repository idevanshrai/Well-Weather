function updateDateTime() {
    const now = new Date();
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' };
    const dateTimeStr = now.toLocaleDateString('en-US', options);
    document.getElementById('datetime').textContent = dateTimeStr;
}

setInterval(updateDateTime, 1000);
updateDateTime();

function updateDateTime() {
    const now = new Date();
    const options = {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    };
    const dateTimeStr = now.toLocaleString('en-US', options);
    const dateTimeElem = document.getElementById('datetime');
    if (dateTimeElem) {
        dateTimeElem.textContent = dateTimeStr;
    }
}


function setWeatherTheme(weatherDescription) {
    const container = document.getElementById('weather-container');
    if (container) {
        // Normalize description to lowercase for consistent checking
        const normalizedDescription = weatherDescription.toLowerCase();
        if (normalizedDescription.includes('clear')) {
            container.className = 'sunny';
        } else if (normalizedDescription.includes('rain')) {
            container.className = 'rainy';
        } else if (normalizedDescription.includes('cloud')) {
            container.className = 'cloudy';
        } else if (normalizedDescription.includes('snow')) {
            container.className = 'snowy';
        } else {
            container.className = ''; // Default to no specific class
        }
    }
}

function renderTemperatureGraph(temperatureData) {
    const canvas = document.getElementById('tempChart');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: temperatureData.timestamps,
                datasets: [{
                    label: 'Temperature (°C)',
                    data: temperatureData.temps,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: false,
                        title: {
                            display: true,
                            text: 'Temperature (°C)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Time'
                        }
                    }
                }
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Update the date and time every second
    updateDateTime();
    setInterval(updateDateTime, 1000);

    // Placeholder data; replace with dynamic data from an API or server
    const weatherDescription = "clear skies"; // Replace with actual weather data
    setWeatherTheme(weatherDescription);

    // Placeholder temperature data; replace with actual data from an API or server
    const temperatureData = {
        temps: [25, 26, 27], // Replace with actual temperature data
        timestamps: ['8 AM', '12 PM', '4 PM'] // Replace with actual timestamps
    };
    renderTemperatureGraph(temperatureData);
});

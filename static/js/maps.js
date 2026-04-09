// Inicializa o mapa focado em Midtown Manhattan
const map = L.map('map', {
    attributionControl: false,
    scrollWheelZoom: false,
    smoothWheelZoom: true,
    zoomControl: true
}).setView([-23.5384907945773, -46.65394544656181], 19);

L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    subdomains: 'abcd',
    maxZoom: 20
}).addTo(map);

// Modifica o link de Leaflet no canto inferior para que seja aberto em uma nova aba
document.addEventListener('click', function (e) {
    const link = e.target.closest('.leaflet-control-attribution a');
    if (link) {
        e.preventDefault();
        window.open(link.href, '_blank', 'noopener,noreferrer');
    }
}, true);

const overlay = document.getElementById('map-overlay');
const mapDiv = document.getElementById('map');

mapDiv.addEventListener('wheel', function(e) {
    if (e.ctrlKey) {
        e.preventDefault();
        map.scrollWheelZoom.enable();
        overlay.style.display = 'none';
    } else {
        map.scrollWheelZoom.disable();
        overlay.style.display = 'flex';
        
        clearTimeout(window.overlayTimer);
        window.overlayTimer = setTimeout(() => {
            overlay.style.display = 'none';
        }, 1500);
    }
}, { passive: false });

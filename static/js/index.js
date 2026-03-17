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

const iconBlue = L.divIcon({
    // iconUrl: 'path-to-image.png'
    className: 'bi bi-geo-alt-fill marker-color-blue',
    iconSize: [33, 33],
    iconAnchor: [16, 24]
});
const iconGreen = L.divIcon({
    className: 'marker-color-green',
    iconSize: [25, 25],
    iconAnchor: [8, 8]
});
const iconPurple = L.divIcon({
    className: 'marker-color-purple',
    iconSize: [25, 25],
    iconAnchor: [8, 8]
});

const locais = [
    {
        nome: "Dona Elisa Restaurante",
        coords: [-23.538264931051398, -46.653986235576866],
        url: "https://www.timessquarenyc.org/"
    },
    {
        nome: "Empire State Building",
        coords: [-23.538810951797632, -46.654006728343425],
        url: "https://www.esbnyc.com/pt"
    },
    {
        nome: "Central Park (The Lake)",
        coords: [40.7758, -73.9712],
        url: "https://www.centralparknyc.org/"
    },
    {
        nome: "Grand Central Terminal",
        coords: [40.7527, -73.9772],
        url: "https://www.grandcentralterminal.com/"
    }
];

locais.forEach(local => {

    // let IconColor;
    // switch()

    const marker = L.marker(local.coords, { icon: iconBlue }).addTo(map);
    
    marker.bindPopup(`<b>${local.nome}</b><br>Clique para visitar.`);

    marker.on('click', () => {
        setTimeout(() => {
            window.open(local.url, '_blank');
        }, 300);
    });
});

// Adiciona o controle de atribuição de volta de forma discreta
L.control.attribution({ position: 'bottomright' }).addTo(map);
// ─── Configuração ─────────────────────────────────────────────────────────────
const OPENCAGE_KEY = '';
const METRO_RADIUS = 1500; // Raio de busca em metros (5km)

const icons = {
    blue: L.divIcon({
        className: 'bi bi-geo-alt-fill marker-color-blue',
        iconSize: [32, 32],
        iconAnchor: [16, 24]
    }),
    metro: L.divIcon({
      className: 'metro-icon',
      html: '🚇',
      iconSize: [32, 32],
      iconAnchor: [16, 32], // Ancorado na base do emoji
      popupAnchor: [0, -30]
  })
};

// Camadas do mapa para fácil limpeza
let mapLayers = L.layerGroup().addTo(map);
let tempCoords = null;

const elements = {
    latManual: document.getElementById('cordenadas_lat'),
    lngManual: document.getElementById('cordenadas_lng'),
    cep: document.getElementById('cep'),
    numero: document.getElementById('numero'),
    bairro: document.getElementById('bairro'),
    status: document.getElementById('status-busca'),
    inputMetro: document.getElementById('metros_ate_o_metro_mais_proximo')
};

// ─── Helpers ──────────────────────────────────────────────────────────────────
const updateStatus = (msg) => elements.status.innerText = msg;

async function request(url) {
    const res = await fetch(url);
    if (!res.ok) throw new Error('Falha na requisição');
    return res.json();
}

// ─── Fluxo Principal ──────────────────────────────────────────────────────────
async function buscarEndereco() {
    if (elements.latManual && elements.lngManual && elements.latManual.value && elements.lngManual.value) {
        const latM = parseFloat(elements.latManual.value);
        const lngM = parseFloat(elements.lngManual.value);

        updateStatus('Usando coordenadas manuais...');
        mapLayers.clearLayers();
        try {
            // Geocodificação reversa para confirmar o local exato
            const data = await request(`https://photon.komoot.io/reverse?lat=${latM}&lon=${lngM}`);
            const infos = data.features?.[0]?.properties;
            
            // Monta o endereço retornado pela coordenada para conferência do usuário
            const enderecoConfirmado = infos 
                ? `${infos.name || ''} ${infos.housenumber || ''}, ${infos.city || ''}, ${infos.cep || ''}`.trim()
                : "Endereço não identificado nesta coordenada";

            await renderizarResultado(
                latM, 
                lngM, 
                `📍 <b>Coordenadas Manuais Utilizadas</b><br>Confirmado no mapa: ${enderecoConfirmado}`, 
                false
            );
        } catch (e) {
            // Se a API de confirmação falhar, ainda posiciona o marcador, mas avisa
            await renderizarResultado(latM, lngM, `📍 <b>Coordenadas Manuais</b><br>Localização forçada pelo usuário`, true);
        }
        return;
    }

    const cep = elements.cep.value.replace(/\D/g, '');
    const numero = elements.numero.value.trim();
    const bairro = elements.bairro.value.trim();

    if (cep.length !== 8) return updateStatus('CEP inválido.');

    try {
        updateStatus('Consultando CEP...');
        mapLayers.clearLayers(); // Limpa busca anterior
        
        const dadosCep = await request(`https://viacep.com.br/ws/${cep}/json/`);
        if (dadosCep.erro) return updateStatus('CEP não encontrado.');

        // Tenta OpenCage, se falhar ou confiança for baixa, cai no Photon automaticamente
        await localizarCoordenadas(dadosCep, numero, bairro);
    } catch (err) {
        updateStatus('Erro na conexão. Verifique sua internet.');
    }
}

async function localizarCoordenadas(dados, num, bairro) {
    updateStatus('Localizando coordenadas...');
    
    const query = `${dados.logradouro}, ${num}, ${bairro || dados.bairro}, ${dados.localidade}, ${dados.uf}, Brasil`;
    
    // 1. Tentativa com OpenCage
    try {
        const ocData = await request(`https://api.opencagedata.com/geocode/v1/json?q=${encodeURIComponent(query)}&key=${OPENCAGE_KEY}&countrycode=br&limit=1`);
        const res = ocData.results?.[0];

        if (res && res.confidence >= 7) {
            return renderizarResultado(res.geometry.lat, res.geometry.lng, res.formatted, false);
        }
    } catch (e) { console.error("OpenCage falhou, tentando Photon..."); }

    // 2. Fallback com Photon (mais resiliente para nomes de ruas brasileiros)
    try {
        const phData = await request(`https://photon.komoot.io/api/?q=${encodeURIComponent(query)}&limit=1&bbox=-73.9,-33.8,-28.6,5.3`);
        const feat = phData.features?.[0];

        if (feat) {
            const [lng, lat] = feat.geometry.coordinates;
            const end = `${feat.properties.name || ''}, ${feat.properties.city || ''}`;
            return renderizarResultado(lat, lng, end, true);
        }
    } catch (e) { updateStatus('Erro ao localizar endereço.'); }
}

async function renderizarResultado(lat, lng, endereco, isAprox) {
    tempCoords = { lat, lng };
    
    L.marker([lat, lng], { icon: icons.blue })
        .addTo(mapLayers)
        .bindPopup(`<b>${isAprox ? '⚠️ Aproximado' : '✅ Localizado'}:</b><br>${endereco}`)
        .openPopup();

    map.setView([lat, lng], 16);
    updateStatus(isAprox ? '⚠️ Endereço exato não encontrado (usando aproximado).' : '✅ Endereço encontrado!');

    await processarMetro(lat, lng);
}

// ─── Lógica de Transporte ─────────────────────────────────────────────────────
async function processarMetro(lat, lng) {
    try {
        // Query otimizada: busca estações de metrô e paradas (tram/light_rail podem ser úteis em algumas cidades)
        const query = `[out:json][timeout:25];(node["station"="subway"](around:${METRO_RADIUS},${lat},${lng});node["railway"="station"]["subway"="yes"](around:${METRO_RADIUS},${lat},${lng}););out body;`;
        
        const url = `https://overpass-api.de/api/interpreter?data=${encodeURIComponent(query)}`;
        const data = await request(url);

        // Se não houver elementos, encerra aqui
        if (!data || !data.elements || data.elements.length === 0) {
            updateStatus(elements.status.innerText + '\nℹ️ Nenhum metrô encontrado no raio de ' + METRO_RADIUS + ' metros.');
            return;
        }

        // Cálculo do mais próximo com proteção contra valores nulos
        let metroMaisProximo = null;
        let menorDistancia = Infinity;

        data.elements.forEach(el => {
            const d = calcularDistancia(lat, lng, el.lat, el.lon);
            if (d < menorDistancia) {
                menorDistancia = d;
                metroMaisProximo = { ...el, dist: d };
            }
        });

        if (metroMaisProximo) {
            exibirMetroNoMapa(metroMaisProximo);
        }

    } catch (err) {
        console.error("Erro detalhado Overpass:", err); // Log para você ver o erro real no console (F12)
        updateStatus(elements.status.innerText + '\n⚠️ Falha ao calcular distância do metrô. Tente novamente para incluir essa métrica');
    }
}

function exibirMetroNoMapa(metro) {
    // Verificação de segurança para evitar erro de 'undefined'
    if (!metro || !metro.lat || !metro.lon) return;

    const distReal = Math.round(metro.dist * 1000);
    const distComMargem = Math.ceil(distReal * 1.2); 
    const nome = (metro.tags && metro.tags.name) ? metro.tags.name : 'Estação de Metrô';

    // Adiciona marcador do metrô
    const markerMetro = L.marker([metro.lat, metro.lon], { icon: icons.metro })
        .addTo(mapLayers)
        .bindPopup(`<b>🚇 ${nome}</b><br>Distância estimada: ~${distComMargem}m`);

    // Desenha a linha pontilhada
    L.polyline([[tempCoords.lat, tempCoords.lng], [metro.lat, metro.lon]], {
        color: '#0033a0', 
        dashArray: '5, 10', 
        weight: 2
    }).addTo(mapLayers);

    // Ajusta o zoom para enquadrar o endereço e o metrô
    const group = new L.featureGroup(mapLayers.getLayers());
    map.fitBounds(group.getBounds().pad(0.2));

    // Atualiza interface
    updateStatus(`✅ Concluído! Metrô: ${nome} (~${distComMargem}m)`);
    if (elements.inputMetro) {
        elements.inputMetro.value = distComMargem;
    }
}

function calcularDistancia(lat1, lon1, lat2, lon2) {
    const toRad = x => x * Math.PI / 180;
    const R = 6371;
    const dLat = toRad(lat2 - lat1);
    const dLon = toRad(lon2 - lon1);
    const a = Math.sin(dLat / 2) ** 2 + Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2;
    return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

// ─── Eventos ──────────────────────────────────────────────────────────────────
document.getElementById('btn-buscar').addEventListener('click', buscarEndereco);

// Máscara Simples de CEP
elements.cep.addEventListener('input', e => {
    let v = e.target.value.replace(/\D/g, '');
    if (v.length > 5) v = v.replace(/^(\d{5})(\d)/, '$1-$2');
    e.target.value = v.slice(0, 9);
});
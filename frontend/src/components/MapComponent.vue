<template>
    <div>
        <div ref="map" style="height:700px; width: 100%;"></div>
    </div>
</template>

<script>
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import regionsJson from '@/geojson/Regions.json';

function convertToGeoJSON(regionsJson) {
    const features = [];
    for (const region in regionsJson) {
        const coordinates = regionsJson[region]["0"];

        features.push({
            type: 'Feature',
            properties: { name: region },
            geometry: {
                type: 'Polygon',
                coordinates: [coordinates],
            }
        });
    }
    return {
        type: 'FeatureCollection',
        features,
    };
}

export default {
    data() {
        return {
            map: null,
        };
    },

    mounted() {
        this.initMap();
        this.loadRegions();
    },

    methods: {
        initMap() {
            this.map = L.map(this.$refs.map, { attributionControl: false }).setView([55.7558, 37.6173], 5);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
                attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
            }).addTo(this.map);
        },

        loadRegions() {
            const geoJsonData = convertToGeoJSON(regionsJson);

            const geoJsonLayer = L.geoJSON(geoJsonData, {
                style: (feature) => ({
                    color: 'green',
                    fillOpacity: 0.5,
                }),
                onEachFeature: (feature, layer) => {
                    layer.on({
                        mouseover: () => this.showPopup(feature, layer),
                        mouseout: () => this.closePopup(),
                        click: () => this.showPopup(feature, layer),
                    });
                }
            }).addTo(this.map);
        },

        highlightRegion(layer) {
            layer.setStyle({
                weight: 5,
                color: '#666',
                dashArray: '',
                fillOpacity: 0.7
            });
        },

        resetHighlight(layer) {
            layer.setStyle({
                weight: 1,
                color: 'green',
                dashArray: '',
                fillOpacity: 0.5
            });
        },

        showPopup(feature, layer) {
            const regionName = feature.properties.name;
            const regionData = this.getRegionData(regionName);
            const popupContent = `
                <div class="popup-content">
                    <h3 style="font-size: 22px; font-weight: 600;">${regionName}</h3>
                    <div class="sources">
                    <a href="${regionData.source1}" target="_blank" style="font-size: 16px; display: block; margin-bottom: 5px;">ИПС Законодательство</a>
                    <a href="${regionData.source2}" target="_blank" style="font-size: 16px; display: block; margin-bottom: 5px;">Pravo.gov.ru</a>
                    <a href="${regionData.source3}" target="_blank" style="font-size: 16px; display: block; margin-bottom: 5px;">МинЮст</a>
                    <a href="${regionData.source4}" target="_blank" style="font-size: 16px; display: block;">orel-region</a>
                    </div>
                </div>
                `;



            L.popup()
                .setLatLng(layer.getBounds().getCenter())
                .setContent(popupContent)
                .openOn(this.map);
        },

        getRegionData(regionName) {

            return {
                source1: 'https://example.com/source1',
                source2: 'https://example.com/source2',
                source3: 'https://example.com/source2',
                source4: 'https://example.com/source2',
            };
        },
    },
};
</script>

<style scoped>
.popup-content h3 {
    margin-top: 0;
}

.popup-content p {
    margin-bottom: 10px;
}

.sources a {
    display: block;
    margin-bottom: 5px;
}

.popup-content {
    padding: 10px;
    font-family: Arial, sans-serif;
}

.popup-content h3 {
    margin-top: 0;
    font-size: 18px;
}

.popup-content p {
    font-size: 16px;
    margin-bottom: 10px;
}

.sources a {
    font-size: 16px;
    display: block;
    margin-bottom: 5px;
}
</style>
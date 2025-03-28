<template>
    <div>
        <div ref="map" style="height: 500px; width: 100%;"></div>
        <div v-if="selectedRegionVar">
            <h3>Данные по региону: {{ selectedRegionVar }}</h3>
        </div>
    </div>
    <p></p>
    <p></p>
    <p></p>
</template>

<script>
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import regionsJson from '@/geojson/Regions.json';
import { selectedRegion } from '@/pinia';

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
            selectedRegionVar: "", //выбранный регион
            activeLayer: null,
            selectedRegionData: null, //данные по региону
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
                attribution: 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
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
                        mouseover: () => this.highlightRegion(layer),
                        mouseout: () => this.resetHighlight(layer),
                        click: async () => {
                            this.selectedRegionVar = feature.properties.name;
                            this.activeLayer = layer;
                            this.setSelectedRegion(this.selectedRegionVar);
                            this.$emit('region-selected', this.selectedRegionVar);
                        }
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

        async setSelectedRegion(region) {
            const store = selectedRegion();
            typeof (region) == "string" ? store.setRegionName(region) : store.setRegionName("");
        },
    },
};
</script>

<style scoped></style>

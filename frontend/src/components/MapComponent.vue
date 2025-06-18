<template>
    <div class="map">
      <div ref="map" style="height: 600px; width: 100%;"></div>
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
  
  // Функция для перевода строки в верхний регистр с учётом русских букв
  function toUpperCaseRU(str) {
    return str.toUpperCase();
  }
  
  export default {
    data() {
      return {
        map: null,
        popup: null,
        regionDataMap: {}, // ключ — название региона в верхнем регистре
      };
    },
  
    async mounted() {
      await this.fetchRegionData();
      this.initMap();
      this.loadRegions();
    },
  
    methods: {
      async fetchRegionData() {
        try {
          const response = await fetch('/api/regions/map_data/');
          if (!response.ok) throw new Error('Ошибка загрузки данных регионов');
          const data = await response.json();
          // Ключи — в верхнем регистре для корректного сопоставления
          this.regionDataMap = data.reduce((acc, item) => {
            acc[toUpperCaseRU(item.region_name)] = item;
            return acc;
          }, {});
        } catch (error) {
          console.error(error);
          this.regionDataMap = {};
        }
      },
  
      initMap() {
        this.map = L.map(this.$refs.map, { attributionControl: false }).setView([55.7558, 37.6173], 5);
  
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          maxZoom: 19,
          attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
        }).addTo(this.map);
      },
  
      loadRegions() {
        const geoJsonData = convertToGeoJSON(regionsJson);
  
        L.geoJSON(geoJsonData, {
          style: () => ({
            color: 'green',
            fillOpacity: 0.5,
            weight: 1,
          }),
          onEachFeature: (feature, layer) => {
            layer.on({
              mouseover: () => {
                this.highlightRegion(layer);
                this.showPopup(feature, layer);
              },
              mouseout: () => {
                this.resetHighlight(layer);
                this.closePopup();
              },
              click: () => {
                this.highlightRegion(layer);
                this.showPopup(feature, layer);
              },
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
        // Название региона в верхнем регистре
        const regionName = toUpperCaseRU(feature.properties.name);
        const regionData = this.regionDataMap[regionName] || null;
  
        const publCount = regionData ? regionData.published_count : 'нет данных';
        const sources = regionData ? regionData.sources : {};
  
        const popupContent = `
          <div class="popup-content">
            <h3 style="font-size: 22px; font-weight: 600;">${feature.properties.name}</h3>
            <h2 style="font-size: 22px; font-weight: 600;">
              За последние сутки опубликовано: ${publCount}
            </h2>
            <div class="sources">
              <a href="${sources.source1 || '#'}" target="_blank" style="font-size: 16px; display: block; margin-bottom: 5px;">ИПС Законодательство</a>
              <a href="${sources.source2 || '#'}" target="_blank" style="font-size: 16px; display: block; margin-bottom: 5px;">Pravo.gov.ru</a>
              <a href="${sources.source3 || '#'}" target="_blank" style="font-size: 16px; display: block; margin-bottom: 5px;">МинЮст</a>
              <a href="${sources.source4 || '#'}" target="_blank" style="font-size: 16px; display: block;">orel-region</a>
            </div>
          </div>
        `;
  
        if (this.popup) {
          this.map.closePopup(this.popup);
        }
  
        this.popup = L.popup()
          .setLatLng(layer.getBounds().getCenter())
          .setContent(popupContent)
          .openOn(this.map);
      },
  
      closePopup() {
        if (this.popup) {
          this.map.closePopup(this.popup);
          this.popup = null;
        }
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
  
  .map {
    padding: 25px;
  }
  </style>
  
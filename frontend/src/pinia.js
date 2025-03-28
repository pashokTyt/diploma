/* гуд практика -разделить сторы в разные файлы, не забыть потом сделать */
import { defineStore } from 'pinia';
import axios from 'axios';

export const useSourcesStore = defineStore('sources', {
    state: () => ({
        sources: [],
    }),
    getters: {
        getSources(state) {
            return state.sources;
        },
    },
    actions: {
        async fetchSources() {
            try {
                const response = await axios.get('api/sources/');
                console.log('Полученные источники:', response.data);
                this.sources = response.data.map(source => ({
                    value: source.name,
                    label: source.name,
                    url_address: source.url_address
                }));
            } catch (error) {
                console.error('Ошибка при получении источников:', error);
            }
        },
    },
});

export const useRegionsStore = defineStore('regions', {
    state: () => ({
        regions: [],
    }),
    getters: {
        getRegions(state) {
            return state.regions;
        },
    },
    actions: {
        async fetchRegions() {
            try {
                const response = await axios.get('api/regions/');
                console.log('Полученные регионы:', response.data);
                this.regions = response.data.map(region => ({
                    value: region.code,
                    label: region.name,
                    code: region.code
                }));
            } catch (error) {
                console.error('Ошибка при получении регионов:', error);
            }
        },
    },
});

export const selectedRegion = defineStore('selected_region', {
    state: () => ({
        name: 'Орловская область'
    }),
    getters: {
        getRegionName(state) {
            return state.name.toString()
        },
    },
    actions: {
        setRegionName(regionName) {
            typeof(regionName) == "string" ? this.name = regionName : this.name = "";
        },
    },
});

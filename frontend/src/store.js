/* легаси мусор, использую пинию, пускай этот код для veux лежит тут, вдруг когда-нибудь пригодится */

/* // store.js
import { createStore } from 'vuex';
import axios from 'axios';

const store = createStore({
    state() {
        return {
            regions: [],
            sources: []
        };
    },
    mutations: {
        setRegions(state, regions) {
            state.regions = regions; // Установка регионов
        },
        setSources(state, sources) {
            state.sources = sources; // Установка источников
        }
    },
    actions: {
        async fetchSources({ commit }) { // Используйте контекст для доступа к commit
            try {
                const response = await axios.get('api/sources/'); // Используйте axios напрямую
                console.log('Полученные источники:', response.data); // Отладка
                const sources = response.data.map(source => ({
                    value: source.name,
                    label: source.name,
                    url_address: source.url_address
                }));
                commit('setSources', sources); // Вызов мутации для обновления состояния
            } catch (error) {
                console.error('Ошибка при получении источников:', error);
            }
        },

        async fetchRegions({ commit }) {
            try {
                const response = await axios.get('api/regions/');
                console.log('Полученные регионы:', response.data); // Отладка
                const regions = response.data.map(region => ({
                    value: region.code,
                    label: region.name,
                    code: region.code
                }));
                commit('setRegions', regions);
            } catch (error) {
                console.error('Ошибка при получении регионов:', error);
            }
        },
    },
    getters: {
        getRegions(state) {
            return state.regions;
        },
        getSources(state) {
            return state.sources;
        }
    }
});

export default store;
 */
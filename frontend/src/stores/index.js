import { defineStore } from 'pinia'

export const useStore = defineStore({
    id: 'store',
    state: () => ({
        infoContentBoxData: {
            infoBoxHeight: 35,
            contentBoxHeight: 65,

        }

        
    }),
    getters: {
        getStoreData(state){
            return state.infoContentBoxData
        }
    }
})
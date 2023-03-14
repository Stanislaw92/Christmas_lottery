<template>
	<base-layout page-title="Lottery"
    page-default-back-link='/'> 
        <participant-list
            :participants="participants"
			@deletePart="deletePart"
        />
        <div class="bottomLotteryPart">
			<div class="flexCenterPart">
				<button class="cardPart" id="open-modal-part">
					<ion-icon
						size="large"
						slot="icon-only"
						:icon="add"
						color="light"
					></ion-icon>
				</button>
				<create-participant-modal 
                    :uuid = "uuid"
                    @refreshParticipants="getParticipants"
                />
			</div>
		</div>
    </base-layout>
</template>

<script>
import ParticipantList from '../components/ParticipantList.vue';
import CreateParticipantModal from '../components/CreateParticipantModal.vue';
import { axios } from '@/common/api.service.js';
import { add } from 'ionicons/icons';
import {
	// IonButton,
	IonIcon,
} from '@ionic/vue';

export default {
    props:{
        uuid: {
            type: String,
            required: true
        }
    },
	components: {
        ParticipantList,
        CreateParticipantModal,
        IonIcon,
        },
    data() {
        return {
            participants: [],
            loadingLotteries: false,
            add,

        }
    },
    methods: {
		async deletePart(partData){
			const endpoint = `/api/v1/participants/${partData.uuid}/`
			try {
				await axios.delete(endpoint)
				this.participants.splice(this.participants.indexOf(partData), 1)
			} catch (error) {
				console.log(error.response);
			}
		},
        async getParticipants(){
            this.participants = []
            let endpoint = `/api/v1/lotteries/${this.uuid}/participants/`;
            try {
				const response = await axios.get(endpoint);
				this.participants.push(...response.data.results);
				this.loadingLotteries = false;
			} catch (error) {
				console.log(error.response);
			}
        }
    },
    created(){
        this.getParticipants()
    }
};

</script>
\
<style>
.bottomLotteryPart {
	width: 80px;
	padding: 20px 0px;
	position: fixed;
	left: 50%;
	transform: translate(-50%);
	bottom: 0;
	right: 0;
}
.flexCenterPart {
	width: 80px;
	align-self: center;
	justify-self: center;
	display: flex;
	justify-content: center;
}

.cardPart {
	position: relative;
	box-sizing: border-box;
	width: 80px;
	height: 80px;
	background: rgb(67, 15, 15);
	border: 1px solid white;
	border-radius: 17px;
	text-align: center;
	cursor: pointer;
	display: flex;
	align-items: center;
	justify-content: center;
	font-weight: bolder;
}

.cardPart:hover {
	border: 1px solid black;
	transform: scale(1.05);
}

.cardPart:active {
	transform: scale(0.95) rotateZ(1.7deg);
}
</style>
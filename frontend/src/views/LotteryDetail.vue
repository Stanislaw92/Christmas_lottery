<template>
	<base-layout page-title="Lottery"
    page-default-back-link='/'> 
	<template v-slot:actions-end>
		<ion-button @click="presentLotteryAlert">
			<ion-icon slot="icon-only" :icon="dice"></ion-icon>
		</ion-button>
	</template>
		<div
			v-if="numOfPart < 4"
			class="partInfo"
		>
			Add atleast 4 participants to start lottery

		</div>
        <participant-list
            :participants="participants"
			@deletePart="deletePart"
        />
        <div class="bottomLotteryPart">
			<div class="flexCenterPart">
				<button class="cardPart" id="open-modal-part">
					<div 
						v-if="numOfPart < 4"
						class="underBtn">
					</div>
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
					@addPart = "addPart"
                />
			</div>
		</div>
    </base-layout>
</template>

<script>
import ParticipantList from '../components/ParticipantList.vue';
import CreateParticipantModal from '../components/CreateParticipantModal.vue';
import { axios } from '@/common/api.service.js';
import { add, dice } from 'ionicons/icons';
import {
	IonButton,
	IonIcon,
	alertController,
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
		IonButton,
		
        },
    data() {
        return {
			lottery: null,
            participants: [],
            loadingLotteries: false,
            add,
			dice,
			numOfPart: 0,

        }
    },
    methods: {
		addPart(){
			this.numOfPart += 1
		},
		async getLottery(){
			const endpoint = `/api/v1/lotteries/${this.uuid}/`
			try {
				const response = await axios.get(endpoint)
				this.lottery = response.data
				this.numOfPart = this.lottery.num_of_participants
			} catch (error) {
				console.log(error)
			}
		},
		async deletePart(partData){
			const endpoint = `/api/v1/participants/${partData.uuid}/`
			try {
				await axios.delete(endpoint)
				this.participants.splice(this.participants.indexOf(partData), 1)
				this.numOfPart -= 1
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
        },
		async presentLotteryAlert(){
			const alert = await alertController.create({
			header: 'Starting lottery info',
			subHeader: 'do you want to start new lottery?',
			buttons: ['START NEW LOTTERY'],
			inputs: [
				{
					type: 'checkbox',
					label: 'Send emails with results',
					value: 'radioone',
					checked: true
				},
				{
					type: 'checkbox',
					label: 'Send sms with results',
					value: 'radiotwo',
					checked: false
				},

			],
			});

			await alert.present();
		}
	},
    created(){
        this.getParticipants()
		this.getLottery()
    }
};

</script>
\
<style>
.partInfo {
	position: fixed;
	padding: 20px 20px;
	color: rgba(255, 255, 255, 0.839);
	height: 50px;
	width: 90%;
	display: flex;
	justify-content: center;
	align-items: center;
	border: 1px solid #3cff00;
	box-shadow: 0px 0px 35px #3cff00;
	border-radius: 15px;
	left: 50%;
	bottom: 120px;
	transform: translate(-50%);
	background: rgba(0, 0, 0, 0.766);
}

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

.underBtn {
	position: absolute;
	border-radius: 17px;
	z-index: -1;
	background: #3cff00;
	width: 82px;
	height: 82px;
	box-shadow: 0px 0px 35px #3cff00
}

.cardPart:hover {
	border: 1px solid black;
	transform: scale(1.05);
}

.cardPart:active {
	transform: scale(0.95) rotateZ(1.7deg);
}
</style>
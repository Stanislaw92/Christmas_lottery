<template>
	<base-layout
		page-title="Lottery"
		page-default-back-link="/"
		:infoBoxHeight="infoBoxHeight"
		:contentBoxHeight="contentBoxHeight"
	>
		<template v-slot:actions-end1>
			<ion-button id="open-modal-part">
				<ion-icon slot="icon-only" :icon="add"></ion-icon>
				<create-participant-modal
					:uuid="uuid"
					@refreshParticipants="getParticipants"
					@addPart="addPart"
				/>
			</ion-button>
		</template>
		<template v-slot:actions-end>
			<ion-button v-if="!isResult" @click="checkLotteryStart">
				<ion-icon slot="icon-only" :icon="dice"></ion-icon>
			</ion-button>
			<ion-button v-else @click="pushToResultDetails">
				<ion-icon slot="icon-only" :icon="clipboard"></ion-icon>
			</ion-button>
		</template>
		
		<template v-slot:actions-end2>
			<ion-button
				@click = "showInfo"
				class="infoIconTrans"
				:style="infoIconVisibility">
				<i class="fa-solid fa-info" style="color: black;"></i>
			</ion-button>
		</template>

		<template v-slot:info-slot>
			<div class="infoContainer">
				<div v-if="waitForLottery" class="infoBody loaderSize">
					<div class="loader"></div>
					<p class="loadingText"> sending emails.. </p>
				</div>
				<div v-else class="infoBody" :style="displayInfoVisible">
					
					<div v-if="isResult">
						<div class="textField">
							You already start your lottery, to check result click on the board
							icon in the top right corner!<br>
							total participants: <b><span style="font-size: 13px;font-family: 'Arial';">{{totalParticipants}}
							</span></b>
						</div>
					</div>
					<div v-else>
						<div
							v-if="totalParticipants >= 4"
							class="textField"
						>
							To start lottery click on the roll icon in the top right corner!<br>
							total participants: <b><span style="font-size: 13px;font-family: 'Arial';">{{totalParticipants}}
							</span></b>				
						</div>
						<div v-else class="textField">
							To start lottery add atleast <b>4</b> participants, to do so click on the
							plus icon in the top right corner! <br>
							total participants: <b><span style="font-size: 13px;font-family: 'Arial';">{{totalParticipants}}
							</span></b>
						</div>
					</div>
					<div >
						<ion-icon
							@click="removeInfo"
							slot="icon-only"
							:icon="close"
						></ion-icon>
					</div>


				</div>
			</div>
		</template>
		<template v-slot:content-slot>

			<participant-list
				style="padding: 20px"
				:participants="participants"
				@deletePart="deletePart"
			/>
		</template>
	</base-layout>
</template>

<script>
import { axios } from '@/common/api.service.js';
import { add, dice, clipboard, close } from 'ionicons/icons';
import CreateParticipantModal from '../components/CreateParticipantModal.vue';
import { useStore } from '../stores';
import ParticipantList from '../components/ParticipantList.vue';
import { IonButton, IonIcon, alertController } from '@ionic/vue';

export default {
	props: {
		uuid: {
			type: String,
			required: true,
		},
	},
	components: {
		ParticipantList,
		CreateParticipantModal,
		IonIcon,
		IonButton,
	},
	data() {
		return {
			isResult: false,
			lottery: null,
			participants: [],
			loadingLotteries: false,
			add,
			dice,
			clipboard,
			close,
			numOfPart: 0,
			emailMsg: false,
			textMsg: false,
			infoBoxHeight: 35,
			contentBoxHeight: 65,
			displayInfoVisible: { visibility: 'visible', opacity: '1' },
			infoIconVisibility: { visibility: 'hidden', opacity: '0' },
			waitForLottery: false,
		};
	},
	computed: {
		totalParticipants() {
			return this.participants.length;
		},
	},
	methods: {
		changeHeightProp(x, y) {
			this.infoBoxHeight = x
			this.contentBoxHeight = y
		},
		removeInfo() {
			this.displayInfoVisible = {visibility: "hidden", opacity: '0'};
			this.changeHeightProp(15, 85)
			this.infoIconVisibility = {visibility: "visible", opacity: '1'}
		},
		showInfo() {
			this.changeHeightProp(35, 65)
			this.infoIconVisibility = {visibility: 'hidden', opacity: '0', transition: "visibility 2s opacity 2s"}
			setTimeout(() => {
				this.displayInfoVisible = {visibility: "visible", opacity: '1', transition: "visibility 0.8s opacity 0.8s"}
			}, 700)
		},
		setResultData() {
			const store = useStore();
			store.lotteryResultData.result = this.participants;
		},
		checkLotteryStart() {
			if (this.participants.length >= 4) {
				this.presentLotteryAlert();
			} else {
				this.notEnaughPartError();
			}
		},
		addPart() {
			this.numOfPart += 1;
		},
		async getLottery() {
			const endpoint = `/api/v1/lotteries/${this.uuid}/`;
			try {
				const response = await axios.get(endpoint);
				this.lottery = response.data;
				this.numOfPart = this.lottery.num_of_participants;
				this.isResult = this.lottery.have_result;
			} catch (error) {
				console.log(error);
			}
		},
		async deletePart(partData) {
			const endpoint = `/api/v1/participants/${partData.uuid}/`;
			try {
				await axios.delete(endpoint);
				this.participants.splice(this.participants.indexOf(partData), 1);
				this.numOfPart -= 1;
			} catch (error) {
				console.log(error.response);
			}
		},
		async getParticipants() {
			this.participants = [];
			let endpoint = `/api/v1/lotteries/${this.uuid}/participants/`;
			try {
				const response = await axios.get(endpoint);
				this.participants.push(...response.data.results);
				this.loadingLotteries = false;
			} catch (error) {
				console.log(error.response);
			}
		},
		async presentLotteryAlert() {
			const alert = await alertController.create({
				header: 'Starting lottery info',
				subHeader: 'do you want to start new lottery?',
				buttons: [
					{
						text: 'START NEW LOTTERY',
						handler: (data) => {
							if (data.includes('emailMsg')) {
								this.emailMsg = true;
							}
							if (data.includes('textMsg')) {
								this.textMsg = true;
							}

							this.getLotteryResults();

							// this.$router.push({
							// 	path: `/lotteryResult/${this.uuid}`,
							// })
						},
					},
				],
				inputs: [
					{
						type: 'checkbox',
						label: 'Send emails with results',
						value: 'emailMsg',
						checked: true,
					},
					{
						type: 'checkbox',
						label: 'Send sms with results',
						value: 'textMsg',
						checked: false,
					},
				],
			});

			await alert.present();
		},
		async getLotteryResults() {
			const endpoint = '/api/v1/lotteryResult/';
			let data = new FormData();

			this.participants.forEach((item) => {
				data.append('participants', JSON.stringify(item));
			});

			data.append('emailMsg', this.emailMsg);
			data.append('textMsg', this.textMsg);
			data.append('uuid', this.uuid);

			try {
				this.waitForLottery = true
				await axios({
					method: 'POST',
					url: endpoint,
					data: data,
				});
				this.waitForLottery = false
				this.getLottery();
			} catch (error) {
				console.log(error);
			}
		},
		async notEnaughPartError() {
			const alert = await alertController.create({
				header: 'You need atleast 4 participants to start lottery!',
				buttons: ['Ok'],
			});

			await alert.present();
		},
		pushToResultDetails() {
			this.$router.push({
				path: `/lotteryResult/${this.lottery.uuid}/`,
			});
		},
	},
	created() {
		this.getParticipants();
		this.getLottery();
	},
	watch: {
		$route(to) {
			if (to.path == `/${this.uuid}/`) {
				this.getLottery();
			}
		},
	},
};
</script>

<style>
.loaderSize {
	width: 150px;
	height: 150px;
	justify-content: space-between;
	align-items: center;
	flex-direction: column;
	padding: 50px 0 0 0;
	margin: 10;
}

.infoIconTrans {
	transition: visibility 0.5s opacity 0.5s;
}

.textField {
	font-family: 'Delicious Handrawn', cursive;
	overflow: scroll;
}
.testContainer {
	display: flex;
	align-items: center;
	justify-content: center;
}

.infoContainer {
	display: flex;
	justify-content: center;
	align-items: center;
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

.underBtn {
	position: absolute;
	border-radius: 17px;
	z-index: -1;
	background: #3cff00;
	width: 82px;
	height: 82px;
	box-shadow: 0px 0px 35px #3cff00;
}

.loader {
  color: rgb(0, 0, 0);
  font-size: 10px;
  width: 1em;
  height: 1em;
  border-radius: 50%;
  position: relative;
  text-indent: -9999em;
  animation: mulShdSpin 1.3s infinite linear;
  transform: translateZ(0);
}

@keyframes mulShdSpin {
  0%,
  100% {
    box-shadow: 0 -3em 0 0.2em, 
    2em -2em 0 0em, 3em 0 0 -1em, 
    2em 2em 0 -1em, 0 3em 0 -1em, 
    -2em 2em 0 -1em, -3em 0 0 -1em, 
    -2em -2em 0 0;
  }
  12.5% {
    box-shadow: 0 -3em 0 0, 2em -2em 0 0.2em, 
    3em 0 0 0, 2em 2em 0 -1em, 0 3em 0 -1em, 
    -2em 2em 0 -1em, -3em 0 0 -1em, 
    -2em -2em 0 -1em;
  }
  25% {
    box-shadow: 0 -3em 0 -0.5em, 
    2em -2em 0 0, 3em 0 0 0.2em, 
    2em 2em 0 0, 0 3em 0 -1em, 
    -2em 2em 0 -1em, -3em 0 0 -1em, 
    -2em -2em 0 -1em;
  }
  37.5% {
    box-shadow: 0 -3em 0 -1em, 2em -2em 0 -1em,
     3em 0em 0 0, 2em 2em 0 0.2em, 0 3em 0 0em, 
     -2em 2em 0 -1em, -3em 0em 0 -1em, -2em -2em 0 -1em;
  }
  50% {
    box-shadow: 0 -3em 0 -1em, 2em -2em 0 -1em,
     3em 0 0 -1em, 2em 2em 0 0em, 0 3em 0 0.2em, 
     -2em 2em 0 0, -3em 0em 0 -1em, -2em -2em 0 -1em;
  }
  62.5% {
    box-shadow: 0 -3em 0 -1em, 2em -2em 0 -1em,
     3em 0 0 -1em, 2em 2em 0 -1em, 0 3em 0 0, 
     -2em 2em 0 0.2em, -3em 0 0 0, -2em -2em 0 -1em;
  }
  75% {
    box-shadow: 0em -3em 0 -1em, 2em -2em 0 -1em, 
    3em 0em 0 -1em, 2em 2em 0 -1em, 0 3em 0 -1em, 
    -2em 2em 0 0, -3em 0em 0 0.2em, -2em -2em 0 0;
  }
  87.5% {
    box-shadow: 0em -3em 0 0, 2em -2em 0 -1em, 
    3em 0 0 -1em, 2em 2em 0 -1em, 0 3em 0 -1em, 
    -2em 2em 0 0, -3em 0em 0 0, -2em -2em 0 0.2em;
  }
}
  
</style>

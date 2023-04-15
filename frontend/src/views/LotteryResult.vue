<template>
	<base-layout page-title="Lottery Result" page-default-back-link="/{{uuid}}" :infoBoxHeight="infoBoxHeight"
		:contentBoxHeight="contentBoxHeight">
		<template v-slot:actions-end>
			<ion-button @click="deteteResultConfirmation">
				<ion-icon slot="icon-only" :icon="trash"></ion-icon>
			</ion-button>
		</template>

		<template v-slot:actions-end1>
			<ion-button
				@click = "showInfo"
				class="infoIconTrans"
				:style="infoIconVisibility">
				<i class="fa-solid fa-info" style="color: black;"></i>
			</ion-button>
		</template>

		<template v-slot:info-slot>
			<div class="infoContainer">
				<div class="infoBody" :style="displayInfoVisible">
						
					<div class="textField">
						Results for lottery:<br><b>{{lotteryName}}</b><br><br>
						To uncover result for each participant, just click on the black field next to the exact name!
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
			<div style="display: flex; justify-content: center; align-items: center">
				<div class="resultCont">
					<div 
						
						class="singleResultCont" v-for="obj in resultsList" 
						:key="obj.uuid"
					>
						{{ obj[0] }} 
						<div>
							<i class="fa-solid fa-gift" style="color: #000000;"></i>&nbsp; 
							<i class="fa-solid fa-arrow-right" style="color: #000000;"></i>
						</div>
						<div
							@click="removeBg" 
							class="result hideResult"
						>
							{{ obj[1] }}
						</div>
					</div>
				</div>
			</div>
			<div v-if="resultLoading">LOADING....</div>
		</template>
	</base-layout>
</template>

<script>
import { trash, close } from 'ionicons/icons';
import { axios } from '@/common/api.service.js';
import { IonButton, IonIcon, alertController } from '@ionic/vue';
// import { useStore } from '../stores';
export default {
	props: ['uuid'],
	components: {
		IonButton,
		IonIcon,
	},
	data() {
		return {
			resultLoading: false,
			result: null,
			resultsList: [],
			trash,
			close,
			resultUuid: null,
            lotteryName: null,
			infoBoxHeight: 35,
			contentBoxHeight: 65,
			displayInfoVisible: { visibility: 'visible', opacity: '1' },
			infoIconVisibility: { visibility: 'hidden', opacity: '0' },
		};
	},
	methods: {
		removeBg(e) {
			e.target.classList.remove('hideResult')
			console.log(e.target.classList)
		} ,
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
				this.displayInfoVisible = {visibility: "visible", opacity: '1', transition: "visibility 0.4s opacity 0.4s"}
			}, 100)
		},
		async getLotteryResult() {
			const endpoint = `/api/v1/lotteries/${this.uuid}/results/`;
			try {
				const response = await axios.get(endpoint);
				this.result = response.data
                this.lotteryName = this.result.group
                this.resultsList = JSON.parse(this.result.result.replace(/'/g, '"'))
			} catch (error) {
				console.log(error);
			}
		},
		async deteteResultConfirmation() {
			const alert = await alertController.create({
				header: 'Do you want to delete your result and start lottery again?',
				buttons: [
					{
						text: 'Yes!',
						handler: () => {
							this.deleteResult();
							this.$router.replace({
								path: `/${this.uuid}/`
							});
						},
					},
				],
			});
			await alert.present();
		},
		async deleteResult() {
			const endpoint = `/api/v1/results/${this.result.uuid}/`;
			try {
				await axios.delete(endpoint);
			} catch (error) {
				console.log(error);
			}
		},
	},
	created() {
		this.getLotteryResult();
	},
};
</script>

<style>
.singleResultCont {
	display: flex;
	justify-content: space-around;
	width: 100%;
	margin: 5px;
	background-color: rgba(255, 255, 255, 0);
}

.hideResult {
	background-color: rgb(0, 0, 0);

}

.result {
	display: flex;
	justify-content: center;
	width: 100px;
	border-radius: 5px;
	transition: background-color 1s;
}

.resultCont {
	padding: 20px;
	margin-top: 50px;
	color: rgb(0, 0, 0);
	width: 80%;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	border-radius: 35px;
}

.lotteryNameSpane {
	font-weight: bold;
	color: rgb(255, 200, 0);
}
</style>

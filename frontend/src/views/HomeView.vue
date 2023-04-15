<template>
	<base-layout
		page-title="Christmas Lottery"
		:infoBoxHeight="infoBoxHeight"
		:contentBoxHeight ="contentBoxHeight"
	>
		
		<template v-slot:actions-start1>
			<ion-button>
				<a href="/accounts/logout/">
					<ion-icon style="font-size: 26px;" name="log-out-outline"></ion-icon>
				</a>
			</ion-button>
		</template>

		<template v-slot:actions-end>
			<ion-button v-if="lotteries.length < 5" id="open-modal">
				<ion-icon slot="icon-only" :icon="add"></ion-icon>
				<create-lottery-modal 
				:lotteriesLenght = "lotteries.length"
				@refreshLotteries="getLotteries">
				</create-lottery-modal>
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
				<div v-if="loadingLotteries" class="lotteriesLoader">
					<div id="wifi-loader">
						<svg class="circle-outer" viewBox="0 0 86 86">
							<circle class="back" cx="43" cy="43" r="40"></circle>
							<circle class="front" cx="43" cy="43" r="40"></circle>
							<circle class="new" cx="43" cy="43" r="40"></circle>
						</svg>
						<svg class="circle-middle" viewBox="0 0 60 60">
							<circle class="back" cx="30" cy="30" r="27"></circle>
							<circle class="front" cx="30" cy="30" r="27"></circle>
						</svg>
						<svg class="circle-inner" viewBox="0 0 34 34">
							<circle class="back" cx="17" cy="17" r="14"></circle>
							<circle class="front" cx="17" cy="17" r="14"></circle>
						</svg>
						<div class="text" data-text="Loading..."></div>
					</div>
				</div>
				<div v-else class="infoBody" :style="displayInfoVisible">
					<div v-if="5 > totalLotteries > 0" class="textField">
						Welcome!This is Your christmass lottery! To see your lottery details click on the image next to your lottery. Maximum number of lotteries is 5.
					</div>
					<div v-else-if="totalLotteries == 0" class="textField">
						Welcome! This is Your christmass lottery! At first u need to create your first lottery, you can do so by pressing plus icon in the right top corner!
					</div>
					<div v-else-if="totalLotteries >= 5" class="textField">
						5 is maximum number of lotteries, you need to delete some to add another one!
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
			<lotteries-list
				v-if="lotteries"
				:lotteries="lotteries"
				:totalLotteries="totalLotteries"
				@deleteLottery="deleteLottery"
				@editLottery="editLottery"
			/>
		</template>
	</base-layout>
</template>

<script>
// import { useStore } from '../stores'
import CreateLotteryModal from '../components/CreateLotteryModal.vue';
import { add, close, checkmark, map, trash, create, logOutOutline } from 'ionicons/icons';
import { axios } from '@/common/api.service.js';
import LotteriesList from '../components/LotteriesList.vue';
import { IonButton, IonIcon } from '@ionic/vue';

export default {
	components: {
		IonButton,
		IonIcon,
		LotteriesList,
		CreateLotteryModal,
	},
	data() {
		return {
			lotteries: [],
			nextPage: null,
			loadingLotteries: false,
			error: null,
			add,
			close,
			checkmark,
			map,
			trash,
			logOutOutline,
			create,
			testVar: false,
			infoBoxHeight: 35,
			contentBoxHeight: 65,
			displayInfoVisible: {visibility: "visible", opacity: '1'},
			infoIconVisibility: {visibility: 'hidden', opacity: '0'}
		};
	},
	methods: {
		logoutFunc() {
			console.log('logout')
			this.$router.replace('/accounts/logout/')
		},
		changeHeightProp(x, y) {
			this.infoBoxHeight = x
			this.contentBoxHeight = y
		},
		removeInfo() {
			this.displayInfoVisible = {visibility: "hidden", opacity: '0'};
			this.changeHeightProp(15, 85)
			this.infoIconVisibility = {visibility: "visible", opacity: '1', transition: "visibility 0.4s opacity 0.4s"}
		},
		showInfo() {
			this.changeHeightProp(35, 65)
			this.infoIconVisibility = {visibility: 'hidden', opacity: '0', transition: "visibility 2s opacity 2s"}
			setTimeout(() => {
				this.displayInfoVisible = {visibility: "visible", opacity: '1', transition: "visibility 0.4s opacity 0.4s"}
			}, 100)
		},
		async getLotteries() {
			this.lotteries = [];
			let endpoint = '/api/v1/lotteries/';
			if (this.nextPage) {
				endpoint = this.nextPage;
			}
			this.loadingLotteries = true;
			try {
				const response = await axios.get(endpoint);
				this.lotteries.push(...response.data.results);
				console.log(this.lotteries)
				this.loadingLotteries = false;
				if (response.data.nextPage) {
					this.nextPage = response.data.next;
				} else {
					this.nextPage = null;
				}
			} catch (error) {
				console.log(error.response);
			}
		},
		async deleteLottery(lotteryData) {
			const endpoint = `/api/v1/lotteries/${lotteryData.uuid}/`;
			try {
				await axios.delete(endpoint);
				this.lotteries.splice(this.lotteries.indexOf(lotteryData), 1);
				this.getLotteries();
			} catch (error) {
				console.log(error);
			}
		},
		async editLottery(lotteryData) {
			console.log('lotteryData', lotteryData);
			const endpoint = `/api/v1/lotteries/${lotteryData.lottery.uuid}/`;
			const method = 'PUT';
			try {
				await axios({
					method: method,
					url: endpoint,
					data: { name: lotteryData.newName },
				});
				this.lotteries[this.lotteries.indexOf(lotteryData.lottery)].name =
					lotteryData.newName;
				// this.getLotteries()
			} catch (error) {
				console.log(error);
			}
		},
	},
	computed: {
		totalLotteries() {
			return this.lotteries.length;
		},
	},
	created() {
		this.getLotteries();
	},
	watch: {
		$route(to) {
			if (to.path == '/') {
				this.getLotteries();
			}
		},
	},
};
</script>

<style>


.christmassImage {
	width: 60px;
	height: 60px;
	margin-right: 20px;
	border-radius: 10px;
}

.infoContainerDetails {
	flex-direction: column;
	display: flex;
	justify-content: center;
	align-items: center;
	margin: 20px;
}
.infoIconTrans {
	transition: visibility 0.5s opacity 0.5s;
}

.textField {
	font-family: 'Delicious Handrawn', cursive;
	overflow: scroll
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

.infoBody {
	border-radius: 20px;
	padding: 20px;
	width: 80%;
	background-color: rgb(238, 237, 237);
	color: black;
	margin: 30px;
	display: flex;
	justify-content: space-between;
	opacity: 1;
	transition:visibility 0.3s linear,opacity 0.3s linear
}

.bottomLottery {
	width: 80px;
	padding: 20px 0px;
	position: fixed;
	left: 50%;
	transform: translate(-50%);
	bottom: 0;
	right: 0;
}

.flexCenter {
	width: 80px;
	align-self: center;
	justify-self: center;
	display: flex;
	justify-content: center;
}

.cardBtn {
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

.cardBtn:hover {
	border: 1px solid black;
	transform: scale(1.05);
}

.cardBtn:active {
	transform: scale(0.95) rotateZ(1.7deg);
}

.cardWarning {
	font-size: 25px;
	margin: 10px;
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 5px 10px;
	height: 100px;
	background: rgba(201, 154, 154, 0.498);
	box-shadow: rgba(0, 0, 0, 0.4) 0px 2px 4px,
		rgba(0, 0, 0, 0.3) 0px 7px 13px -3px, rgba(0, 0, 0, 0.2) 0px -3px 0px inset;
}

.lotteriesLoader {
	margin-top: 100px;
	display: flex;
	align-items: center;
	justify-content: center;
	flex-direction: column;
}

#wifi-loader {
	--background: #62abff;
	--front-color: #3b4f72;
	--back-color: #c3c8de;
	--text-color: #414856;
	width: 64px;
	height: 64px;
	border-radius: 50px;
	position: relative;
	display: flex;
	justify-content: center;
	align-items: center;
}

#wifi-loader svg {
	position: absolute;
	display: flex;
	justify-content: center;
	align-items: center;
}

#wifi-loader svg circle {
	position: absolute;
	fill: none;
	stroke-width: 6px;
	stroke-linecap: round;
	stroke-linejoin: round;
	transform: rotate(-100deg);
	transform-origin: center;
}

#wifi-loader svg circle.back {
	stroke: var(--back-color);
}

#wifi-loader svg circle.front {
	stroke: var(--front-color);
}

#wifi-loader svg.circle-outer {
	height: 86px;
	width: 86px;
}

#wifi-loader svg.circle-outer circle {
	stroke-dasharray: 62.75 188.25;
}

#wifi-loader svg.circle-outer circle.back {
	animation: circle-outer135 1.8s ease infinite 0.3s;
}

#wifi-loader svg.circle-outer circle.front {
	animation: circle-outer135 1.8s ease infinite 0.15s;
}

#wifi-loader svg.circle-middle {
	height: 60px;
	width: 60px;
}

#wifi-loader svg.circle-middle circle {
	stroke-dasharray: 42.5 127.5;
}

#wifi-loader svg.circle-middle circle.back {
	animation: circle-middle6123 1.8s ease infinite 0.25s;
}

#wifi-loader svg.circle-middle circle.front {
	animation: circle-middle6123 1.8s ease infinite 0.1s;
}

#wifi-loader svg.circle-inner {
	height: 34px;
	width: 34px;
}

#wifi-loader svg.circle-inner circle {
	stroke-dasharray: 22 66;
}

#wifi-loader svg.circle-inner circle.back {
	animation: circle-inner162 1.8s ease infinite 0.2s;
}

#wifi-loader svg.circle-inner circle.front {
	animation: circle-inner162 1.8s ease infinite 0.05s;
}

#wifi-loader .text {
	position: absolute;
	bottom: -50px;
	display: flex;
	justify-content: center;
	align-items: center;
	text-transform: lowercase;
	font-weight: 500;
	font-size: 20px;
	letter-spacing: 0.2px;
}

#wifi-loader .text::before,
#wifi-loader .text::after {
	content: attr(data-text);
}

#wifi-loader .text::before {
	color: var(--text-color);
}

#wifi-loader .text::after {
	color: var(--front-color);
	animation: text-animation76 3.6s ease infinite;
	position: absolute;
	left: 0;
}

@keyframes circle-outer135 {
	0% {
		stroke-dashoffset: 25;
	}

	25% {
		stroke-dashoffset: 0;
	}

	65% {
		stroke-dashoffset: 301;
	}

	80% {
		stroke-dashoffset: 276;
	}

	100% {
		stroke-dashoffset: 276;
	}
}

@keyframes circle-middle6123 {
	0% {
		stroke-dashoffset: 17;
	}

	25% {
		stroke-dashoffset: 0;
	}

	65% {
		stroke-dashoffset: 204;
	}

	80% {
		stroke-dashoffset: 187;
	}

	100% {
		stroke-dashoffset: 187;
	}
}

@keyframes circle-inner162 {
	0% {
		stroke-dashoffset: 9;
	}

	25% {
		stroke-dashoffset: 0;
	}

	65% {
		stroke-dashoffset: 106;
	}

	80% {
		stroke-dashoffset: 97;
	}

	100% {
		stroke-dashoffset: 97;
	}
}

@keyframes text-animation76 {
	0% {
		clip-path: inset(0 100% 0 0);
	}

	50% {
		clip-path: inset(0);
	}

	100% {
		clip-path: inset(0 0 0 100%);
	}
}
</style>

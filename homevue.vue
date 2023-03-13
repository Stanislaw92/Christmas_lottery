<template>
	<base-layout page-title="Christmas Lottery">
		<lotteries-list
			:lotteries="lotteries"
			:totalLotteries="totalLotteries"
			@deleteLottery="deleteLottery"
			@changeLotteryName="changeLotteryName"
		>
		</lotteries-list>
		<div class="lotteriesLoader">
			<div v-if="loadingLotteries" id="wifi-loader">
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
		<div class="bottomLottery">
			<div class="flexCenter">
				<button class="card" id="open-modal">
					<ion-icon
						size="large"
						slot="icon-only"
						color="light"
						:icon="add"
					></ion-icon>
				</button>
			</div>
		</div>
	</base-layout>
</template>

<script>
// import { OverlayEventDetail } from '@ionic/core/components';
import { add, close, checkmark } from 'ionicons/icons';
import { axios } from '@/common/api.service.js';
import LotteriesList from '../components/LotteriesList.vue';

import {
	// IonButton,
	IonIcon,
} from '@ionic/vue';

export default {
	components: {
		// IonButton,
		IonIcon,
		LotteriesList,
	},
	data() {
		return {
			lotteries: [],
			next: null,
			loadingLotteries: false,
			error: null,
			add,
			close,
			checkmark,
			updatedLotteries: null,
		};
	},
	methods: {
		async getLotteries() {
			this.lotteries = [];
			let endpoint = '/api/v1/lotteries/';
			if (this.next) {
				endpoint = this.next;
			}
			this.loadingLotteries = true;
			try {
				const response = await axios.get(endpoint);
				this.lotteries.push(...response.data.results);
				this.loadingLotteries = false;
				if (response.data.next) {
					this.next = response.data.next;
				} else {
					this.next = null;
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
			} catch (error) {
				console.log(error);
			}
		},
		async changeLotteryName(lotteryData) {
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
		updateLotteriesMethod() {
			this.updatedLotteries = this.lotteries;
		},
	},
	computed: {
		totalLotteries() {
			return this.lotteries.length;
		},
	},
	created() {
		this.getLotteries();
		this.updateLotteriesMethod();
		console.log(this.updatedLotteries);
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

.card {
	position: relative;
	box-sizing: border-box;
	width: 80px;
	height: 80px;
	background: #3b4f72;
	border: 1px solid rgb(0, 0, 0);
	border-radius: 17px;
	text-align: center;
	cursor: pointer;
	display: flex;
	align-items: center;
	justify-content: center;
	font-weight: bolder;
}

.card:hover {
	border: 1px solid black;
	transform: scale(1.05);
}

.card:active {
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
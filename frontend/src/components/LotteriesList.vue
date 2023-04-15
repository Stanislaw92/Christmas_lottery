<template>
	<div style="padding:20px;">
			<lottery-list-item
				v-for="lottery in lotteries"
				:key="lottery.uuid"
				:lottery="lottery"
				@deleteLottery="deleteLottery"
				@editLottery="editLottery"
			/>

	</div>
</template>

<script>

import LotteryListItem from './LotteriesListItem.vue';
import { add } from 'ionicons/icons';
export default {
	props: ['lotteries', 'totalLotteries'],
	components: {
		LotteryListItem,
	},
	methods: {
		deleteLottery(lotteryData) {
			this.$emit('deleteLottery', lotteryData);
		},
		editLottery(lotteryData) {
			this.$emit('editLottery', lotteryData);
		},
	},
	data() {
		return {
			add,
		};
	},
};
</script>

<style>
.actionButtons {
	font-size: 20px;
}

.iconPartCont {
	display: flex;
	flex-direction: column;

	justify-content: space-between;
}

.placementDiv {
	height: 100%;
	width: 100%;
	display: flex;
	justify-content: space-between;
	/* align-items: end; */
	font-size: 13px;
	color: #ffffff;
}

.underText {
	padding: 5px 10px 5px 10px;
	background-color: rgba(0, 0, 0, 0.442);
	border-radius: 10px;
	font-family: 'PT Sans', Calibri, Tahoma, sans-serif;
}

.imageBackground {
	padding: 10px;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	width: 90%;
	height: 170px;
	background: rgba(0, 0, 0, 0.594);
	border-radius: 10px;
}

.infoField {
	font-family: 'Delicious Handrawn', cursive;
	padding: 20px;
	width: 250px;
	border-radius: 50px;
	background: #fefefe;
	box-shadow: 10px 10px 30px #444444,
				-10px -10px 30px #444444;
	align-self:center;
}

.homeContainer {
	padding-top: 30px;
	display: flex;
	flex-direction: column;
}
</style>

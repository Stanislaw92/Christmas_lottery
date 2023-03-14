<template>
	<ion-list class="bgTrans">
		<lottery-list-item
			v-for="lottery in lotteries"
			:key="lottery.uuid"
			:lottery="lottery"
			@deleteLottery = "deleteLottery"
			@editLottery = 'editLottery'
		/>
	</ion-list>
</template>

<script>
import { IonList } from '@ionic/vue';
import LotteryListItem from './LotteriesListItem.vue';
export default {
	props: ['lotteries', 'totalLotteries'],
	components: {
		IonList,
		LotteryListItem,
	},
	methods: {
		deleteLottery(lotteryData){
			this.$emit('deleteLottery', lotteryData)
		},
		editLottery(lotteryData){
			this.$emit('editLottery', lotteryData)
		}
	},
	data() {
		return {};
	},
};
</script>


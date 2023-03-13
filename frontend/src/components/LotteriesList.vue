<template>
	<ion-list>
		<lottery-list-item
			v-for="lottery in lotteries"
			:key="lottery.uuid"
			:lottery="lottery"
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
	data() {
		return {};
	},
};
</script>

<template>
	<ion-list
		class="bgTrans"
		>
		<participant-list-item
			v-for="participant in participants"
			:key="participant.uuid"
			:participant="participant"
			@deletePart = "deletePart"
		/>
	</ion-list>
</template>

<script>
import { IonList } from '@ionic/vue';
import ParticipantListItem from './ParticipantListItem.vue';
export default {
	props: ['participants'],
	components: {
		IonList,
        ParticipantListItem
	},
	methods:{
		deletePart(partData){
			this.$emit('deletePart', partData)
		}
	},
	data() {
		return {};
	},

};
</script>
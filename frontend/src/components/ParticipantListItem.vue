<template>
	<ion-item>
		<ion-label>
			<div class="partName">
				<div>{{ participant.name }} {{ participant.surname }}</div>
				<div class="flexSubClass">
					<div v-if="deleteAccept">
						<ion-icon
							class="actionButtons"
							@click="deletePart(participant)"
							slot="icon-only"
							:icon="checkmark"
							color="success"
						></ion-icon>&nbsp;
						<ion-icon
							v-if="deleteAccept"
							class="actionButtons"
							@click="deleteAccept = false"
							slot="icon-only"
							:icon="close"
							color="danger"
						></ion-icon>&nbsp;
					</div>
					<ion-icon
						class="actionButtons"
						@click="deleteAccept = !deleteAccept"
						slot="icon-only"
						:icon="trash"
					></ion-icon>
				</div>
			</div>
			<div class="partContainer">
				<div class="partEmail">
					{{ participant.email }}
				</div>
				<div>
					<span style="font-size: 14px">
						relation: {{ participant.relation }}</span
					>
				</div>
			</div>
		</ion-label>
	</ion-item>
</template>

<script>
import { IonItem, IonLabel, IonIcon } from '@ionic/vue';
import { trash, checkmark, close } from 'ionicons/icons';

export default {
	props: ['participant'],
	components: {
		IonItem,
		IonIcon,
		IonLabel,
	},
	data() {
		return {
			close,
			trash,
			checkmark,
			deleteAccept: false,
		};
	},
	methods:{
		deletePart(partData){
			this.$emit('deletePart', partData)
		}
	},
	created() {},
};
</script>

<style>
.flexSubClass {
	display: flex;
	flex-direction: row;
}
.partContainer {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
}

.partEmail {
	color: #5a64f5;
	font-size: 14px;
}

.partName {
	display: flex;
	justify-content: space-between;
	font-size: 20px;
}
</style>

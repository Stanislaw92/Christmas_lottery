<template>
	<ion-item router-link="/">
		<ion-label>
			{{lottery.name}}
		</ion-label>
	</ion-item>
</template>

<script>
import { IonItem, IonLabel } from '@ionic/vue';
export default {
	props: ['lottery'],
	components: {
		IonItem,
		IonLabel,
	},
	data() {
		return {};
	},
    created() {
        console.log(this.lottery)
    }
};
</script>

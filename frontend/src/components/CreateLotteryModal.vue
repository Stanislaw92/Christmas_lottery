<template>
		<ion-modal ref="modal" trigger="open-modal">
			<ion-header>
				<ion-toolbar>
					<ion-buttons slot="start">
						<ion-button @click="cancel()">
                            <ion-icon
                                slot="icon-only"
                                :icon="arrowBack"
                            ></ion-icon>
                        </ion-button>
					</ion-buttons>
					<ion-title mode="ios">Create lottery</ion-title>
					<ion-buttons slot="end">
						<ion-button @click="cancel()">
                            <ion-icon
                                slot="icon-only"
                                :icon="add"
                            ></ion-icon>
                        </ion-button>
					</ion-buttons>
				</ion-toolbar>
			</ion-header>
			<ion-content class="ion-padding">
				<ion-item>
					<ion-label position="stacked">Enter your lottery name</ion-label>
					<ion-input
						ref="input"
						type="text"
						placeholder="Lottery name"
					></ion-input>
				</ion-item>
			</ion-content>
		</ion-modal>
</template>

<script>
import {
	IonButtons,
	IonButton,
	IonModal,
	IonHeader,
	IonContent,
	IonToolbar,
	IonTitle,
	IonItem,
	IonInput,
	IonLabel,
	IonIcon
} from '@ionic/vue';
import { arrowBack, add } from 'ionicons/icons'
import { defineComponent } from 'vue';

export default defineComponent({
	components: {
		IonButtons,
		IonButton,
		IonModal,
		IonHeader,
		IonContent,
		IonToolbar,
		IonTitle,
		IonItem,
		IonInput,
		IonLabel,
		IonIcon
	},
	data() {
		return {
            arrowBack,
            add,
			message:
				'This modal example uses triggers to automatically open a modal when the button is clicked.',
		};
	},
	methods: {
		cancel() {
			this.$refs.modal.$el.dismiss(null, 'cancel');
		},
		confirm() {
			const name = this.$refs.input.$el.value;
			this.$refs.modal.$el.dismiss(name, 'confirm');
		},
	},
});
</script>

<style>
ion-toolbar, ion-header {
    --min-height: 48px;
   }


</style>
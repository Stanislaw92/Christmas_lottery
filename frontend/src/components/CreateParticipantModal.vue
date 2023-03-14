<template>
		<ion-modal ref="modal" trigger="open-modal-part">
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
						<ion-button @click="confirm()">
                            <ion-icon
                                slot="icon-only"
                                :icon="add"
                            ></ion-icon>
                        </ion-button>
					</ion-buttons>
				</ion-toolbar>
			</ion-header>
			<ion-content class="ion-padding">
				<ion-item class="backGR">
					<ion-label color="light" position="stacked">Enter your name</ion-label>
					<ion-input
						color="light"
						required = "true"
						ref="name"
						type="text"
						placeholder="name"
					></ion-input>
				</ion-item>
                <ion-item class="backGR">
					<ion-label color="light" position="stacked">Enter your surname</ion-label>
					<ion-input
						color="light"
						required = "true"
						ref="surname"
						type="text"
						placeholder="surname"
					></ion-input>
				</ion-item>
                <ion-item class="backGR">
					<ion-label color="light" position="stacked">Enter your e-mail</ion-label>
					<ion-input
						color="light"
						required = "true"
						ref="email"
						type="email"
						placeholder="email"
					></ion-input>
				</ion-item>
                <ion-item class="backGR">
					<ion-label color="light" position="stacked">Enter your relation</ion-label>
					<ion-input
						color="light"
						required = "true"
						ref="relation"
						type="number"
						placeholder="0"
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
import { axios } from '@/common/api.service.js';
import { arrowBack, add } from 'ionicons/icons'
import { defineComponent } from 'vue';

export default defineComponent({
	props: ['uuid'],
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
		async confirm() {
			const name = this.$refs.name.$el.value;
			const surname = this.$refs.surname.$el.value;
			const email = this.$refs.email.$el.value;
			const relation = this.$refs.relation.$el.value;

			const endpoint = `/api/v1/lotteries/${this.uuid}/participant/`
			let method ="POST"
			try {
				await axios({
					method: method,
					url: endpoint,
					data: { name: name,
							surname: surname,
							email: email,
							relation: relation
					}
				})
			} catch (error) {
				console.log(error)
			}
			this.$emit('refreshParticipants')
			this.$refs.modal.$el.dismiss(null, 'cancel');
		},

	},
});
</script>

<style>
ion-toolbar, ion-header {
    --min-height: 48px;
   }

.backGR {
	background: rgba(0, 0, 0, 0.8);
}

</style>
<template>
	<ion-modal ref="modal" trigger="open-modal">
		<ion-header>
			<ion-toolbar>
				<ion-buttons slot="start">
					<ion-button @click="cancel()">
						<ion-icon slot="icon-only" :icon="arrowBack"></ion-icon>
					</ion-button>
				</ion-buttons>
				<ion-title mode="ios">Create lottery</ion-title>
				<ion-buttons slot="end">
					<ion-button @click="confirm()">
						<ion-icon slot="icon-only" :icon="add"></ion-icon>
					</ion-button>
				</ion-buttons>
			</ion-toolbar>
		</ion-header>
		<ion-content class="ion-padding">
			<ion-item 
				lines="none" 
				class="backGRLott"
				@keyup="checkName(this.name)"
				:class="{errorBorderCorrect: nameCorrect}">
				<ion-label color="light" position="stacked"
					>Enter your lottery name ( max length = 50 )</ion-label
				>
				<ion-input
					v-model="name"
					color="light"
					ref="input"
					type="text"
					placeholder="Lottery name"
				></ion-input>
			</ion-item>
			<div v-if="errorMsg" class="errorClass">
				Your lottery name cannot have more letters than 50!
			</div>
			<div v-if="errorMsgEmptyStr" class="errorClass">
				Your lottery need a name!
			</div>
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
	IonIcon,
} from '@ionic/vue';
import { axios } from '@/common/api.service.js';
import { arrowBack, add } from 'ionicons/icons';
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
		IonIcon,
	},
	data() {
		return {
			arrowBack,
			add,
			name: null,
			errorMsg: false,
			errorMsgEmptyStr: false,
			nameCorrect: false,
		};
	},
	methods: {
		cancel() {
			console.log();
			this.$refs.modal.$el.dismiss(null, 'cancel');
			this.errorMsg = false;
			this.errorMsgEmptyStr = false;
		},
		checkName(name){
			if ( name.length != 0 && name != '' && name != undefined && name.length <= 30) {
				this.nameCorrect = true
				this.errorMsg = ''
				this.errorMsgEmptyStr = false;
			} else {
				this.nameCorrect = false
			}
		},
		async confirm() {
			const name = this.$refs.input.$el.value;
			const endpoint = `/api/v1/lotteries/`;
			let method = 'POST';

			if (name.length == 0 || name == undefined || name == '') {
				this.errorMsgEmptyStr = true;
			} else {
				if (name.length < 51) {
					try {
						await axios({
							method: method,
							url: endpoint,
							data: { name: name },
						});
						this.$emit('refreshLotteries');
						this.errorMsg = false;
						this.errorMsgEmptyStr = false;
						this.$refs.modal.$el.dismiss(null, 'cancel');
					} catch (error) {
						console.log(error);
					}
				} else {
					this.errorMsg = true;
				}
			}
		},
	},
});
</script>

<style>
ion-toolbar,
ion-header {
	--min-height: 48px;
}

.backGRLott {
	background: rgba(0, 0, 0, 0.8);
}
.errorClass {
	display: flex;
	align-items: center;
	justify-content: center;
	color: red;
	background: rgba(29, 0, 0, 0.89);
	border: 1px solid black;
}

.errorBorderCorrect {
	border: 1px solid rgb(34, 255, 0);
}
</style>

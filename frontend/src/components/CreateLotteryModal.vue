<template>
	<ion-modal ref="modal" trigger="open-modal">
		<ion-header>
			<ion-toolbar>
				<ion-buttons slot="start">
					<ion-button @click="cancel()">
						<ion-icon slot="icon-only" :icon="arrowBack"></ion-icon>
					</ion-button>
				</ion-buttons>
				<ion-title mode="ios">Create Lottery</ion-title>
				<ion-buttons slot="end">
					<ion-button
						@click = "showInfo"
						class="iconInfoTrans"
						:style="infoIconVisibility">
						<i class="fa-solid fa-info" style="color: black;"></i>
					</ion-button>
					<ion-button @click="confirm()">
						<ion-icon slot="icon-only" :icon="add"></ion-icon>
					</ion-button>
				</ion-buttons>
			</ion-toolbar>
		</ion-header>
		<ion-content>
			<div class="backgroundHomeModal">
				<div
					:style="{
						height: infoBoxHeight + '%',
						transition: 'height 0.5s',
					}"
				>
					<div class="infoContainer">
						<div class="infoBody" :style="displayInfoVisible">
							<div class="textField">
								To create new lottery, enter new lottery name ( remember that
								name cannot have more letters than 50 ) then click on 'add'
								button in the right top corner of the app!
							</div>
							<div>
								<ion-icon
									@click="removeInfo"
									slot="icon-only"
									:icon="close"
								></ion-icon>
							</div>
						</div>
					</div>
				</div>
				<div
					class="backgroundHomeBodyModal"
					:style="{
						height: contentBoxHeight + '%',
						transition: 'height 0.5s',
					}"
				>
					<ion-item
						lines="none"
						class="backGRLott"
						@keyup="checkName(this.name)"
						:class="{ errorBorderCorrect: nameCorrect }"
					>
						<ion-label color="dark" position="stacked"></ion-label>
						<ion-input
							v-model="name"
							color="dark"
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
				</div>
			</div>
		</ion-content>
	</ion-modal>
</template>

<script>
import {
	IonButton,
	IonItem,
	IonInput,
	IonLabel,
	IonIcon,
	IonButtons,
	IonToolbar,
	IonHeader,
	IonContent,
	IonTitle,
	IonModal,
} from '@ionic/vue';
import { axios } from '@/common/api.service.js';
import { arrowBack, add, close } from 'ionicons/icons';
import { defineComponent } from 'vue';

export default defineComponent({
	props: ['lotteriesLenght'],
	components: {
		IonButton,
		IonItem,
		IonInput,
		IonLabel,
		IonIcon,
		IonButtons,
		IonToolbar,
		IonHeader,
		IonTitle,
		IonContent,
		IonModal,
	},
	data() {
		return {
			arrowBack,
			add,
			close,
			name: null,
			errorMsg: false,
			errorMsgEmptyStr: false,
			nameCorrect: false,
			infoBoxHeight: 35,
			contentBoxHeight: 65,
			displayInfoVisible: {visibility: "visible", opacity: '1'},
			infoIconVisibility: {visibility: 'hidden', opacity: '0'}
		};
	},
	methods: {
		changeHeightProp(x, y) {
			(this.infoBoxHeight = x), (this.contentBoxHeight = y);
		},
		removeInfo() {
			this.displayInfoVisible = {visibility: "hidden", opacity: '0', transition: "visibility 0.5s opacity 0.5s;"};
			this.changeHeightProp(15, 85)
			this.infoIconVisibility = 'visible'
		},
		showInfo() {
			this.changeHeightProp(35, 65)
			setTimeout(() => {
				this.displayInfoVisible = {visibility: "visible", opacity: '1', transition: "visibility 0.4s opacity 0.4s;"}
			}, 100)
;
			this.infoIconVisibility = {visibility: 'hidden', opacity: '0'}
		},
		cancel() {
			console.log();
			this.$refs.modal.$el.dismiss(null, 'cancel');
			this.errorMsg = false;
			this.errorMsgEmptyStr = false;
		},
		checkName(name) {
			if (
				name.length != 0 &&
				name != '' &&
				name != undefined &&
				name.length <= 30
			) {
				this.nameCorrect = true;
				this.errorMsg = '';
				this.errorMsgEmptyStr = false;
			} else {
				this.nameCorrect = false;
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
						this.name = null;
					} catch (error) {
						console.log(error);
					}
				} else {
					this.errorMsg = true;
				}
			}
		},
	},
	created() {
	}
});
</script>

<style>
ion-toolbar,
ion-header {
	--min-height: 48px;
}

.backGRLott {
	background: rgba(0, 0, 0, 0.8);
	border-radius: 10px;
}
.errorClass {
	display: flex;
	align-items: center;
	justify-content: center;
	color: red;
	background: rgba(29, 0, 0, 0.89);
	border: 1px solid black;
	border-radius: 8px;
}

.errorBorderCorrect {
	border: 1px solid rgb(34, 255, 0);
}

.backgroundHomeModal {
	width: 100%;
	height: 100%;
	/* background-color: rgb(255, 255, 255); */
	background: rgb(209, 70, 70);
	background: linear-gradient(
		90deg,
		rgba(209, 70, 70, 1) 0%,
		rgba(205, 118, 118, 1) 100%
	);
}

.backgroundHomeBodyModal {
	width: 100%;
	padding: 25px;
	/* height: 65%; */
	background-color: rgb(238, 237, 237);
	border-top-left-radius: 30px;
	border-top-right-radius: 30px;
	/* box-shadow: -5px -5px 10px #444444; */
}
</style>

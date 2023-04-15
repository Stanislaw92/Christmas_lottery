<template>
	<ion-modal ref="modal" trigger="open-modal-part">
		<ion-header>
			<ion-toolbar>
				<ion-buttons slot="start">
					<ion-button @click="cancel()">
						<ion-icon slot="icon-only" :icon="arrowBack"></ion-icon>
					</ion-button>
				</ion-buttons>
				<ion-title mode="ios">Create participant</ion-title>
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
						class="backGR"
						:class="{ errorBorderCorrect: nameCorrect }"
						style="border-radius: 20px 20px 0 0;">
						<ion-label color="dark" position="stacked">Enter your name</ion-label>
						<ion-input
							@keyup="checkName(this.name)"
							v-model = "name"
							color="dark"
							required="true"
							ref="name"
							type="text"
							placeholder="name"
					></ion-input>
					</ion-item>
					<div v-if="errNameMsg" class="errorClassPart unCorrect">
						{{ errNameMsg }}
					</div>
					<ion-item 
						lines="none" 
						class="backGR"
						:class="{ errorBorderCorrect: surnameCorrect }">
						<ion-label color="dark" position="stacked"
							>Enter your surname</ion-label
						>
						<ion-input
							@keyup="checkSurName(this.surname)"
							v-model = "surname"
							color="dark"
							required="true"
							ref="surname"
							type="text"
							placeholder="surname"
						></ion-input>
					</ion-item>
					<div v-if="errSurNameMsg" class="errorClassPart unCorrect">
						{{ errSurNameMsg }}
					</div>
					<ion-item 
						lines="none" 
						class="backGR" 
						:class="{ errorBorderCorrect: emailCorrect }"
					>
						<ion-label color="dark" position="stacked"
							>Enter your e-mail</ion-label
						>
						<ion-input
							v-model="email"
							@keyup="checkEmail"
							color="dark"
							required="true"
							ref="email"
							type="email"
							placeholder="email"
						></ion-input>
					</ion-item>
					<div
						v-if="errEmailMsg"
						class="errorClassPart unCorrect"	
					>
						{{ errEmailMsg }}
					</div>
					<ion-item 
						lines="none" 	
						class="backGR"
						:class="{ errorBorderCorrect: relationCorrect }"
						style="border-radius: 0 0 20px 20px;">
						<ion-label color="dark" position="stacked"
							>Enter your relation</ion-label
						>
						<ion-input
							@keyup="checkRelation(this.relation)"
							v-model = "relation"
							color="dark"
							required="true"
							ref="relation"
							type="number"
							placeholder="1 ( if there is no relation type 1 )"
						></ion-input>
					</ion-item>
					<div v-if="errRelMsg" class="errorClassPart unCorrect">
						{{ errRelMsg }}
					</div>
				</div>
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
import { arrowBack, add, close } from 'ionicons/icons';
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
		IonIcon,
	},
	data() {
		return {
			arrowBack,
			add,
			close,
			errNameMsg: '',
			errSurNameMsg: '',
			errEmailMsg: '',
			errRelMsg: '',
			email: null,
			relation: null,
			name: null,
			surname: null,
			emailCorrect: false,
			nameCorrect: false,
			surnameCorrect: false,
			relationCorrect: false,
			infoBoxHeight: 35,
			contentBoxHeight: 65,
			displayInfoVisible: {visibility: "visible", opacity: '1'},
			infoIconVisibility: {visibility: 'hidden', opacity: '0'}
		};
	},
	created() {},
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
		checkEmail() {
			if (this.validateEmail(this.email)) {
				this.emailCorrect = true;
				this.errEmailMsg = ''
			} else {
				this.emailCorrect = false;
			}
		},
		validateEmail(email) {
			var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
			return re.test(email);
		},
		refreshForm(){
			this.emailCorrect = false;
			this.nameCorrect = false
			this.surnameCorrect = false
			this.relationCorrect = false
			this.errNameMsg = '';
			this.errSurNameMsg = '';
			this.errEmailMsg = '';
			this.errRelMsg = '';
			this.$refs.name.$el.value = '';
			this.$refs.surname.$el.value = '';
			this.$refs.email.$el.value = '';
			this.$refs.relation.$el.value = '';
		},
		cancel() {
			this.$refs.modal.$el.dismiss(null, 'cancel');
			this.refreshForm()
		},
		checkName(name){
			if ( name.length != 0 && name != '' && name != undefined && name.length <= 30) {
				this.nameCorrect = true
				this.errNameMsg = ''
			} else {
				this.nameCorrect = false
			}
		},
		checkSurName(surname){
			if ( surname != '' && surname != undefined && surname.length <= 30) {
				this.surnameCorrect = true
				this.errSurNameMsg = ''
			} else {
				this.surnameCorrect = false
			}
		},
		checkRelation(relation){
			if ( relation != '' && relation != undefined && relation <= 10) {
				this.relationCorrect = true
				this.errRelMsg = ''
			} else {
				this.relationCorrect = false
			}
		},
		async confirm() {
			this.errNameMsg = '';
			this.errSurNameMsg = '';
			this.errEmailMsg = '';
			this.errRelMsg = '';

			const name = this.$refs.name.$el.value;
			const surname = this.$refs.surname.$el.value;
			const email = this.$refs.email.$el.value;
			const relation = this.$refs.relation.$el.value;

			if (name.length == 0 || name == undefined || name == '') {
				this.errNameMsg = "Please enter the participant's name ";
			} else if (name.length > 30) {
				this.errNameMsg = 'Name cannot have more than 30 letters!';
			} else {
				this.errNameMsg = '';
			}

			if (surname.length == 0 || surname == undefined || surname == '') {
				this.errSurNameMsg = "Please enter the participant's surname ";
			} else if (surname.length > 30) {
				this.errSurNameMsg = 'Name cannot have more than 30 letters!';
			} else {
				this.errSurNameMsg = '';
			}

			if (email.length == 0 || email == undefined || email == '') {
				this.errEmailMsg = "Please enter the participant's email ";
			} else {
				if (this.validateEmail(email)) {
					this.errEmailMsg = '';
				} else {
					this.errEmailMsg = 'Please enter correct email!';
				}
			}

			if (relation.length == 0 || relation == undefined || relation == '') {
				this.errRelMsg = 'Please enter relation beetwen participants';
			} else if (relation > 10) {
				this.errRelMsg = 'Choose relation only from 1-10!';
			} else {
				this.errRelMsg = '';
			}

			if (
				this.errNameMsg == '' &&
				this.errSurNameMsg == '' &&
				this.errEmailMsg == '' &&
				this.errRelMsg == ''
			) {
				const endpoint = `/api/v1/lotteries/${this.uuid}/participant/`;
				let method = 'POST';
				try {
					await axios({
						method: method,
						url: endpoint,
						data: {
							name: name,
							surname: surname,
							email: email,
							relation: relation,
						},
					});
					this.$emit('refreshParticipants');
					this.$emit('addPart');
					this.$refs.modal.$el.dismiss(null, 'cancel');
					this.refreshForm()
				} catch (error) {
					console.log(error);
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

.backGR {
	background: rgba(0, 0, 0, 0.8);
	border: green;
}

.correct {
	color: rgb(0, 219, 29);
}
.unCorrect {
	color: red;
}

.errorClassPart {
	display: flex;
	align-items: center;
	justify-content: center;
	background: rgba(29, 0, 0, 0.89);
	border: 1px solid black;
	border-radius: 5px;
}

.errorBorderCorrect {
	border: 1px solid rgb(34, 255, 0);
}

.errorBorderWrong {
	border: 1px solid red;
}

.backgroundHomeModalPart {
	width: 100%;
	/* height: 100%; */
	/* background-color: rgb(255, 255, 255); */
	background: rgb(209, 70, 70);
	background: linear-gradient(
		90deg,
		rgba(209, 70, 70, 1) 0%,
		rgba(205, 118, 118, 1) 100%
	);
}

.backgroundHomeBodyModalPart {
	width: 100%;
	padding: 25px;
	/* height: 65%; */
	background-color: rgb(238, 237, 237);
	border-top-left-radius: 30px;
	border-top-right-radius: 30px;
	/* box-shadow: -5px -5px 10px #444444; */
}
</style>

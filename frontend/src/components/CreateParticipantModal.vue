<template>
	<ion-modal ref="modal" trigger="open-modal-part">
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
				class="backGR"
				:class="{ errorBorderCorrect: nameCorrect }">
				<ion-label color="light" position="stacked">Enter your name</ion-label>
				<ion-input
					@keyup="checkName(this.name)"
					v-model = "name"
					color="light"
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
				<ion-label color="light" position="stacked"
					>Enter your surname</ion-label
				>
				<ion-input
					@keyup="checkSurName(this.surname)"
					v-model = "surname"
					color="light"
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
				<ion-label color="light" position="stacked"
					>Enter your e-mail</ion-label
				>
				<ion-input
					v-model="email"
					@keyup="checkEmail"
					color="light"
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
				:class="{ errorBorderCorrect: relationCorrect }">
				<ion-label color="light" position="stacked"
					>Enter your relation</ion-label
				>
				<ion-input
					@keyup="checkRelation(this.relation)"
					v-model = "relation"
					color="light"
					required="true"
					ref="relation"
					type="number"
					placeholder="1 ( if there is no relation type 1 )"
				></ion-input>
			</ion-item>
			<div v-if="errRelMsg" class="errorClassPart unCorrect">
				{{ errRelMsg }}
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
		};
	},
	created() {},
	methods: {
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
				this.errRelMsg = 'Please enter relation beetwen other participants';
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
}

.errorBorderCorrect {
	border: 1px solid rgb(34, 255, 0);
}

.errorBorderWrong {
	border: 1px solid red;
}
</style>

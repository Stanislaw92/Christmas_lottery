<template>
	<ion-page>
		<ion-header>
			<ion-toolbar>
				<ion-buttons slot="start">
					<slot name="actions-start1"></slot>
					<ion-back-button
						:default-href="pageDefaultBackLink"
					></ion-back-button>
				</ion-buttons>
				<ion-title mode="ios">{{ pageTitle }}</ion-title>
				<ion-buttons slot="end">
					<slot name="actions-end2"></slot>
					<slot name="actions-end1"></slot>
					<slot name="actions-end"></slot>
				</ion-buttons>
			</ion-toolbar>
		</ion-header>
		<ion-content>
			<div class="backgroundHome">
				<div
					:style="{
						height: infoBoxHeight + '%',
						transition: 'height 0.5s',
					}"
				>

					<slot name="info-slot" />

				</div>
				<div
					class="backgroundHomeBody"
					:style="{
						height: contentBoxHeight + '%',
						transition: 'height 0.5s',
					}"
				>
					<slot name="content-slot"/>
				</div>
			</div>
		</ion-content>
	</ion-page>
</template>

<script>
// import { useStore } from '../../stores';
import {
	IonPage,
	IonHeader,
	IonTitle,
	IonContent,
	IonToolbar,
	IonBackButton,
	IonButtons,
} from '@ionic/vue';

export default {
	props: ['pageTitle', 'pageDefaultBackLink', 'infoBoxHeight', 'contentBoxHeight'],
	components: {
		IonPage,
		IonHeader,
		IonTitle,
		IonContent,
		IonToolbar,
		IonBackButton,
		IonButtons,
		
	},
	data() {
		return {
		};
	},
	methods: {
	},
	created() {
	},
};
</script>

<style>
.infoIcon {
	padding: 10px 30px 10px 30px;
	align-self: flex-end;
}
.infoSlotContainer {
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
}

.backgroundHome {
	width: 100%;
	height: 100%;
	background: linear-gradient(90deg, rgba(209,70,70,1) 0%, rgba(205,118,118,1) 100%);
}

.backgroundHomeBody {
	width: 100%;
	background-color: rgb(238, 237, 237);
	border-top-left-radius: 30px;
	border-top-right-radius: 30px;
}
</style>

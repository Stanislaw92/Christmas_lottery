<template>
<div class="testNewDiv">
	<img @click="detailsPush" class="christmassImage" src="https://img.freepik.com/premium-vector/cute-christmas-tree-cartoon-character_313669-57.jpg?w=2000" alt="">
	<div class="testNewDivSubDIv">
		<div class="elementName">
			{{lottery.name}}
		</div>
		<div class="subDiv">
			<div>{{lottery.created_at}}</div>
			&nbsp;&#183;&nbsp;
			<div>participants: <b>{{lottery.num_of_participants}}</b></div>
		</div>
	</div>
	<div class="iconsStyle">
		<ion-icon @click="deleteAlertConfirmation" style="color: rgba(0, 0, 0, 0.73);" slot="icon-only" :icon="trash"></ion-icon>
		<ion-icon @click="alertChangeName" style="color: rgba(0, 0, 0, 0.73);" slot="icon-only" :icon="create"></ion-icon>
	</div>
</div>
</template>

<script>
import { alertController } from '@ionic/vue';
import { add, trash, map, create } from 'ionicons/icons';
import { IonIcon } from '@ionic/vue';
export default {
	props: ['lottery'],
	components: {
		IonIcon,
	},
	data() {
		return {
			trash,
			map,
			create,
			add,
		};
	},
	methods: {
		detailsPush() {
			this.$router.push({ path: `/${this.lottery.uuid}/` });

		},
		deleteLottery() {
			this.$emit('deleteLottery', this.lottery);
		},
		editLottery(lotteryData) {
			this.$emit('editLottery', lotteryData);
		},
		async deleteAlertConfirmation() {
			const alert = await alertController.create({
				message: 'Are u sure you want delete this lottery?',
				buttons: [
					{
						text: 'No',
						role: 'cancel',
					},
					{
						text: 'Yes',
						handler: () => {
							this.deleteLottery();
						},
					},
				],
			});
			await alert.present();
		},
		async alertChangeName() {
			const alert = await alertController.create({
				message: 'Change name of the lottery',
				buttons: [
					{
						text: 'exit!',
						role: 'cancel',
					},
					{
						text: 'Accept!',
						handler: (alertData) => {
							const newName = alertData.newName;
							const emitData = {
								newName: newName,
								lottery: this.lottery,
							};
							this.editLottery(emitData);
						},
					},
				],
				inputs: [
					{
						name: 'newName',
						type: 'text',
						placeholder: `${this.lottery.name}`,
					},
				],
			});
			await alert.present();
		},
	},
	computed: {
		getImage() {
			const x = this.test[Math.floor(Math.random() * this.test.length)];
			return x;
		},
	},
	created() {},
};
</script>

<style>
.subDiv {
	display: flex;
	flex-direction: row;
	/* justify-content: space-between; */
	font-size: 10px;
	color: rgb(0, 0, 0);
}

.iconsStyle{
	padding: 6px;
	display: flex;
	flex-direction: column;
	justify-content: space-evenly;
	
}
.elementName {
	font-size: 15px;
	font-weight: bold;
}



.testNewDivSubDIv {
	font-family: 'Inconsolata', monospace;
	padding: 5px;
	width: 100%;
	display: flex;
	flex-direction: column;
	justify-content: space-evenly;
	/* align-items: space-evenly; */

}

.testNewDiv {
	margin: 10px;
	display: flex;
	justify-content: flex-start;
}
</style>

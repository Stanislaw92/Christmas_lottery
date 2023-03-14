<template>
	<ion-item 
			@click = "detailsPush"
		>
		<ion-label>
			<div class="lotteryItemCont">
				<div>
					{{lottery.name}}
				</div>
				<div>
					<ion-icon
						class="actionButtons"
						@click ="alertChangeName"
						slot="icon-only"
						:icon="create"
					></ion-icon>&nbsp;&nbsp;&nbsp;
					<ion-icon
						class="actionButtons"
						@click ="alertConfirmation('are You sure You want delete this lottery?!', deleteLottery)"
						slot="icon-only"
						:icon="trash"
					></ion-icon>
				</div>
			</div>
		</ion-label>
	</ion-item>
</template>

<script>
import { alertController } from '@ionic/vue';
import { trash, create } from 'ionicons/icons';
import { IonItem, IonLabel, IonIcon } from '@ionic/vue';
export default {
	props: ['lottery'],
	components: {
		IonItem,
		IonIcon,
		IonLabel,
	},
	data() {
		return {
			trash,
			create,
		};
	},
	methods: {
		detailsPush(e){
			if (!e.target.classList.contains('actionButtons')) {
				this.$router.push({ path: `/${this.lottery.uuid}/`})
			}
		},
		deleteLottery(){
			this.$emit('deleteLottery', this.lottery)
		},
		editLottery(lotteryData){
			this.$emit('editLottery', lotteryData)
		},
		async alertConfirmation(textVar, handlerFunct) {	
			const alert = await alertController.create({
				message: textVar,
				buttons: [
					{
						text: 'No!',
						role: 'cancel'
					},
					{
						text: 'Yes!',
						handler: handlerFunct
					},

				],
			});

			await alert.present();
		},
		async alertChangeName(){
			const alert = await alertController.create({
				message: 'Change name of the lottery',
				buttons: [
					{
						text: 'exit!',
						role: 'cancel'
					},
					{
						text: 'Accept!',
						handler: (alertData) => {
							const newName = alertData.newName
							const emitData = {
								newName: newName,
								lottery: this.lottery
							}
							this.editLottery(emitData)
						}
					},
				],
				inputs: [
					{
						name: 'newName',
						type: 'text',
						placeholder: `${this.lottery.name}`,
					}
				]
			})
			await alert.present();
		}
	},
    created() {
    }
};
</script>

<style>
.lotteryItemCont {
	display: flex;
	justify-content: space-between;
}

</style>
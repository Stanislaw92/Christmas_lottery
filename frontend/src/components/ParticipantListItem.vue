<template>
	<div class="participantItem">
		<img
			v-if = "!checkSex"
			@click="detailsPush"
			class="christmassImage"
			src="https://cdn4.vectorstock.com/i/1000x1000/39/58/unknown-male-person-eps-10-vector-13383958.jpg"
			alt=""
		/>
		<img
			v-else
			@click="detailsPush"
			class="christmassImage"
			src="https://i0.wp.com/socoshaping.com/wp-content/uploads/2019/02/unknown-woman.png?ssl=1"
			alt=""
		/>
		<div class="participantItemIcons">
			<div class="elementName">
				{{ participant.name }}
			</div>
			<div class="subDiv">
				<div class="partEmail">{{ participant.email }}</div>
				&nbsp;&#183;&nbsp;
				<div>
					rel: <b>{{ participant.relation }}</b>
				</div>
			</div>
		</div>
		<div class="iconsStyleParticipant">
			<div v-if="deleteAccept">
				<ion-icon
					class="actionButtons"
					@click="deletePart(participant)"
					slot="icon-only"
					:icon="checkmark"
					color="success"
				></ion-icon>
			</div>
			<ion-icon
				@click="deleteAccept = !deleteAccept"
				style="color: rgba(0, 0, 0, 0.73)"
				slot="icon-only"
				:icon="trash"
			></ion-icon>
		</div>
	</div>
</template>

<script>
import { IonIcon } from '@ionic/vue';
import { trash, checkmark, close } from 'ionicons/icons';

export default {
	props: ['participant'],
	components: {
		IonIcon,
	},
	data() {
		return {
			close,
			trash,
			checkmark,
			deleteAccept: false,
		};
	},
	methods: {
		deletePart(partData) {
			this.$emit('deletePart', partData);
		},
	},
	computed: {
		checkSex() {
			if ( this.participant.name.endsWith('a')){
				return true
			} else {
				return false
			}
		}
	},
	created() {},
};
</script>

<style>
.participantItem {
	margin: 10px;
	display: flex;
	justify-content: flex-start;
}

.partEmail {
	color: rgb(0, 250, 238);
}

.flexSubClass {
	display: flex;
	flex-direction: row;
}
.partContainer {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
}

.partEmail {
	color: #5a64f5;
	font-size: 14px;
}

.partName {
	display: flex;
	justify-content: space-between;
	font-size: 20px;
}

.participantItemIcons {
	font-family: 'Inconsolata', monospace;
	padding: 5px;
	width: 100%;
	display: flex;
	flex-direction: column;
	justify-content: space-evenly;
	/* align-items: space-evenly; */

}

.iconsStyleParticipant{
	padding: 6px;
	display: flex;
	flex-direction: column;
	justify-content: space-evenly;
	
}
</style>

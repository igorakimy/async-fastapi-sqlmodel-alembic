<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Панель управления</div>
      </v-card-title>
      <v-card-text>
        <div class="headline font-weight-light ml-0 mb-5 mt-5">Добро пожаловать, <span class="font-weight-bold">{{greetedUser}}</span></div>
      </v-card-text>
      <v-card-actions>
        <v-btn to="/main/profile/view">Профиль</v-btn>
        <v-btn to="/main/profile/edit">Изменить профиль</v-btn>
        <v-btn to="/main/profile/password">Изменить пароль</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import { readUserProfile } from '@/store/main/getters';
@Component
export default class Dashboard extends Vue {
  get greetedUser() {
    const userProfile = readUserProfile(this.$store);
    if (userProfile) {
      if (userProfile.first_name) {
        return userProfile.first_name + ' ' + userProfile.last_name;
      } else {
        return userProfile.email;
      }
    }
  }
}
</script>
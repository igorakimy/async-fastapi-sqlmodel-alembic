<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Профиль</div>
      </v-card-title>
      <v-card-text>
        <div class="my-4">
          <div class="subheading secondary--text ">Имя</div>
          <div class="title primary--text text--darken-2" v-if="userProfile && userProfile.first_name">{{userProfile.first_name}}</div>
          <div class="title primary--text text--darken-2" v-else>-----</div>
        </div>
        <div class="my-4">
          <div class="subheading secondary--text ">Фамилия</div>
          <div class="title primary--text text--darken-2" v-if="userProfile && userProfile.last_name">{{userProfile.last_name}}</div>
          <div class="title primary--text text--darken-2" v-else>-----</div>
        </div>
        <div class="my-3">
          <div class="subheading secondary--text ">Email</div>
          <div class="title primary--text text--darken-2" v-if="userProfile && userProfile.email">{{userProfile.email}}</div>
          <div class="title primary--text text--darken-2" v-else>-----</div>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-btn to="/main/profile/edit">Изменить</v-btn>
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
export default class UserProfile extends Vue {
  get userProfile() {
    return readUserProfile(this.$store);
  }
  public goToEdit() {
    this.$router.push('/main/profile/edit');
  }
  public goToPassword() {
    this.$router.push('/main/profile/password');
  }
}
</script>
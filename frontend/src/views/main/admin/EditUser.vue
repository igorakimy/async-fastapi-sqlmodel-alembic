<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Редактирование пользователя</div>
      </v-card-title>
      <v-card-text>
        <template>
          <div class="my-3">
<!--            <div class="subheading secondary&#45;&#45;text text&#45;&#45;lighten-2">Username</div>-->
            <div
              class="title primary--text text--darken-2"
              v-if="user"
            >{{user.email}}</div>
            <div
              class="title primary--text text--darken-2"
              v-else
            >-----</div>
          </div>
          <v-form
            v-model="valid"
            ref="form"
            lazy-validation
          >
            <v-text-field
              label="Имя"
              v-model="firstName"
              required
            ></v-text-field>
            <v-text-field
              label="Фамилия"
              v-model="lastName"
              required
            ></v-text-field>
            <v-text-field
              label="E-mail"
              type="email"
              v-model="email"
              v-validate="'required|email'"
              data-vv-name="email"
              :error-messages="errors.collect('email')"
              required
            ></v-text-field>
            <div class="subheading secondary--text text--lighten-2">Является ли пользователь суперпользователем <span v-if="isSuperuser">(Да)</span><span v-else>(Нет)</span></div>
            <v-checkbox
              label="Суперпользователь"
              v-model="isSuperuser"
            ></v-checkbox>
            <div class="subheading secondary--text text--lighten-2">Активен ли пользователь <span v-if="isActive">(Да)</span><span v-else>(Нет)</span></div>
            <v-checkbox
              label="Активен"
              v-model="isActive"
            ></v-checkbox>
            <v-layout align-center>
              <v-flex shrink>
                <v-checkbox
                  v-model="setPassword"
                  class="mr-2"
                ></v-checkbox>
              </v-flex>
              <v-flex>
                <v-text-field
                  :disabled="!setPassword"
                  type="password"
                  ref="password"
                  label="Новый пароль"
                  data-vv-name="password"
                  data-vv-delay="100"
                  v-validate="{required: setPassword}"
                  v-model="password1"
                  :error-messages="errors.first('password')"
                >
                </v-text-field>
                <v-text-field
                  v-show="setPassword"
                  type="password"
                  label="Новый пароль еще раз"
                  data-vv-name="password_confirmation"
                  data-vv-delay="100"
                  data-vv-as="password"
                  v-validate="{required: setPassword, confirmed: 'password'}"
                  v-model="password2"
                  :error-messages="errors.first('password_confirmation')"
                >
                </v-text-field>
              </v-flex>
            </v-layout>
          </v-form>
        </template>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="cancel">Отменить</v-btn>
        <v-btn @click="reset">Сбросить</v-btn>
        <v-btn
          @click="submit"
          :disabled="!valid"
        >
          Сохранить
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { IUserProfile, IUserProfileUpdate } from '@/interfaces';
import { dispatchGetUsers, dispatchUpdateUser } from '@/store/admin/actions';
import { readAdminOneUser } from '@/store/admin/getters';
@Component
export default class EditUser extends Vue {
  public valid = true;
  public firstName: string = '';
  public lastName: string = '';
  public email: string = '';
  public isActive: boolean = true;
  public isSuperuser: boolean = false;
  public setPassword = false;
  public password1: string = '';
  public password2: string = '';
  public async mounted() {
    await dispatchGetUsers(this.$store);
    this.reset();
  }
  public reset() {
    this.setPassword = false;
    this.password1 = '';
    this.password2 = '';
    this.$validator.reset();
    if (this.user) {
      this.firstName = this.user.first_name;
      this.lastName = this.user.last_name;
      this.email = this.user.email;
      this.isActive = this.user.is_active;
      this.isSuperuser = this.user.is_superuser;
    }
  }
  public cancel() {
    this.$router.back();
  }
  public async submit() {
    if (await this.$validator.validateAll()) {
      const updatedProfile: IUserProfileUpdate = {};
      if (this.firstName) {
        updatedProfile.first_name = this.firstName;
      }
      if (this.lastName) {
        updatedProfile.last_name = this.lastName;
      }
      if (this.email) {
        updatedProfile.email = this.email;
      }
      updatedProfile.is_active = this.isActive;
      updatedProfile.is_superuser = this.isSuperuser;
      if (this.setPassword) {
        updatedProfile.password = this.password1;
        updatedProfile.password_confirmation = this.password2;
      }
      await dispatchUpdateUser(this.$store, { id: this.user!.id, user: updatedProfile });
      this.$router.push('/main/admin/users');
    }
  }
  get user() {
    return readAdminOneUser(this.$store)(+this.$router.currentRoute.params.id);
  }
}
</script>
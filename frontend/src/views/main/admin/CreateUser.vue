<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Добавление пользователя</div>
      </v-card-title>
      <v-card-text>
        <template>
          <v-form v-model="valid" ref="form" lazy-validation>
            <v-text-field label="Имя" v-model="firstName" required></v-text-field>
            <v-text-field label="Фамилия" v-model="lastName" required></v-text-field>
            <v-text-field label="E-mail" type="email" v-model="email" v-validate="'required|email'" data-vv-name="email" :error-messages="errors.collect('email')" required></v-text-field>
            <v-select
                v-model="role_id"
                label="Роль"
                :items="roles"
                item-text="name"
                item-value="id"
            ></v-select>
            <div class="subheading primary--text">Является ли пользователь суперпользователем <span v-if="isSuperuser">(Да)</span><span v-else>(Нет)</span></div>
            <v-checkbox label="Суперпользователь" v-model="isSuperuser"></v-checkbox>
            <div class="subheading primary--text">Активен ли пользователь <span v-if="isActive">(Да)</span><span v-else>(Нет)</span></div>
            <v-checkbox label="Активен" v-model="isActive"></v-checkbox>
            <v-layout align-center>
              <v-flex>
                <v-text-field
                    type="password"
                    ref="password"
                    label="Пароль"
                    data-vv-name="password"
                    data-vv-delay="100"
                    v-validate="{required: true}"
                    v-model="password1"
                    :error-messages="errors.first('password')">
                </v-text-field>
                <v-text-field
                    type="password"
                    label="Пароль еще раз"
                    data-vv-name="password_confirmation"
                    data-vv-delay="100"
                    data-vv-as="password"
                    v-validate="{
                      required: true,
                      confirmed: 'password'
                    }"
                    v-model="password2"
                    :error-messages="errors.first('password_confirmation')">
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
        <v-btn @click="submit" :disabled="!valid">
              Сохранить
            </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import {
  IUserProfile,
  IUserProfileUpdate,
  IUserProfileCreate,
} from '@/interfaces';
import { dispatchGetUsers, dispatchCreateUser, dispatchGetRoles } from '@/store/admin/actions';
import {readAdminRoles} from "@/store/admin/getters";
@Component
export default class CreateUser extends Vue {
  public valid = false;
  public firstName: string = '';
  public lastName: string = '';
  public email: string = '';
  public role_id: number = 0;
  public isActive: boolean = true;
  public isSuperuser: boolean = false;
  public setPassword = false;
  public password1: string = '';
  public password2: string = '';
  public async mounted() {
    await dispatchGetUsers(this.$store);
    await dispatchGetRoles(this.$store);
    this.reset();
  }
  public reset() {
    this.password1 = '';
    this.password2 = '';
    this.firstName = '';
    this.lastName = '';
    this.email = '';
    this.role_id = 0;
    this.isActive = true;
    this.isSuperuser = false;
    this.$validator.reset();
  }
  public cancel() {
    this.$router.back();
  }
  public async submit() {
    if (await this.$validator.validateAll()) {
      const updatedProfile: IUserProfileCreate = {
        email: this.email,
        password: this.password1,
        password_confirmation: this.password2,
        role_id: this.role_id,
      };
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
      await dispatchCreateUser(this.$store, updatedProfile);
      this.$router.push('/main/admin/users');
    }
  }
  get roles() {
    return readAdminRoles(this.$store)
  }
}
</script>
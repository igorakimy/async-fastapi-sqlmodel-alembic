<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title>
        Пользователи
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="secondary" to="/main/admin/users/create">Добавить пользователя</v-btn>
    </v-toolbar>
    <v-data-table
      :headers="headers"
      :items="users"
      :rows-per-page-items='[10,25,50,{"text":"Все","value":-1}]'
      :rows-per-page-text="'Кол-во записей на странице:'">
      <template slot="items" slot-scope="props">
        <td>{{ props.item.first_name }}</td>
        <td>{{ props.item.last_name }}</td>
        <td>{{ props.item.email }}</td>
        <td><v-icon v-if="props.item.is_active">checkmark</v-icon></td>
        <td><v-icon v-if="props.item.is_superuser">checkmark</v-icon></td>
        <td>
          {{ props.item.role.name }}
        </td>
        <td class="justify-center layout px-0 ">
          <v-tooltip top>
            <span>Редактировать</span>
            <v-btn slot="activator" flat icon color="secondary" :to="{name: 'main-admin-users-edit', params: {id: props.item.id}}">
              <v-icon>edit</v-icon>
            </v-btn>
          </v-tooltip>
          <v-tooltip top>
            <span>Удалить</span>
            <v-btn slot="activator" flat icon color="error" @click="deleteUser(props.item.id)">
              <v-icon>delete</v-icon>
            </v-btn>
          </v-tooltip>
        </td>
      </template>
      <template v-slot:pageText="props">
        Показаны записи {{ props.pageStart }} - {{ props.pageStop }} из {{ props.itemsLength }}
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import { IUserProfile } from '@/interfaces';
import { readAdminUsers, readAdminRoles } from '@/store/admin/getters';
import { dispatchGetUsers, dispatchGetRoles, dispatchDeleteUser } from '@/store/admin/actions';
@Component
export default class AdminUsers extends Vue {
  public headers = [
    {
      text: 'Имя',
      sortable: true,
      value: 'first_name',
      align: 'left',
    },
    {
      text: 'Фамилия',
      sortable: true,
      value: 'last_name',
      align: 'left',
    },
    {
      text: 'Email',
      sortable: true,
      value: 'email',
      align: 'left',
    },
    {
      text: 'Активность',
      sortable: true,
      value: 'isActive',
      align: 'left',
    },
    {
      text: 'Суперпользователь',
      sortable: true,
      value: 'isSuperuser',
      align: 'left',
    },
    {
      text: 'Роль',
      sortable: true,
      value: 'role_id',
      align: 'left',
    },
    {
      text: 'Действия',
      value: 'id',
      align: 'center',
    },
  ];
  get users() {
    return readAdminUsers(this.$store);
  }
  get roles() {
    return readAdminRoles(this.$store);
  }
  public async mounted() {
    await dispatchGetUsers(this.$store);
    await dispatchGetRoles(this.$store);
  }
  async deleteUser(userId: number) {
    await dispatchDeleteUser(this.$store, { id: userId })
  }

}
</script>
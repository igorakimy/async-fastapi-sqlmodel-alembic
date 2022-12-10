<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title>
        Роли
      </v-toolbar-title>
      <v-spacer></v-spacer>
<!--      <v-btn color="primary" to="/main/admin/roles/create">Добавить роль</v-btn>-->
    </v-toolbar>
    <v-data-table
      :headers="headers"
      :items="roles"
      :rows-per-page-items='[10,25,50,{"text":"Все","value":-1}]'
      :rows-per-page-text="'Кол-во записей на странице:'">
      <template slot="items" slot-scope="props">
        <td>{{ props.item.name }}</td>
        <td>{{ props.item.slug }}</td>
        <td>{{ props.item.description }}</td>
        <td class="justify-center layout px-0 ">
          <v-tooltip top>
            <span>Редактировать</span>
            <v-btn slot="activator" flat icon color="secondary" :to="{name: 'main-admin-roles-edit', params: {id: props.item.id}}">
              <v-icon>edit</v-icon>
            </v-btn>
          </v-tooltip>
          <v-tooltip top>
            <span>Удалить</span>
            <v-btn slot="activator" flat icon color="error" @click="deleteRole(props.item.id)">
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
import { readAdminRoles } from '@/store/admin/getters';
import { dispatchGetRoles, dispatchDeleteRole } from '@/store/admin/actions';
@Component
export default class AdminRoles extends Vue {
  public headers = [
    {
      text: 'Название',
      sortable: true,
      value: 'name',
      align: 'left',
    },
    {
      text: 'URL',
      sortable: true,
      value: 'slug',
      align: 'left',
    },
    {
      text: 'Описание',
      sortable: true,
      value: 'description',
      align: 'left',
    },
    {
      text: 'Действия',
      value: 'id',
      align: 'center',
    },
  ];
  get roles() {
    return readAdminRoles(this.$store);
  }
  public async mounted() {
    await dispatchGetRoles(this.$store);
  }
  async deleteRole(roleId: number) {
    await dispatchDeleteRole(this.$store, { id: roleId })
  }

}
</script>
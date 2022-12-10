<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Редактирование роли</div>
      </v-card-title>
      <v-card-text>
        <template>
          <v-form
            v-model="valid"
            ref="form"
            lazy-validation
          >
            <v-text-field
              label="Название"
              v-model="name"
              required
            ></v-text-field>
            <v-text-field
              label="URL"
              v-model="slug"
              required
            ></v-text-field>
            <v-text-field
              v-model="description"
              label="Description"
            ></v-text-field>
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
import { IRoleSelect, IRoleUpdate } from '@/interfaces';
import { dispatchGetRoles, dispatchUpdateRole } from '@/store/admin/actions';
import { readAdminRoles, readAdminOneRole} from '@/store/admin/getters';
@Component
export default class EditUser extends Vue {
  public valid = true;
  public name: string = '';
  public slug: string = '';
  public description: string = '';
  public async mounted() {
    await dispatchGetRoles(this.$store)
    this.reset();
  }
  public reset() {
    this.name = '';
    this.slug = '';
    this.description = '';
    this.$validator.reset();
    if (this.role) {
      this.name = this.role.name;
      this.slug = this.role.slug;
      this.description = this.role.description;
    }
  }
  public cancel() {
    this.$router.back();
  }
  public async submit() {
    if (await this.$validator.validateAll()) {
      const updatedRole: IRoleUpdate = {};
      if (this.name) {
        updatedRole.name = this.name;
      }
      if (this.slug) {
        updatedRole.slug = this.slug;
      }
      if (this.description) {
        updatedRole.description = this.description;
      }
      await dispatchUpdateRole(this.$store, { id: this.role!.id, role: updatedRole });
      this.$router.push('/main/admin/roles');
    }
  }
  get role() {
    return readAdminOneRole(this.$store)(+this.$router.currentRoute.params.id);
  }
  get roles() {
    return readAdminRoles(this.$store)
  }
}
</script>
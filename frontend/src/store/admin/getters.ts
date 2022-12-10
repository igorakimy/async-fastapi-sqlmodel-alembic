import { AdminState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const getters = {
    adminUsers: (state: AdminState) => state.users,
    adminOneUser: (state: AdminState) => (userId: number) => {
        const filteredUsers = state.users.filter((user) => user.id === userId);
        if (filteredUsers.length > 0) {
            return { ...filteredUsers[0] };
        }
    },
    adminRoles: (state: AdminState) => state.roles,
    adminOneRole: (state: AdminState) => (roleId: number) => {
        const filterRoles = state.roles.filter((role) => role.id === roleId);
        if (filterRoles.length > 0) {
            return { ...filterRoles[0] };
        }
    }
};

const { read } = getStoreAccessors<AdminState, State>('');

export const readAdminOneUser = read(getters.adminOneUser);
export const readAdminUsers = read(getters.adminUsers);
export const readAdminRoles = read(getters.adminRoles);
export const readAdminOneRole = read(getters.adminOneRole);
import {IRoleSelect, IUserProfile} from '@/interfaces';
import { AdminState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const mutations = {
    setUsers(state: AdminState, payload: IUserProfile[]) {
        state.users = payload;
    },
    setUser(state: AdminState, payload: IUserProfile) {
        const users = state.users.filter((user: IUserProfile) => user.id !== payload.id);
        users.push(payload);
        state.users = users;
    },
    unsetUser(state: AdminState, payload: IUserProfile) {
        state.users = state.users.filter((user: IUserProfile) => user.id !== payload.id);
    },
    setRoles(state: AdminState, payload: IRoleSelect[]) {
        state.roles = payload;
    },
    setRole(state: AdminState, payload: IRoleSelect) {
        const roles = state.roles.filter((role: IRoleSelect) => role.id !== payload.id);
        roles.push(payload);
        state.roles = roles;
    },
    unsetRole(state: AdminState, payload: IRoleSelect) {
        state.roles = state.roles.filter((role: IRoleSelect) => role.id !== payload.id);
    }
};

const { commit } = getStoreAccessors<AdminState, State>('');

export const commitSetUser = commit(mutations.setUser);
export const commitSetUsers = commit(mutations.setUsers);
export const commitUnsetUser = commit(mutations.unsetUser);
export const commitSetRoles = commit(mutations.setRoles);
export const commitSetRole = commit(mutations.setRole);
export const commitUnsetRole = commit(mutations.unsetRole);
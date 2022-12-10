import { api } from '@/api';
import { ActionContext } from 'vuex';
import {IRoleUpdate, IUserProfile, IUserProfileCreate, IUserProfileUpdate} from '@/interfaces';
import { State } from '../state';
import { AdminState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import {
    commitSetUsers,
    commitSetUser,
    commitUnsetUser,
    commitSetRoles,
    commitUnsetRole,
    commitSetRole,
} from './mutations';
import { dispatchCheckApiError } from '../main/actions';
import { commitAddNotification, commitRemoveNotification } from '../main/mutations';

type MainContext = ActionContext<AdminState, State>;

export const actions = {
    async actionGetUsers(context: MainContext) {
        try {
            const response = await api.getUsers(context.rootState.main.token);
            if (response) {
                commitSetUsers(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionUpdateUser(context: MainContext, payload: { id: number, user: IUserProfileUpdate }) {
        try {
            const loadingNotification = { content: 'Сохранение...', showProgress: true };
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.updateUser(context.rootState.main.token, payload.id, payload.user),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitSetUser(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Пользователь успешно обновлен', color: 'success' });
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionCreateUser(context: MainContext, payload: IUserProfileCreate) {
        const loadingNotification = { content: 'Сохранение...', showProgress: true };
        try {
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.createUser(context.rootState.main.token, payload),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitSetUser(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Пользователь успешно создан', color: 'success' });
        } catch (error) {
            commitRemoveNotification(context, loadingNotification);
            await dispatchCheckApiError(context, error);
        }
    },
    async actionDeleteUser(context: MainContext, payload: { id: number }) {
        if (!confirm('Вы уверены, что хотите удалить?')) {
            return
        }
        const loadingNotification = { content: 'Удаление...', showProgress: true };
        try {
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.deleteUser(context.rootState.main.token, payload.id),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0]
            commitUnsetUser(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Пользователь удален', color: 'success' });
        } catch (error) {
            await dispatchCheckApiError(context, error)
        }
    },
    async actionGetRoles(context: MainContext) {
        try {
            const response = await api.getRoles(context.rootState.main.token);
            if (response) {
                commitSetRoles(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionUpdateRole(context: MainContext, payload: {id: number, role: IRoleUpdate}) {
        const loadingNotification = { content: 'Сохранение...', showProgress: true };
        try {
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.updateRole(context.rootState.main.token, payload.id, payload.role),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitSetRole(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Роль успешно обновлена', color: 'success' });
        } catch (error) {
            commitRemoveNotification(context, loadingNotification);
            await dispatchCheckApiError(context, error);
        }
    },
    async actionDeleteRole(context: MainContext, payload: {id: number}) {
        if (!confirm('Вы уверены, что хотите удалить роль?')) {
            return
        }
        const loadingNotification = { content: 'Удаление...', showProgress: true };
        try {
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.deleteRole(context.rootState.main.token, payload.id),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0]
            commitUnsetRole(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Роль удалена', color: 'success' });
        } catch (error) {
            commitRemoveNotification(context, loadingNotification);
            await dispatchCheckApiError(context, error)
        }
    }
};

const { dispatch } = getStoreAccessors<AdminState, State>('');

export const dispatchCreateUser = dispatch(actions.actionCreateUser);
export const dispatchGetUsers = dispatch(actions.actionGetUsers);
export const dispatchUpdateUser = dispatch(actions.actionUpdateUser);
export const dispatchDeleteUser = dispatch(actions.actionDeleteUser);
export const dispatchGetRoles = dispatch(actions.actionGetRoles);
export const dispatchUpdateRole = dispatch(actions.actionUpdateRole);
export const dispatchDeleteRole = dispatch(actions.actionDeleteRole);
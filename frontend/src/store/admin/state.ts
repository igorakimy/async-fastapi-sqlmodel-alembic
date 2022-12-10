import {IRoleSelect, IUserProfile} from '@/interfaces';

export interface AdminState {
    users: IUserProfile[];
    roles: IRoleSelect[];
}
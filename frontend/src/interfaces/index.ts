export interface IUserProfile {
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    first_name: string;
    last_name: string;
    role_id: number;
    role: IRoleSelect;
    id: number;
}

export interface IUserProfileUpdate {
    email?: string;
    first_name?: string;
    last_name?: string;
    password?: string;
    password_confirmation?: string;
    role_id?: number;
    is_active?: boolean;
    is_superuser?: boolean;
}

export interface IUserProfileCreate {
    email: string;
    password: string;
    password_confirmation: string;
    role_id: number;
    first_name?: string;
    last_name?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}

export interface IRoleSelect {
    id: number;
    name: string;
    slug: string;
    description: string;
}

export interface IRoleUpdate {
    name?: string;
    slug?: string;
    description?: string;
}

export interface IRoleCreate {
    name: string;
    slug: string;
    description: string;
}

export interface IUserProfile {
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    first_name: string;
    last_name: string;
    id: number;
}

export interface IUserProfileUpdate {
    email?: string;
    first_name?: string;
    last_name?: string;
    password?: string;
    password_confirmation?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}

export interface IUserProfileCreate {
    email: string;
    password: string;
    password_confirmation: string;
    first_name?: string;
    last_name?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}

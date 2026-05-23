import { apiGet, apiPatch, apiPost } from "./api";
import type { User, UserRole } from "../types/user";

export interface CreateUserPayload {
  email: string;
  first_name: string;
  last_name: string;
  role: UserRole;
  temp_password: string;
}

export const adminService = {
  listUsers() {
    return apiGet<User[]>("/admin/users");
  },
  createUser(payload: CreateUserPayload) {
    return apiPost<User>("/admin/users", payload);
  },
  setStatus(userId: number, isActive: boolean) {
    return apiPatch<User>(`/admin/users/${userId}/status`, { is_active: isActive });
  },
};

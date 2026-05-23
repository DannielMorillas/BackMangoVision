import { apiGet, apiPost } from "./api";
import type { TokenResponse, User } from "../types/user";

export interface LoginPayload {
  email: string;
  password: string;
}

export interface ForgotResponse {
  message: string;
  debug_token: string | null;
  debug_expires_at: string | null;
}

export const authService = {
  login(payload: LoginPayload) {
    return apiPost<TokenResponse>("/auth/login", payload);
  },
  logout() {
    return apiPost<void>("/auth/logout");
  },
  me() {
    return apiGet<User>("/auth/me");
  },
  forgotPassword(email: string) {
    return apiPost<ForgotResponse>("/auth/forgot-password", { email });
  },
  resetPassword(token: string, new_password: string) {
    return apiPost<void>("/auth/reset-password", { token, new_password });
  },
};

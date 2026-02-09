import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
  token: string | null;
  username: string | null;
  setToken: (token: string) => void;
  setUsername: (username: string) => void;
  logout: () => void;
  isAuthenticated: () => boolean;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      token: null,
      username: null,
      setToken: (token) => set({ token }),
      setUsername: (username) => set({ username }),
      logout: () => set({ token: null, username: null }),
      isAuthenticated: () => !!get().token,
    }),
    {
      name: 'auth-storage', // key in localStorage
    }
  )
);

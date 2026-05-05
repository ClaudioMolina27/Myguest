import { create } from 'zustand'

const useAuthStore = create((set) => ({
  token: localStorage.getItem('token') || null,
  usuario: null,

  setToken: (token) => {
    localStorage.setItem('token', token)
    set({ token })
  },

  setUsuario: (usuario) => set({ usuario }),

  logout: () => {
    localStorage.removeItem('token')
    set({ token: null, usuario: null })
  }
}))

export default useAuthStore
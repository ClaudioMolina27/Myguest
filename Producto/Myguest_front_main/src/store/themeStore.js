import { create } from 'zustand'

const useThemeStore = create((set) => ({
  isDark: localStorage.getItem('theme') === 'dark' || true,

  toggleTheme: () => set((state) => {
    const newTheme = !state.isDark
    localStorage.setItem('theme', newTheme ? 'dark' : 'light')
    return { isDark: newTheme }
  })
}))

export default useThemeStore
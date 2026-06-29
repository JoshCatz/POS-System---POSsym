
import { create } from 'zustand'

const useRestaurantAuth = create((set) => ({
    token: null,
    employee: null,
    login: (token, employee) => set({ token, employee }),
    logout: () => set({ token: null, employee: null })
}))

export default useRestaurantAuth
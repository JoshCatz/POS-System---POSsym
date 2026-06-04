import { create } from 'zustand'
import { persist } from 'zustand/middleware'

const useEmployeeAuth = create(
    persist(
        (set) => ({
            token: null,
            employee: null,
            login: (token, employee) => set({ token, employee }),
            logout: () => set({ token: null, employee: null })
        }),
        { name: 'employee-auth' }
    )
)

export default useEmployeeAuth
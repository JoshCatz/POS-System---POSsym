// src/portals/employee/pages/Dashboard.jsx
import { useNavigate } from 'react-router-dom'
import useEmployeeAuth from '../../../stores/authStore'

export default function Dashboard() {
    const { employee, logout } = useEmployeeAuth()
    const navigate = useNavigate()

    const handleLogout = () => {
        logout()
        navigate('/employee/login')
    }

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
            <div className="bg-white p-8 rounded-lg shadow-md">
                <h1 className="text-2xl font-bold mb-4">Employee Dashboard</h1>
                <p className="text-gray-600 mb-6">
                    Logged in as: {employee?.email}
                </p>
                <button
                    onClick={handleLogout}
                    className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
                >
                    Logout
                </button>
            </div>
        </div>
    )
}
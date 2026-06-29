import { useNavigate } from "react-router-dom"
import useRestaurantAuth from '../../../stores/restaurantAuthStore'

export default function Menu() {
  const {employee, logout} =  useRestaurantAuth()
  const navigate = useNavigate()

    const handleLogout = () => {
        logout()
        navigate('/employee/login')
    }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <div className="border-2 flex flex-col items-center gap-4 p-10 rounded-3xl">
        <p>Hello {employee?.name}</p>
        <button onClick={handleLogout} className="border-2 p-2 rounded-2xl">logout</button>
      </div>
    </div>

  )
}
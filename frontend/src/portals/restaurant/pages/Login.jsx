import { useState } from "react"
import { useNavigate } from "react-router-dom"
import api from '../../../services/api'
import useRestaurantAuth from '../../../stores/restaurantAuthStore'

export default function RestaurantLogin() {
  const [pin, setPin] = useState("");
  const [error, setError] = useState("")

  const { login } = useRestaurantAuth()
  const navigate = useNavigate()

  const handlePress = (digit) => setPin(prev => prev + digit);
  const handleDelete = () => setPin(prev => prev.slice(0, -1));

// handles the submission of the login form
  const handleSubmit = async () => {
    setError(null); // sets the default error to null

        // tries to send credentials to backend
    try {
      const response = await api.post('/auth/login/pos', {
        pin: pin // sends pin!
      });

      const { access_token, name, role } = response.data; // pulls the access token and role based from the response data
      login(access_token, { name, role }); // store the token and user info in authStore
      navigate('/restaurant/menu'); //navigate to the restaurant menu

    } catch (err) {
      setError(err.response?.data?.message || 'Invalid credentials'); // shows the backend error message or fallback if none exist - 'Invalid credentials'
    };
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="flex flex-col items-center gap-6 bg-white p-8 rounded-2xl shadow-md">
        
        {/* PIN display */}
        <div className="text-3xl tracking-widest h-10">
          {pin.replace(/./g, '●') || <span className="text-gray-300">● ● ● ●</span>}
        </div>

        {/* Keypad */}
        <div className="flex flex-col gap-3">
          <div className="flex gap-3">
            <button type="button" onClick={() => handlePress("1")} className="w-20 h-20 text-2xl border-2 rounded-full flex items-center justify-center hover:bg-gray-100">1</button>
            <button type="button" onClick={() => handlePress("2")} className="w-20 h-20 text-2xl border-2 rounded-full flex items-center justify-center hover:bg-gray-100">2</button>
            <button type="button" onClick={() => handlePress("3")} className="w-20 h-20 text-2xl border-2 rounded-full flex items-center justify-center hover:bg-gray-100">3</button>
          </div>
          <div className="flex gap-3">
            <button type="button" onClick={() => handlePress("4")} className="w-20 h-20 text-2xl border-2 rounded-full flex items-center justify-center hover:bg-gray-100">4</button>
            <button type="button" onClick={() => handlePress("5")} className="w-20 h-20 text-2xl border-2 rounded-full flex items-center justify-center hover:bg-gray-100">5</button>
            <button type="button" onClick={() => handlePress("6")} className="w-20 h-20 text-2xl border-2 rounded-full flex items-center justify-center hover:bg-gray-100">6</button>
          </div>
          <div className="flex gap-3">
            <button type="button" onClick={() => handlePress("7")} className="w-20 h-20 text-2xl border-2 rounded-full flex items-center justify-center hover:bg-gray-100">7</button>
            <button type="button" onClick={() => handlePress("8")} className="w-20 h-20 text-2xl border-2 rounded-full flex items-center justify-center hover:bg-gray-100">8</button>
            <button type="button" onClick={() => handlePress("9")} className="w-20 h-20 text-2xl border-2 rounded-full flex items-center justify-center hover:bg-gray-100">9</button>
          </div>
          <div className="flex gap-3">
            <button type="button" onClick={handleDelete} className="w-20 h-20 text-lg border-2 rounded-full flex items-center justify-center hover:bg-gray-100">⌫</button>
            <button type="button" onClick={() => handlePress("0")} className="w-20 h-20 text-2xl border-2 rounded-full flex items-center justify-center hover:bg-gray-100">0</button>
            <button type="button" onClick={handleSubmit} className="w-20 h-20 text-lg border-2 rounded-full flex items-center justify-center hover:bg-gray-100">✓</button>
          </div>
        </div>

      </div>
    </div>
  )
}
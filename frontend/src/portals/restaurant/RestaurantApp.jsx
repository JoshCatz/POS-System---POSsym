import { Routes, Route } from 'react-router-dom'
import Login from './pages/Login'
import Floor from './pages/Floor'
import Menu from './pages/Menu'

export default function RestaurantApp() {
  return (
    <Routes>
      <Route path="login" element={<Login />} />
      <Route path="floor" element={<Floor />} />
      <Route path="menu" element={<Menu />} />
    </Routes>
  )
}
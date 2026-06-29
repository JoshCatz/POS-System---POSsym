import { Routes, Route } from 'react-router-dom'
import Login from './pages/Login'
import Floor from './pages/Floor'
import Menu from './pages/Menu'
import ProtectedRestaurantRoute from '../../components/ProtectedRestaurantRoute'

export default function RestaurantApp() {
  return (
    <Routes>
      <Route 
        path="login" 
        element={
            <Login />
        } 
      />
      <Route 
        path="floor"
        element={
          <ProtectedRestaurantRoute>
            <Floor />
          </ProtectedRestaurantRoute>
        }
      />
      <Route 
        path="menu"
        element={
          <ProtectedRestaurantRoute>
            <Menu />
          </ProtectedRestaurantRoute>
        }
      />
    </Routes>
  )
}
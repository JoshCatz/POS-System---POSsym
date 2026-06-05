import { Routes, Route } from 'react-router-dom'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import ProtectedRoute from '../../components/ProtectedRoute'

export default function EmployeeApp() {
  return (
    <Routes>
      <Route path="login" element={<Login />} />
      <Route 
        path="dashboard" 
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        } 
      />
    </Routes>
  )
}
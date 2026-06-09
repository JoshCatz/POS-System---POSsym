import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import EmployeeApp from './portals/employee/EmployeeApp'
import RestaurantApp from './portals/restaurant/RestaurantApp'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/employee/*" element={<EmployeeApp />} />
        <Route path="/restaurant/*" element={<RestaurantApp />} />
        <Route path="/" element={<Navigate to="/employee/login" />} />
      </Routes>
    </BrowserRouter>
  )
}
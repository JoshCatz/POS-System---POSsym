import { Navigate } from 'react-router-dom';
import useEmployeeAuth from '../stores/restaurantAuthStore';
import useRestaurantAuth from '../stores/restaurantAuthStore';

export default function ProtectedRestaurantRoute({ children }) {
    const { token } = useRestaurantAuth();

    if (!token) {
        return <Navigate to="/restaurant/login/" replace />
    };

    return children;
}
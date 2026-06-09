import { Navigate } from 'react-router-dom';
import useEmployeeAuth from '../stores/authStore';

export default function ProtectedRoute({ children }) {
    const { token } = useEmployeeAuth();

    if (!token) {
        return <Navigate to="/employee/login/" replace />
    };

    return children;
}
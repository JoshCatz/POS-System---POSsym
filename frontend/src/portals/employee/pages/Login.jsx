import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import api from '../../../services/api'
import useEmployeeAuth from '../../../stores/authStore'

export default function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    const { login } = useEmployeeAuth();
    const { token } = useEmployeeAuth();
    const navigate = useNavigate();

    useEffect(() => {
        if (token) {
            navigate('/employee/dashboard/')
        }
    }, [token, navigate])

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const response = await api.post('/auth/login/portal', {
                username: username,
                password: password
            });

            const { access_token, role } = response.data;
            login(access_token, { username, role });
            navigate('/employee/dashboard');

        } catch (err) {
            setError(err.response?.data?.message || 'Invalid credentials');
        } finally {
            setLoading(false);
        };
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <div className='flex flex-col border-2 p-4'>
                <h1 className="text-xl text-center pb-2">Employee Login</h1>
                {error && (
                    <p className="text-red-500 text-sm text-center mb-4">{error}</p>
                )}
                <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                    <div className="flex items-center justify-between gap-4">
                        <label htmlFor="username">Username: </label>
                        <input
                            type="text"
                            id="username"
                            className="border-0 border-b-2"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="Enter your username"
                        />
                    </div>
                    <div className="flex items-center justify-between gap-4">
                        <label htmlFor="password">Password: </label>
                        <input
                            type="password"
                            id="password"
                            className="border-0 border-b-2 "
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Enter your password"
                        />
                    </div>
                    <button
                        type="submit"
                        disabled={loading}
                        className="border-2 py-1 disabled:opacity-50"
                    >
                        {loading ? 'Logging in...' : 'Login'}
                    </button>
                </form>
            </div>
        </div>
    );
};
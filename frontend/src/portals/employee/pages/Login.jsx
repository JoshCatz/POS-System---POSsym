import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import api from '../../../services/api'
import useEmployeeAuth from '../../../stores/authStore'

export default function Login() {
    const [username, setUsername] = useState(''); // tracks username input
    const [password, setPassword] = useState(''); // tracks password input
    const [error, setError] = useState(null); // sets the error - default null
    const [loading, setLoading] = useState(false); // sets the loading state - default false

    const { login } = useEmployeeAuth(); // login action from authStore
    const { token } = useEmployeeAuth(); // current token from authStore
    const navigate = useNavigate(); // used to redirect the user

    // checks if a token exist - if it does, navigate to the dashboard
    useEffect(() => {
        if (token) {
            navigate('/employee/dashboard/')
        }
    }, [token, navigate]) // re-runs if token or navigate is changed

    // handles the submission of the login form
    const handleSubmit = async (e) => {
        e.preventDefault(); // prevents the page from refreshing on submit
        setLoading(true); // sets the state of loading to true
        setError(null); // sets the default error to null

        // tries to send credentials to backend
        try {
            const response = await api.post('/auth/login/portal', {
                username: username, // sends the username from the username state
                password: password // sends the password from the password state
            });

            const { access_token, role } = response.data; // pulls the access token and role based from the response data
            login(access_token, { username, role }); // store the token and user info in authStore
            navigate('/employee/dashboard'); //navigate to the employee dashboard

        } catch (err) {
            setError(err.response?.data?.message || 'Invalid credentials'); // shows the backend error message or fallback if none exist - 'Invalid credentials'
        } finally {
            setLoading(false); // lastly we change loading to false - re-enabling the button
        };
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <div className='flex flex-col border-2 p-4'>
                <h1 className="text-xl text-center pb-2">Employee Login</h1>
                {/* Only renders if error is not null */}
                {error && (
                    <p className="text-red-500 text-sm text-center mb-4">{error}</p>
                )}
                {/* Form for capturing username and password */}
                <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                    <div className="flex items-center justify-between gap-4">
                        <label htmlFor="username">Username: </label>
                        <input
                            type="text"
                            id="username"
                            className="border-0 border-b-2"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)} // When changed, set the username to value  
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
                            onChange={(e) => setPassword(e.target.value)} // When changed, set the password to value
                            placeholder="Enter your password"
                        />
                    </div>
                    <button
                        type="submit"
                        disabled={loading} // disables the button while a request is processing
                        className="border-2 py-1 disabled:opacity-50"
                    >
                        {loading ? 'Logging in...' : 'Login'} {/* Swaps button text while loading */}
                    </button>
                </form>
            </div>
        </div>
    );
};
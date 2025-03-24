import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./css/Login.css"; // Import the CSS file

const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleLogin = async () => {
        try {
            const res = await axios.post("http://localhost:5000/login", { username, password }, { withCredentials: true });
            localStorage.setItem("isAuthenticated", "true");
            localStorage.setItem("role", res.data.role);
            navigate("/dashboard");
        } catch (error) {
            alert("Invalid credentials");
        }
    };

    return (
        <div className="login-page">
            <div className="login-container">
                <h2>Welcome</h2>
                <p>Sign in to continue</p>
                <input 
                    type="text" 
                    placeholder="Username" 
                    value={username} 
                    onChange={(e) => setUsername(e.target.value)} 
                    required 
                />
                <input 
                    type="password" 
                    placeholder="Password" 
                    value={password} 
                    onChange={(e) => setPassword(e.target.value)} 
                    required 
                />
                <button onClick={handleLogin}>Login</button>
            </div>
        </div>
    );
};

export default Login;

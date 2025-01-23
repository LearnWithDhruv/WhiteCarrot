import React from 'react';
import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google';
import { loginWithGoogle } from '../services/api'; // Backend API call

const Login = () => {

    const handleGoogleLoginSuccess = async (credentialResponse) => {
        try {
            const token = credentialResponse.credential;
    
            await new Promise((resolve) => setTimeout(resolve, 2000));
    
            const response = await loginWithGoogle(token);
            alert(response.data.message);
            window.location.href = '/calendar';
        } catch (error) {
            console.error('Login failed:', error);
        }
    };

    return (
        <GoogleOAuthProvider clientId="611881352751-qnlpqck9el3gaogsssd2cgk0ctidd1ou.apps.googleusercontent.com">
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
                <GoogleLogin
                    onSuccess={handleGoogleLoginSuccess}
                    onError={() => console.log('Login failed')}
                />
            </div>
        </GoogleOAuthProvider>
    );
};

export default Login;

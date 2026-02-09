import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import JSEncrypt from 'jsencrypt';
import { useAuthStore } from '../stores/authStore';
import { API_BASE_URL } from '../utils/constants';

const LoginPage: React.FC = () => {
    const [username, setUsernameInput] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [publicKey, setPublicKey] = useState('');

    const navigate = useNavigate();
    const location = useLocation();
    const { setToken, setUsername } = useAuthStore();

    // 获取重定向地址
    const from = location.state?.from?.pathname || '/';

    useEffect(() => {
        // 获取 RSA 公钥
        const fetchPublicKey = async () => {
            try {
                const response = await axios.get(`${API_BASE_URL}/api/v1/auth/public-key`);
                setPublicKey(response.data.public_key);
            } catch (err) {
                console.error('Failed to fetch public key', err);
                setError('无法连接到服务器获取安全密钥，请稍后重试');
            }
        };
        fetchPublicKey();
    }, []);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            if (!publicKey) {
                throw new Error('公钥未加载');
            }

            // RSA 加密密码
            const encrypt = new JSEncrypt();
            encrypt.setPublicKey(publicKey);
            const encryptedPassword = encrypt.encrypt(password);

            if (!encryptedPassword) {
                throw new Error('密码加密失败');
            }

            // 发送登录请求
            const response = await axios.post(`${API_BASE_URL}/api/v1/auth/login`, {
                username,
                encrypted_password: encryptedPassword,
            });

            const { access_token } = response.data;

            // 保存 Token 和用户名
            setToken(access_token);
            setUsername(username);

            // 跳转
            navigate(from, { replace: true });

        } catch (err: any) {
            console.error('Login failed', err);
            if (err.response) {
                setError(err.response.data.detail || '登录失败，请检查用户名或密码');
            } else {
                setError(err.message || '登录请求失败');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex min-h-screen items-center justify-center bg-base-200">
            <div className="w-full max-w-md p-8 space-y-6 bg-base-100 rounded-xl shadow-lg">
                <div className="text-center">
                    <h1 className="text-3xl font-bold text-primary">Daily Stock Analysis</h1>
                    <p className="mt-2 text-base-content/60">请登录以继续使用</p>
                </div>

                {error && (
                    <div className="alert alert-error text-sm py-2">
                        <svg xmlns="http://www.w3.org/2000/svg" className="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                        <span>{error}</span>
                    </div>
                )}

                <form className="space-y-4" onSubmit={handleSubmit}>
                    <div className="form-control w-full">
                        <label className="label">
                            <span className="label-text">用户名</span>
                        </label>
                        <input
                            type="text"
                            placeholder="输入用户名"
                            className="input input-bordered w-full"
                            value={username}
                            onChange={(e) => setUsernameInput(e.target.value)}
                            autoFocus
                            required
                        />
                    </div>

                    <div className="form-control w-full">
                        <label className="label">
                            <span className="label-text">密码</span>
                        </label>
                        <input
                            type="password"
                            placeholder="输入密码"
                            className="input input-bordered w-full"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        className="btn btn-primary w-full"
                        disabled={loading || !publicKey}
                    >
                        {loading ? (
                            <>
                                <span className="loading loading-spinner loading-sm"></span>
                                登录中...
                            </>
                        ) : '登录'}
                    </button>

                    {!publicKey && !error && (
                        <p className="text-xs text-center text-warning">正在建立安全连接...</p>
                    )}
                </form>
            </div>
        </div>
    );
};

export default LoginPage;

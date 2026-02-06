import type React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import NotFoundPage from './pages/NotFoundPage';
import { DockNav } from './components/common';
import './App.css';

const App: React.FC = () => {
    return (
        <Router>
            <div className="flex min-h-screen bg-base">
                {/* Dock 导航 */}
                <DockNav />

                {/* 主内容区 */}
                <main className="flex-1 dock-safe-area">
                    <Routes>
                        <Route path="/" element={<HomePage />} />
                        <Route path="*" element={<NotFoundPage />} />
                    </Routes>
                </main>
            </div>
        </Router>
    );
};

export default App;

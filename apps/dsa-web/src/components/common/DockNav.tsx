import type React from 'react';
import { NavLink } from 'react-router-dom';
import { HomeIcon, SettingsIcon, MenuIcon } from '../common';

type DockItem = {
    key: string;
    label: string;
    to: string;
    icon: React.FC<{ active?: boolean }>;
};

const NAV_ITEMS: DockItem[] = [
    {
        key: 'home',
        label: '首页',
        to: '/',
        icon: HomeIcon,
    },
];

export const DockNav: React.FC = () => {
    return (
        <aside className="dock-nav" aria-label="主导航">
            <div className="dock-surface">
                <NavLink to="/" className="dock-logo" title="首页" aria-label="首页">
                    <MenuIcon className="w-5 h-5" />
                </NavLink>

                <nav className="dock-items" aria-label="页面">
                    {NAV_ITEMS.map((item) => {
                        const Icon = item.icon;
                        return (
                            <NavLink
                                key={item.key}
                                to={item.to}
                                end={item.to === '/'}
                                title={item.label}
                                aria-label={item.label}
                                className={({ isActive }) => `dock-item${isActive ? ' is-active' : ''}`}
                            >
                                {({ isActive }) => <Icon active={isActive} />}
                            </NavLink>
                        );
                    })}
                </nav>

                <div className="dock-footer">
                    <button
                        type="button"
                        className="dock-item is-placeholder"
                        title="设置（即将推出）"
                        aria-disabled="true"
                        disabled
                    >
                        <SettingsIcon />
                    </button>
                </div>
            </div>
        </aside>
    );
};

import React, { forwardRef } from 'react';

export interface InputProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'prefix'> {
    label?: string;
    error?: string;
    prefix?: React.ReactNode;
    suffix?: React.ReactNode;
    fullWidth?: boolean;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
    ({ className = '', label, error, prefix, suffix, fullWidth = true, ...props }, ref) => {
        return (
            <div className={`${fullWidth ? 'w-full' : ''} ${className}`}>
                {label && (
                    <label className="block text-xs font-medium text-gray-400 mb-1.5 ml-1">
                        {label}
                    </label>
                )}
                <div className="relative group">
                    {prefix && (
                        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-500">
                            {prefix}
                        </div>
                    )}
                    <input
                        ref={ref}
                        className={`
              input-terminal
              ${prefix ? 'pl-9' : ''}
              ${suffix ? 'pr-9' : ''}
              ${error ? 'border-danger/50 focus:border-danger focus:ring-danger/20' : ''}
            `}
                        {...props}
                    />
                    {suffix && (
                        <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none text-gray-500">
                            {suffix}
                        </div>
                    )}
                </div>
                {error && (
                    <p className="mt-1 text-xs text-danger ml-1 animate-fade-in">{error}</p>
                )}
            </div>
        );
    }
);

Input.displayName = 'Input';

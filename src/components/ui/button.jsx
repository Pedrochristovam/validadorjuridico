import React from 'react'
import { cn } from '/src/lib/utils'

const Button = React.forwardRef(({ 
  className, 
  variant = 'default', 
  size = 'default', 
  children, 
  ...props 
}, ref) => {
  const variants = {
    default: 'bg-gradient-to-r from-blue-600 via-blue-500 to-indigo-600 text-white hover:from-blue-700 hover:via-blue-600 hover:to-indigo-700 shadow-lg shadow-blue-500/25 hover:shadow-xl hover:shadow-blue-500/35',
    outline: 'border-2 border-slate-200/60 bg-white/80 backdrop-blur-sm hover:bg-slate-50/80 hover:border-slate-300/60 shadow-sm hover:shadow-md',
    ghost: 'hover:bg-slate-100/80 backdrop-blur-sm',
  }

  const sizes = {
    default: 'h-10 px-4 py-2',
    sm: 'h-9 px-3',
    lg: 'h-11 px-8',
    icon: 'h-10 w-10',
  }

  return (
    <button
      className={cn(
        'inline-flex items-center justify-center rounded-xl text-sm font-semibold transition-all duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 disabled:cursor-not-allowed active:scale-[0.98]',
        variants[variant],
        sizes[size],
        className
      )}
      ref={ref}
      {...props}
    >
      {children}
    </button>
  )
})

Button.displayName = 'Button'

export { Button }


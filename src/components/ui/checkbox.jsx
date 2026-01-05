import React from 'react'
import { cn } from '@/lib/utils'
import { Check } from 'lucide-react'

const Checkbox = React.forwardRef(({ 
  className, 
  checked, 
  onCheckedChange, 
  ...props 
}, ref) => {
  const handleClick = () => {
    onCheckedChange?.(!checked)
  }

  return (
    <div
      ref={ref}
      className={cn(
        'peer h-4 w-4 shrink-0 rounded-sm border border-slate-200 ring-offset-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
        checked && 'bg-blue-600 border-blue-600 text-white',
        'flex items-center justify-center cursor-pointer',
        className
      )}
      onClick={handleClick}
      {...props}
    >
      {checked && <Check className="h-3 w-3" />}
    </div>
  )
})

Checkbox.displayName = 'Checkbox'

export { Checkbox }







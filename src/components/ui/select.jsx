import React, { useState, useRef, useEffect } from 'react'
import { cn } from '../../lib/utils'
import { ChevronDown } from 'lucide-react'

const Select = ({ value, onValueChange, children, models, ...props }) => {
  const [open, setOpen] = useState(false)
  const selectRef = useRef(null)

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (selectRef.current && !selectRef.current.contains(event.target)) {
        setOpen(false)
      }
    }
    if (open) {
      document.addEventListener('mousedown', handleClickOutside)
    }
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [open])

  return (
    <div className="relative w-full" ref={selectRef} {...props}>
      {React.Children.map(children, (child) => {
        if (!child) return null
        if (child.type === SelectTrigger) {
          return React.cloneElement(child, { open, setOpen, value, models })
        }
        if (child.type === SelectContent) {
          return React.cloneElement(child, { open, setOpen, value, onValueChange })
        }
        return null
      })}
    </div>
  )
}

const SelectTrigger = ({ className, children, open, setOpen, value, models, ...props }) => {
  return (
    <button
      type="button"
      onClick={(e) => {
        e.preventDefault()
        e.stopPropagation()
        setOpen(!open)
      }}
      className={cn(
        'flex h-10 w-full items-center justify-between rounded-xl border-2 border-slate-200 bg-white px-4 py-2.5 text-sm transition-all duration-300 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 focus:bg-white focus:shadow-lg hover:border-slate-300 disabled:cursor-not-allowed disabled:opacity-50',
        className
      )}
      style={{ backgroundColor: '#ffffff' }}
      {...props}
    >
      {children || <SelectValue value={value} models={models} />}
      <ChevronDown className={`h-4 w-4 text-slate-400 transition-transform duration-300 ${open ? 'rotate-180' : ''}`} />
    </button>
  )
}

const SelectValue = ({ placeholder, value, models }) => {
  if (value && value !== "" && models && models.length > 0) {
    const selectedModel = models.find(m => m.id === value)
    if (selectedModel) {
      return <span className="text-slate-700 font-medium">{selectedModel.name}</span>
    }
  }
  if (!value || value === "") {
    return <span className="text-slate-400">{placeholder}</span>
  }
  return <span className="text-slate-700">{value}</span>
}

const SelectContent = ({ className, children, open, setOpen, value, onValueChange, ...props }) => {
  if (!open) return null

  return (
    <div
      className={cn(
        'absolute z-[100] mt-2 max-h-60 w-full overflow-auto rounded-xl border-2 border-slate-200 bg-white p-2 shadow-2xl shadow-slate-900/10',
        className
      )}
      style={{ 
        backgroundColor: '#ffffff',
        minHeight: '40px',
        top: '100%',
        left: 0,
        right: 0
      }}
      {...props}
    >
      {React.Children.map(children, (child) => {
        if (!child) return null
        if (child.type === SelectItem) {
          return React.cloneElement(child, { 
            selectedValue: value,
            onValueChange, 
            setOpen 
          })
        }
        return child
      })}
    </div>
  )
}

const SelectItem = ({ className, children, value: itemValue, onValueChange, setOpen, selectedValue, ...props }) => {
  const isSelected = selectedValue === itemValue

  const handleSelect = (e) => {
    e.preventDefault()
    e.stopPropagation()
    console.log('SelectItem clicked:', itemValue)
    
    if (onValueChange) {
      console.log('Calling onValueChange with:', itemValue)
      onValueChange(itemValue)
    }
    
    if (setOpen) {
      setTimeout(() => setOpen(false), 100)
    }
  }

  return (
    <div
      className={cn(
        'relative flex cursor-pointer select-none items-center rounded-lg px-3 py-2.5 text-sm outline-none transition-all duration-200 hover:bg-slate-100 focus:bg-slate-100 text-slate-700',
        isSelected && 'bg-blue-50 text-blue-600 font-medium',
        className
      )}
      onClick={handleSelect}
      onMouseDown={(e) => {
        e.preventDefault()
        handleSelect(e)
      }}
      role="option"
      aria-selected={isSelected}
      {...props}
    >
      {children}
    </div>
  )
}

Select.Trigger = SelectTrigger
Select.Content = SelectContent
Select.Item = SelectItem
Select.Value = SelectValue

export { Select, SelectContent, SelectItem, SelectTrigger, SelectValue }


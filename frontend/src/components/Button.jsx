import React from 'react';

const Button = ({ children, variant = 'primary', className = '', ...props }) => {
  const baseStyles = "px-8 py-3 font-xiaowei tracking-widest text-lg transition-all rounded-sm";
  
  const variants = {
    primary: "bg-ink-black text-rice-paper hover:bg-vermilion",
    outline: "border border-ink-black/30 text-ink-black hover:border-ink-black hover:bg-ink-black/5",
    ghost: "text-ink-black hover:text-vermilion"
  };

  return (
    <button 
      className={`${baseStyles} ${variants[variant]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;

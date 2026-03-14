import React from 'react';

const Card = ({ children, className = '', hoverEffect = true }) => {
  return (
    <div 
      className={`bg-white rounded-sm overflow-hidden relative ${hoverEffect ? 'card-shadow hover:-translate-y-1 hover:shadow-xl transition-all duration-300' : 'card-shadow'} ${className}`}
    >
      {children}
    </div>
  );
};

export default Card;

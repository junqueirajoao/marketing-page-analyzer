import React, { useState } from 'react';

interface CollapsibleSectionProps {
  title: string;
  icon?: string;
  defaultExpanded?: boolean;
  children: React.ReactNode;
  badge?: string | number;
  className?: string;
}

export const CollapsibleSection: React.FC<CollapsibleSectionProps> = ({
  title,
  icon,
  defaultExpanded = false,
  children,
  badge,
  className = '',
}) => {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);

  return (
    <div className={`bg-white rounded-xl shadow-md border border-gray-100 ${className}`}>
      {/* Clickable Header */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full p-6 flex items-center justify-between hover:bg-gray-50 transition-colors rounded-t-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-inset"
        aria-expanded={isExpanded}
        aria-label={`${isExpanded ? 'Recolher' : 'Expandir'} seção ${title}`}
      >
        <div className="flex items-center gap-2">
          {icon && <span className="text-2xl">{icon}</span>}
          <h3 className="text-xl font-bold text-gray-900">
            {title}
            {badge !== undefined && (
              <span className="ml-2 text-sm font-normal text-gray-600">
                ({badge})
              </span>
            )}
          </h3>
        </div>
        
        {/* Chevron Icon */}
        <svg
          className={`w-6 h-6 text-gray-600 transition-transform duration-200 ${
            isExpanded ? 'rotate-180' : ''
          }`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>

      {/* Collapsible Content */}
      <div
        className={`overflow-hidden transition-all duration-300 ease-in-out ${
          isExpanded ? 'max-h-[10000px] opacity-100' : 'max-h-0 opacity-0'
        }`}
      >
        <div className="p-6 pt-0 border-t border-gray-100">
          {children}
        </div>
      </div>
    </div>
  );
};

// Made with Bob
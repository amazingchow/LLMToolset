'use client';

import { cn } from '@/lib/utils';

interface ProgressCircleProps {
  percentage: number;
  size?: number;
  strokeWidth?: number;
  className?: string;
  children?: React.ReactNode;
}

export function ProgressCircle({ percentage, size = 120, strokeWidth = 8, className, children }: ProgressCircleProps) {
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;
  const progressColorClass = percentage >= 90 ? 'text-red-500' : 'text-green-500';

  return (
    <div className={cn('relative', className)} style={{ width: size, height: size }}>
      <svg className="progress-ring" width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="currentColor"
          strokeWidth={strokeWidth}
          fill="transparent"
          className="text-gray-200"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="currentColor"
          strokeWidth={strokeWidth}
          fill="transparent"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          className={cn(progressColorClass, 'transition-all duration-300 ease-in-out')}
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center">
        {children || (
          <div className="text-center">
            <div className="text-2xl font-bold text-gray-900">{percentage.toFixed(1)}%</div>
            <div className="text-xs text-gray-500">可用</div>
          </div>
        )}
      </div>
    </div>
  );
}

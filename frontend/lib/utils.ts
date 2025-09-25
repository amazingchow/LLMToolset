import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatMemory(memory: string): { value: number; unit: string } {
  const match = memory.match(/^([\d.]+)\s*(\w+)/);
  if (!match) return { value: 0, unit: 'GB' };

  const value = parseFloat(match[1]);
  const unit = match[2];

  return { value, unit };
}

export function parseMemoryToGB(memory: string): number {
  const { value, unit } = formatMemory(memory);

  switch (unit.toUpperCase()) {
    case 'TB':
      return value * 1024;
    case 'GB':
      return value;
    case 'MB':
      return value / 1024;
    case 'KB':
      return value / (1024 * 1024);
    case 'BYTES':
      return value / (1024 * 1024 * 1024);
    default:
      return value;
  }
}

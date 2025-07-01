import { vi } from 'vitest';

export const useToast = vi.fn(() => ({
  toast: vi.fn(),
  toasts: [],
  dismiss: vi.fn()
}));

export const toast = vi.fn();
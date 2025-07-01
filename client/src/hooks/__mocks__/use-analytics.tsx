import { vi } from 'vitest';

export const useAnalytics = vi.fn(() => ({
  trackEvent: vi.fn(),
  trackTiming: vi.fn(),
  trackException: vi.fn(),
  trackView: vi.fn()
}));
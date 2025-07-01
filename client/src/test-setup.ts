import '@testing-library/jest-dom'
import { vi, afterEach } from 'vitest'

// Dieser Mock hilft React-DOM bei der Prüfung von CSS-Funktionen in JSDOM
;(global as any).CSS = { 
  supports: () => false, 
  escape: (str: string) => str 
};

// Mock für fetch API
global.fetch = vi.fn()

// Mock für localStorage
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
  length: 0,
  key: vi.fn()
} as Storage
global.localStorage = localStorageMock

// Mock für sessionStorage
const sessionStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
  length: 0,
  key: vi.fn()
} as Storage
global.sessionStorage = sessionStorageMock

// Mock für gtag (Google Analytics)
;(global as any).gtag = vi.fn()

// Mock für window.location - KORRIGIERT für Tests
Object.defineProperty(window, 'location', {
  writable: true,
  value: {
    href: 'http://localhost:3000/test?utm_source=google&utm_campaign=test',
    search: '?utm_source=google&utm_campaign=test',
    pathname: '/test',
    origin: 'http://localhost:3000',
    protocol: 'http:',
    host: 'localhost:3000',
    hostname: 'localhost',
    port: '3000'
  }
})

// Mock für window.navigator
Object.defineProperty(window, 'navigator', {
  writable: true,
  value: {
    userAgent: 'Mozilla/5.0 (Test Browser)',
    language: 'de-DE',
    languages: ['de-DE', 'de', 'en'],
    cookieEnabled: true,
    onLine: true
  }
})

// Mock für DOM Animation support
Object.defineProperty(window.document, 'documentElement', {
  writable: true,
  value: {
    style: {
      WebkitAnimation: '',
      animation: '',
      WebkitTransition: '',
      transition: ''
    }
  }
});

// Mock für Animation related properties
(window as any).WebkitAnimation = '';
(window as any).Animation = '';

// Mock für window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(), // deprecated
    removeListener: vi.fn(), // deprecated
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
})

// Mock für IntersectionObserver
global.IntersectionObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}))

// Mock für ResizeObserver
global.ResizeObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}))

// Mock für getComputedStyle
global.getComputedStyle = vi.fn().mockImplementation(() => ({
  getPropertyValue: vi.fn(),
}))

// Mock für console methods
global.console = {
  ...console,
  log: vi.fn(),
  warn: vi.fn(),
  error: vi.fn(),
  info: vi.fn(),
  debug: vi.fn()
}

// Mock für Date.now() - KORRIGIERT für konsistente Tests
const mockDate = new Date('2024-01-01T00:00:00.000Z')
global.Date.now = vi.fn(() => mockDate.getTime())

// Cleanup nach jedem Test
afterEach(() => {
  vi.clearAllMocks()
}) 
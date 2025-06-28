// Q-Money PWA Service Worker v2.0
// Optimiert für Performance, Offline-Funktionalität und Push-Notifications

const CACHE_NAME = 'q-money-v2.0.0';
const DYNAMIC_CACHE = 'q-money-dynamic-v2.0.0';
const API_CACHE = 'q-money-api-v2.0.0';

// Assets die immer gecacht werden sollen (Critical Resources)
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/offline.html',
  '/manifest.json',
  '/src/main.tsx',
  '/src/index.css',
  // Icons
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png',
  // Kritische Fonts
  'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap'
];

// Assets die bei Bedarf gecacht werden
const RUNTIME_CACHE = [
  '/quiz',
  '/vsl',
  '/bridge',
  '/tsl'
];

// API-Endpunkte die gecacht werden sollen
const API_ENDPOINTS = [
  '/api/leads',
  '/api/analytics',
  '/api/quiz/results'
];

// Cache-Strategien
const CACHE_STRATEGIES = {
  // Statische Assets: Cache First
  CACHE_FIRST: 'cache-first',
  // API-Daten: Network First mit Fallback
  NETWORK_FIRST: 'network-first',
  // Bilder und Media: Stale While Revalidate
  STALE_WHILE_REVALIDATE: 'stale-while-revalidate',
  // HTML-Seiten: Network First
  NETWORK_ONLY: 'network-only'
};

// Installation - Cache statische Assets
self.addEventListener('install', (event) => {
  console.log('[SW] Installing Service Worker v2.0.0');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[SW] Caching static assets');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => {
        console.log('[SW] Static assets cached successfully');
        return self.skipWaiting(); // Aktiviere sofort
      })
      .catch((error) => {
        console.error('[SW] Failed to cache static assets:', error);
      })
  );
});

// Aktivierung - Lösche alte Caches
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating Service Worker v2.0.0');
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== CACHE_NAME && 
                cacheName !== DYNAMIC_CACHE && 
                cacheName !== API_CACHE) {
              console.log('[SW] Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('[SW] Service Worker activated and ready');
        return self.clients.claim(); // Übernehme Kontrolle sofort
      })
  );
});

// Fetch - Intelligente Cache-Strategien
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Ignoriere Chrome Extension Requests
  if (url.protocol === 'chrome-extension:') return;
  
  // API-Requests: Network First mit Cache Fallback
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(handleApiRequest(request));
    return;
  }
  
  // HTML-Seiten: Network First mit Offline-Fallback
  if (request.mode === 'navigate') {
    event.respondWith(handleNavigationRequest(request));
    return;
  }
  
  // Statische Assets: Cache First
  if (isStaticAsset(request)) {
    event.respondWith(handleStaticAsset(request));
    return;
  }
  
  // Bilder und Media: Stale While Revalidate
  if (isImageRequest(request)) {
    event.respondWith(handleImageRequest(request));
    return;
  }
  
  // Default: Network First
  event.respondWith(handleDefaultRequest(request));
});

// API-Request Handler
async function handleApiRequest(request) {
  const cache = await caches.open(API_CACHE);
  
  try {
    // Versuche Network First
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      // Cache erfolgreiche Responses
      cache.put(request, networkResponse.clone());
      
      // Analytics für erfolgreiche API-Calls
      trackEvent('api_success', request.url);
    }
    
    return networkResponse;
  } catch (error) {
    console.log('[SW] Network failed for API, trying cache:', request.url);
    
    // Fallback zu Cache
    const cachedResponse = await cache.match(request);
    if (cachedResponse) {
      trackEvent('api_cache_hit', request.url);
      return cachedResponse;
    }
    
    // Offline-Response für kritische APIs
    if (request.url.includes('/api/capture-lead') || 
        request.url.includes('/api/quiz/results')) {
      return new Response(
        JSON.stringify({
          success: false,
          error: 'Offline - Daten werden synchronisiert sobald du wieder online bist',
          offline: true
        }),
        {
          status: 202,
          headers: { 'Content-Type': 'application/json' }
        }
      );
    }
    
    throw error;
  }
}

// Navigation Request Handler (HTML-Seiten)
async function handleNavigationRequest(request) {
  try {
    // Versuche Network First
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      // Cache erfolgreiche Seiten
      const cache = await caches.open(DYNAMIC_CACHE);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.log('[SW] Network failed for navigation, trying cache:', request.url);
    
    // Fallback zu Cache
    const cache = await caches.open(DYNAMIC_CACHE);
    const cachedResponse = await cache.match(request);
    
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Fallback zur Offline-Seite
    return caches.match('/offline.html');
  }
}

// Statische Assets Handler
async function handleStaticAsset(request) {
  const cache = await caches.open(CACHE_NAME);
  const cachedResponse = await cache.match(request);
  
  if (cachedResponse) {
    return cachedResponse;
  }
  
  // Nicht gecacht - hole vom Network und cache
  try {
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch (error) {
    console.error('[SW] Failed to fetch static asset:', request.url);
    throw error;
  }
}

// Bilder Handler
async function handleImageRequest(request) {
  const cache = await caches.open(DYNAMIC_CACHE);
  const cachedResponse = await cache.match(request);
  
  // Stale While Revalidate
  if (cachedResponse) {
    // Gib Cache zurück, aber update im Hintergrund
    fetch(request)
      .then((networkResponse) => {
        if (networkResponse.ok) {
          cache.put(request, networkResponse.clone());
        }
      })
      .catch(() => {
        // Netzwerkfehler ignorieren für Background-Update
      });
    
    return cachedResponse;
  }
  
  // Kein Cache - hole vom Network
  try {
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch (error) {
    // Placeholder-Bild für fehlgeschlagene Bilder
    return new Response(
      '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200"><rect width="200" height="200" fill="#f3f4f6"/><text x="100" y="100" text-anchor="middle" dy=".3em" fill="#9ca3af">Bild nicht verfügbar</text></svg>',
      { headers: { 'Content-Type': 'image/svg+xml' } }
    );
  }
}

// Default Request Handler
async function handleDefaultRequest(request) {
  try {
    return await fetch(request);
  } catch (error) {
    console.log('[SW] Default network request failed:', request.url);
    throw error;
  }
}

// Helper Functions
function isStaticAsset(request) {
  return request.url.includes('/src/') ||
         request.url.includes('.css') ||
         request.url.includes('.js') ||
         request.url.includes('.tsx') ||
         request.url.includes('/icons/') ||
         request.url.includes('fonts.googleapis.com');
}

function isImageRequest(request) {
  return request.destination === 'image' ||
         request.url.includes('.jpg') ||
         request.url.includes('.jpeg') ||
         request.url.includes('.png') ||
         request.url.includes('.gif') ||
         request.url.includes('.webp') ||
         request.url.includes('.svg');
}

// Analytics Tracking
function trackEvent(eventName, eventData) {
  // Sende Analytics-Event an alle Clients
  self.clients.matchAll().then((clients) => {
    clients.forEach((client) => {
      client.postMessage({
        type: 'SW_ANALYTICS',
        event: eventName,
        data: eventData,
        timestamp: Date.now()
      });
    });
  });
}

// Push Notifications
self.addEventListener('push', (event) => {
  console.log('[SW] Push notification received');
  
  const options = {
    body: 'Du hast eine neue Nachricht von Q-Money!',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/badge-72x72.png',
    vibrate: [200, 100, 200],
    data: {
      url: '/',
      timestamp: Date.now()
    },
    actions: [
      {
        action: 'open',
        title: 'Öffnen',
        icon: '/icons/open-action.png'
      },
      {
        action: 'dismiss',
        title: 'Schließen',
        icon: '/icons/close-action.png'
      }
    ],
    requireInteraction: true,
    tag: 'q-money-notification'
  };
  
  if (event.data) {
    const data = event.data.json();
    options.body = data.message || options.body;
    options.data.url = data.url || options.data.url;
  }
  
  event.waitUntil(
    self.registration.showNotification('Q-Money Update', options)
  );
});

// Notification Click Handler
self.addEventListener('notificationclick', (event) => {
  console.log('[SW] Notification clicked');
  
  event.notification.close();
  
  if (event.action === 'dismiss') {
    return;
  }
  
  const url = event.notification.data?.url || '/';
  
  event.waitUntil(
    self.clients.matchAll({ type: 'window' })
      .then((clients) => {
        // Prüfe ob bereits ein Tab offen ist
        for (const client of clients) {
          if (client.url.includes(url) && 'focus' in client) {
            return client.focus();
          }
        }
        
        // Öffne neuen Tab
        if (self.clients.openWindow) {
          return self.clients.openWindow(url);
        }
      })
  );
});

// Background Sync für Offline-Daten
self.addEventListener('sync', (event) => {
  console.log('[SW] Background sync triggered:', event.tag);
  
  if (event.tag === 'offline-leads') {
    event.waitUntil(syncOfflineLeads());
  }
  
  if (event.tag === 'offline-analytics') {
    event.waitUntil(syncOfflineAnalytics());
  }
});

// Sync Offline Leads
async function syncOfflineLeads() {
  try {
    // Hole offline gespeicherte Leads aus IndexedDB
    const offlineLeads = await getOfflineData('leads');
    
    for (const lead of offlineLeads) {
      try {
        const response = await fetch('/api/capture-lead', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(lead.data)
        });
        
        if (response.ok) {
          await removeOfflineData('leads', lead.id);
          console.log('[SW] Offline lead synced successfully');
        }
      } catch (error) {
        console.error('[SW] Failed to sync offline lead:', error);
      }
    }
  } catch (error) {
    console.error('[SW] Background sync failed:', error);
  }
}

// Sync Offline Analytics
async function syncOfflineAnalytics() {
  try {
    const offlineEvents = await getOfflineData('analytics');
    
    for (const event of offlineEvents) {
      try {
        const response = await fetch('/api/analytics', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(event.data)
        });
        
        if (response.ok) {
          await removeOfflineData('analytics', event.id);
          console.log('[SW] Offline analytics synced successfully');
        }
      } catch (error) {
        console.error('[SW] Failed to sync offline analytics:', error);
      }
    }
  } catch (error) {
    console.error('[SW] Analytics sync failed:', error);
  }
}

// IndexedDB Helper Functions (vereinfacht)
async function getOfflineData(type) {
  // In einer echten Implementierung würde hier IndexedDB verwendet
  return [];
}

async function removeOfflineData(type, id) {
  // In einer echten Implementierung würde hier IndexedDB verwendet
  return true;
}

// Performance Monitoring
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'GET_VERSION') {
    event.ports[0].postMessage({ version: CACHE_NAME });
  }
});

console.log('[SW] Q-Money Service Worker v2.0.0 loaded successfully'); 
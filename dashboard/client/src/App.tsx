import { useEffect } from 'react';
import { ApolloProvider } from '@apollo/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { apolloClient } from '@/services/apollo';
import { wsClient } from '@/services/websocket';
import { Dashboard } from '@/components/dashboard';
import { Toaster } from '@/components/ui/toaster';

function App() {
  useEffect(() => {
    // Initialize WebSocket connection
    wsClient.connect().catch(console.error);

    return () => {
      wsClient.disconnect();
    };
  }, []);

  return (
    <ApolloProvider client={apolloClient}>
      <Router>
        <div className="min-h-screen bg-background text-foreground">
          <Routes>
            <Route path="/*" element={<Dashboard />} />
          </Routes>
          <Toaster />
        </div>
      </Router>
    </ApolloProvider>
  );
}

export default App;
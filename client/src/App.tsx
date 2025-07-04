import { Switch, Route } from "wouter";
import { queryClient } from "./lib/queryClient";
import { QueryClientProvider } from "@tanstack/react-query";
import { HelmetProvider } from 'react-helmet-async';
import { Toaster } from "./components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import { useEffect } from "react";
import { initGA, initSessionTracking, trackPageView } from "./lib/analytics";
import { useAnalytics } from "./hooks/use-analytics";
import { AccessibilityProvider, AccessibilityMenu } from "@/components/AccessibilityProvider";
import SEOOptimizer from "@/components/SEOOptimizer";
import Home from "@/pages/Home";
import Quiz from "@/pages/Quiz";
import VSL from "@/pages/VSL";
import Bridge from "@/pages/Bridge";
import TSL from "@/pages/TSL";
import NotFound from "@/pages/not-found";

// Persona Landingpages
import StarterKapital from "@/pages/StarterKapital";
import ElternEinkommen from "@/pages/ElternEinkommen";
import ProjektProfit from "@/pages/ProjektProfit";
import RentenRendite from "@/pages/RentenRendite";
import FeierabendKapital from "@/pages/FeierabendKapital";
import RemoteCashflow from "@/pages/RemoteCashflow";
import Personas from "@/pages/Personas";

function Router() {
  // Track page views when routes change
  useAnalytics();
  
  return (
    <Switch>
      <Route path="/" component={Home} />
      <Route path="/quiz" component={Quiz} />
      <Route path="/vsl/:system?" component={VSL} />
      <Route path="/bridge" component={Bridge} />
      <Route path="/tsl" component={TSL} />
      
      {/* Persona Landingpages */}
      <Route path="/personas" component={Personas} />
      <Route path="/starter-kapital" component={StarterKapital} />
      <Route path="/eltern-einkommen" component={ElternEinkommen} />
      <Route path="/projekt-profit" component={ProjektProfit} />
      <Route path="/renten-rendite" component={RentenRendite} />
      <Route path="/feierabend-kapital" component={FeierabendKapital} />
      <Route path="/remote-cashflow" component={RemoteCashflow} />
      
      <Route component={NotFound} />
    </Switch>
  );
}

function App() {
  // Initialize Google Analytics and Session Tracking when app loads
  useEffect(() => {
    // Initialize session tracking first
    const sessionData = initSessionTracking();
    console.log('Session initialized:', sessionData.sessionId);
    
    // Verify required environment variable is present
    if (!import.meta.env.VITE_GA_MEASUREMENT_ID) {
      console.warn('Missing required Google Analytics key: VITE_GA_MEASUREMENT_ID');
    } else {
      initGA();
    }
    
    // Track initial page view
    const trackInitialPageView = () => {
      trackPageView(window.location.pathname);
    };
    
    // Small delay to ensure GA is loaded
    setTimeout(trackInitialPageView, 1000);
  }, []);

  return (
    <QueryClientProvider client={queryClient}>
      <HelmetProvider>
        <AccessibilityProvider>
          <TooltipProvider>
            <SEOOptimizer />
            <Router />
            <Toaster />
            <AccessibilityMenu />
          </TooltipProvider>
        </AccessibilityProvider>
      </HelmetProvider>
    </QueryClientProvider>
  );
}

export default App;

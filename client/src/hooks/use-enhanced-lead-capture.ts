import { useMutation } from "@tanstack/react-query";
import { apiRequest } from "@/lib/queryClient";
import { trackLeadCapture, trackConversion } from "@/lib/analytics";
import { toast } from "@/hooks/use-toast";

interface LeadData {
  email: string;
  name?: string;
  phone?: string;
  source: string;
  funnel?: string;
  quizAnswers?: Record<string, string>;
  persona?: Record<string, any>;
}

interface EnhancedLeadResponse {
  success: boolean;
  data: {
    lead: any;
    integrations: {
      n8n: boolean;
      instapage?: {
        success: boolean;
        pageUrl?: string;
        pageId?: string;
      };
    };
  };
  message: string;
}

export function useEnhancedLeadCapture() {
  const mutation = useMutation({
    mutationFn: async (leadData: LeadData): Promise<EnhancedLeadResponse> => {
      // Erstelle erweiterte Lead-Daten mit Tracking
      const enhancedLeadData = await trackLeadCapture(leadData);

      // Verwende den erweiterten capture-lead Endpunkt
      const response = await apiRequest('POST', '/api/capture-lead', enhancedLeadData);
      return response.json();
    },
    onSuccess: (data: EnhancedLeadResponse, variables: LeadData) => {
      // Zeige erweiterte Erfolgsmeldung basierend auf Integration-Status
      const integrations = data.data?.integrations;
      let description = "Deine Daten wurden gespeichert. Du erhältst gleich eine E-Mail von uns.";
      
      if (integrations) {
        const integrationStatus = [];
        if (integrations.n8n) integrationStatus.push("n8n Workflow gestartet");
        if (integrations.instapage?.success) integrationStatus.push("Personalisiertes Angebot erstellt");
        
        if (integrationStatus.length > 0) {
          description += ` ${integrationStatus.join(", ")}.`;
        }
      }

      toast({
        title: "Erfolgreich!",
        description,
      });

      // Track conversion event
      trackConversion('lead_capture_success', 1, 'EUR', {
        lead_source: variables.source,
        lead_funnel: variables.funnel,
        has_quiz_answers: !!variables.quizAnswers,
        has_persona: !!variables.persona,
        integrations_used: integrations ? Object.keys(integrations).filter(k => integrations[k]).length : 0
      });
    },
    onError: (error: any) => {
      console.error('Enhanced lead capture failed:', error);
      toast({
        title: "Fehler",
        description: "Beim Speichern deiner Daten ist ein Fehler aufgetreten. Bitte versuche es erneut.",
        variant: "destructive"
      });
    }
  });

  const captureLead = (leadData: LeadData) => {
    // Track form submission
    trackConversion('form_submission', 1, 'EUR', {
      form_type: 'enhanced_lead_capture',
      lead_source: leadData.source,
      lead_funnel: leadData.funnel,
      has_phone: !!leadData.phone,
      has_persona: !!leadData.persona
    });

    mutation.mutate(leadData);
  };

  return {
    captureLead,
    isPending: mutation.isPending,
    isSuccess: mutation.isSuccess,
    isError: mutation.isError,
    data: mutation.data,
    error: mutation.error
  };
}

// Hook für Quiz-spezifische Lead-Capture
export function useQuizLeadCapture() {
  const mutation = useMutation({
    mutationFn: async (data: {
      email: string;
      firstName: string;
      phone?: string;
      answers: Record<string, string>;
      results: any;
    }): Promise<EnhancedLeadResponse> => {
      // Erstelle Persona basierend auf Quiz-Ergebnissen
      const persona = {
        type: data.results.profileText?.split(' - ')[0] || 'Standard',
        preferences: data.answers,
        quizResults: data.results
      };

      // Erstelle erweiterte Lead-Daten mit Tracking
      const enhancedLeadData = await trackLeadCapture({
        email: data.email,
        name: data.firstName,
        phone: data.phone,
        source: 'quiz',
        funnel: data.results?.recommendedFunnel,
        quizAnswers: data.answers,
        persona
      });

      // Verwende den erweiterten capture-lead Endpunkt
      const response = await apiRequest('POST', '/api/capture-lead', enhancedLeadData);
      return response.json();
    },
    onSuccess: (data: EnhancedLeadResponse, variables: any) => {
      // Zeige erweiterte Erfolgsmeldung basierend auf Integration-Status
      const integrations = data.data?.integrations;
      let description = "Deine Daten wurden gespeichert. Du erhältst gleich eine E-Mail von uns.";
      
      if (integrations) {
        const integrationStatus = [];
        if (integrations.n8n) integrationStatus.push("n8n Workflow gestartet");
        if (integrations.instapage?.success) integrationStatus.push("Personalisiertes Angebot erstellt");
        
        if (integrationStatus.length > 0) {
          description += ` ${integrationStatus.join(", ")}.`;
        }
      }

      toast({
        title: "Erfolgreich!",
        description,
      });
      
      // Track enhanced conversion
      trackConversion('quiz_lead_capture_success', 1, 'EUR', {
        lead_source: 'quiz',
        lead_funnel: variables.results?.recommendedFunnel,
        has_quiz_answers: true,
        has_persona: true,
        integrations_used: integrations ? Object.keys(integrations).filter(k => integrations[k]).length : 0,
        persona_type: variables.results.profileText?.split(' - ')[0]
      });
    },
    onError: (error: any) => {
      console.error('Quiz lead capture failed:', error);
      toast({
        title: "Fehler",
        description: "Beim Speichern deiner Daten ist ein Fehler aufgetreten. Bitte versuche es erneut.",
        variant: "destructive"
      });
    }
  });

  const captureQuizLead = (data: {
    email: string;
    firstName: string;
    phone?: string;
    answers: Record<string, string>;
    results: any;
  }) => {
    mutation.mutate(data);
  };

  return {
    captureQuizLead,
    isPending: mutation.isPending,
    isSuccess: mutation.isSuccess,
    isError: mutation.isError,
    data: mutation.data,
    error: mutation.error
  };
} 
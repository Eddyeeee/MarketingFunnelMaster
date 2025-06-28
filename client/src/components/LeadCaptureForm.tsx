import React, { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { useToast } from '../hooks/use-toast';
import { trackLeadCapture } from '../lib/analytics';

interface LeadCaptureFormProps {
  title?: string;
  description?: string;
  placeholder?: string;
  buttonText?: string;
  source?: string;
  funnel?: string;
  className?: string;
  onSuccess?: (data: any) => void;
  showPhone?: boolean;
  showName?: boolean;
  quizAnswers?: Record<string, string>;
  persona?: any;
}

export function LeadCaptureForm({
  title = "Sichere dir jetzt deinen kostenlosen Guide!",
  description = "Erhalte sofort Zugang zu unserem exklusiven Guide und starte noch heute mit deinem ersten Online-Einkommen.",
  placeholder = "Deine E-Mail-Adresse",
  buttonText = "Jetzt kostenlos sichern",
  source = 'capture-lead',
  funnel = 'magic_tool',
  className = "",
  onSuccess,
  showPhone = false,
  showName = false,
  quizAnswers,
  persona
}: LeadCaptureFormProps) {
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!email) {
      toast({
        title: "E-Mail erforderlich",
        description: "Bitte gib deine E-Mail-Adresse ein.",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);

    try {
      // Erstelle Lead-Daten
      const leadData = {
        email,
        name: showName ? name : undefined,
        phone: showPhone ? phone : undefined,
        source,
        funnel,
        quizAnswers,
        persona
      };

      // Sende an Backend
      const response = await fetch('/api/capture-lead', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(leadData),
      });

      const result = await response.json();

      if (result.success) {
        // Track Lead Capture
        await trackLeadCapture({
          email,
          name: showName ? name : undefined,
          source,
          funnel,
          quizAnswers,
          persona
        });

        toast({
          title: "Erfolgreich angemeldet!",
          description: "Du erhältst gleich eine E-Mail von uns mit deinem kostenlosen Guide.",
        });

        // Reset form
        setEmail('');
        setName('');
        setPhone('');

        // Call success callback
        if (onSuccess) {
          onSuccess(result);
        }
      } else {
        throw new Error(result.error || 'Unbekannter Fehler');
      }
    } catch (error) {
      console.error('Lead capture error:', error);
      toast({
        title: "Fehler beim Anmelden",
        description: "Bitte versuche es noch einmal oder kontaktiere uns direkt.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className={`w-full max-w-md mx-auto ${className}`}>
      <CardHeader className="text-center">
        <CardTitle className="text-xl font-bold text-gray-900">
          {title}
        </CardTitle>
        <CardDescription className="text-gray-600">
          {description}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          {showName && (
            <div className="space-y-2">
              <Label htmlFor="name">Name</Label>
              <Input
                id="name"
                type="text"
                placeholder="Dein Name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full"
              />
            </div>
          )}
          
          <div className="space-y-2">
            <Label htmlFor="email">E-Mail</Label>
            <Input
              id="email"
              type="email"
              placeholder={placeholder}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full"
              required
            />
          </div>

          {showPhone && (
            <div className="space-y-2">
              <Label htmlFor="phone">Telefon (optional)</Label>
              <Input
                id="phone"
                type="tel"
                placeholder="Deine Telefonnummer"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                className="w-full"
              />
            </div>
          )}

          <Button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
            disabled={isLoading}
          >
            {isLoading ? (
              <div className="flex items-center space-x-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                <span>Wird verarbeitet...</span>
              </div>
            ) : (
              buttonText
            )}
          </Button>

          <p className="text-xs text-gray-500 text-center">
            Du kannst dich jederzeit wieder abmelden. Wir respektieren deine Privatsphäre.
          </p>
        </form>
      </CardContent>
    </Card>
  );
}

export default LeadCaptureForm;

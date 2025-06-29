import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Mail, Clock, Users, TrendingUp, CheckCircle } from 'lucide-react';

interface EmailPreviewProps {
  persona: {
    type: string;
    profileText: string;
    strategyText: string;
    recommendedFunnel: string;
  };
  leadId?: number;
  className?: string;
}

interface EmailTemplate {
  subject: string;
  body: string;
  delay: number;
}

export function EmailPreview({ persona, leadId, className = "" }: EmailPreviewProps) {
  const [emailFunnel, setEmailFunnel] = useState<any>(null);
  const [emailStats, setEmailStats] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (persona.type) {
      fetchEmailFunnel();
    }
  }, [persona.type]);

  useEffect(() => {
    if (leadId) {
      fetchEmailStats();
    }
  }, [leadId]);

  const fetchEmailFunnel = async () => {
    try {
      setLoading(true);
      const response = await fetch(`/api/email-funnels/persona/${persona.type}`);
      const data = await response.json();
      
      if (data.success) {
        setEmailFunnel(data.funnel);
      }
    } catch (error) {
      console.error('Error fetching email funnel:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchEmailStats = async () => {
    try {
      const response = await fetch(`/api/email-stats/${leadId}`);
      const data = await response.json();
      
      if (data.success) {
        setEmailStats(data.stats);
      }
    } catch (error) {
      console.error('Error fetching email stats:', error);
    }
  };

  const getPersonaIcon = (type: string) => {
    switch (type) {
      case 'student':
        return '🎓';
      case 'employee':
        return '💼';
      case 'parent':
        return '👨‍👩‍👧‍👦';
      default:
        return '👤';
    }
  };

  const getPersonaColor = (type: string) => {
    switch (type) {
      case 'student':
        return 'bg-blue-100 text-blue-800';
      case 'employee':
        return 'bg-green-100 text-green-800';
      case 'parent':
        return 'bg-purple-100 text-purple-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <Card className={`w-full max-w-4xl mx-auto ${className}`}>
        <CardContent className="p-8">
          <div className="flex items-center justify-center space-x-2">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
            <span className="text-gray-600">Lade E-Mail-Funnel...</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={`w-full max-w-4xl mx-auto ${className}`}>
      <CardHeader className="text-center bg-gradient-to-r from-blue-50 to-purple-50">
        <div className="flex justify-center mb-4">
          <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center">
            <Mail className="w-8 h-8 text-white" />
          </div>
        </div>
        <CardTitle className="text-2xl font-bold text-gray-900">
          Dein personalisierter E-Mail-Funnel 📧
        </CardTitle>
        <CardDescription className="text-lg text-gray-600">
          Basierend auf deiner Persona: {persona.profileText}
        </CardDescription>
        <div className="flex justify-center mt-4">
          <Badge className={`${getPersonaColor(persona.type)} text-lg px-4 py-2`}>
            {getPersonaIcon(persona.type)} {persona.type.toUpperCase()}
          </Badge>
        </div>
      </CardHeader>

      <CardContent className="p-8">
        {/* E-Mail-Statistiken */}
        {emailStats && (
          <div className="mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <TrendingUp className="w-5 h-5 mr-2" />
              E-Mail-Performance
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg text-center">
                <div className="text-2xl font-bold text-blue-600">{emailStats.emailsSent}</div>
                <div className="text-sm text-gray-600">E-Mails gesendet</div>
              </div>
              <div className="bg-green-50 p-4 rounded-lg text-center">
                <div className="text-2xl font-bold text-green-600">{emailStats.emailsOpened}</div>
                <div className="text-sm text-gray-600">Geöffnet</div>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg text-center">
                <div className="text-2xl font-bold text-purple-600">{emailStats.emailsClicked}</div>
                <div className="text-sm text-gray-600">Geklickt</div>
              </div>
              <div className="bg-orange-50 p-4 rounded-lg text-center">
                <div className="text-2xl font-bold text-orange-600">
                  {emailStats.emailsOpened > 0 ? Math.round((emailStats.emailsClicked / emailStats.emailsOpened) * 100) : 0}%
                </div>
                <div className="text-sm text-gray-600">Click-Rate</div>
              </div>
            </div>
          </div>
        )}

        {/* E-Mail-Templates */}
        {emailFunnel && (
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <Mail className="w-5 h-5 mr-2" />
              Deine E-Mail-Sequenz
            </h3>
            
            <Tabs defaultValue="0" className="w-full">
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="0">Willkommen</TabsTrigger>
                <TabsTrigger value="1">Follow-up 1</TabsTrigger>
                <TabsTrigger value="2">Follow-up 2</TabsTrigger>
              </TabsList>
              
              {JSON.parse(emailFunnel.emails).map((template: EmailTemplate, index: number) => (
                <TabsContent key={index} value={index.toString()}>
                  <Card>
                    <CardHeader>
                      <div className="flex items-center justify-between">
                        <div>
                          <CardTitle className="text-lg">{template.subject}</CardTitle>
                          <CardDescription className="flex items-center mt-2">
                            <Clock className="w-4 h-4 mr-1" />
                            {template.delay === 0 ? 'Sofort' : `${template.delay} Stunden nach Quiz`}
                          </CardDescription>
                        </div>
                        <Badge variant="outline">
                          {index === 0 ? 'Willkommen' : `Follow-up ${index}`}
                        </Badge>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <div className="whitespace-pre-wrap text-sm text-gray-700 font-mono">
                          {template.body}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </TabsContent>
              ))}
            </Tabs>
          </div>
        )}

        {/* E-Mail-Funnel-Info */}
        <div className="mt-8 bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-lg">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <Users className="w-5 h-5 mr-2" />
            Dein E-Mail-Funnel: {persona.recommendedFunnel}
          </h3>
          <div className="grid md:grid-cols-3 gap-4 text-sm">
            <div className="flex items-center">
              <CheckCircle className="w-4 h-4 text-green-600 mr-2" />
              <span>Personalisiert für {persona.type}</span>
            </div>
            <div className="flex items-center">
              <CheckCircle className="w-4 h-4 text-green-600 mr-2" />
              <span>Automatische Follow-ups</span>
            </div>
            <div className="flex items-center">
              <CheckCircle className="w-4 h-4 text-green-600 mr-2" />
              <span>Optimiert für Conversion</span>
            </div>
          </div>
        </div>

        {/* Call-to-Action */}
        <div className="mt-8 text-center">
          <Button
            onClick={() => window.location.href = '/vsl'}
            size="lg"
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-8 py-3"
          >
            Jetzt zu deiner VSL-Seite
          </Button>
          <p className="text-xs text-gray-500 mt-2">
            Du erhältst automatisch personalisierte E-Mails basierend auf deiner Persona.
          </p>
        </div>
      </CardContent>
    </Card>
  );
}

export default EmailPreview; 
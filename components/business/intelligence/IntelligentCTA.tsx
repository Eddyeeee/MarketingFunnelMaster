/**
 * Intelligent Call-to-Action v2.0
 * Adaptive CTA component based on persona, intent, and device
 * 
 * Module 3B Week 2 - Intelligence Integration
 */

'use client';

import React, { useState, useEffect } from 'react';
import { useComponentIntelligence, usePersonaContent } from '@/hooks/use-intelligence';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { motion } from 'framer-motion';
import { Clock, Users, Shield, Zap, TrendingUp, Award } from 'lucide-react';

interface IntelligentCTAProps {
  primaryAction?: () => void;
  secondaryAction?: () => void;
  productName?: string;
  price?: number;
  originalPrice?: number;
  className?: string;
}

export function IntelligentCTA({
  primaryAction,
  secondaryAction,
  productName = "Smart Solution",
  price = 97,
  originalPrice = 197,
  className = ""
}: IntelligentCTAProps) {
  const {
    optimizations,
    persona,
    device,
    intent,
    confidence,
    shouldUseImmediateResponse
  } = useComponentIntelligence('CallToAction');

  const {
    getPersonaText,
    getPersonaCTA,
    getTrustFactors,
    contentTone
  } = usePersonaContent();

  const [urgencyLevel, setUrgencyLevel] = useState<'low' | 'medium' | 'high'>('medium');
  const [showUrgency, setShowUrgency] = useState(false);
  const [countdown, setCountdown] = useState(0);

  // Set urgency based on intent and persona
  useEffect(() => {
    if (intent === 'purchase') {
      setUrgencyLevel('high');
      setShowUrgency(true);
      setCountdown(15 * 60); // 15 minutes
    } else if (intent === 'decision') {
      setUrgencyLevel('medium');
      setShowUrgency(persona === 'StudentHustler' || persona === 'RemoteDad');
    } else {
      setUrgencyLevel('low');
      setShowUrgency(false);
    }
  }, [intent, persona]);

  // Countdown timer for urgency
  useEffect(() => {
    if (countdown > 0 && showUrgency) {
      const timer = setTimeout(() => setCountdown(countdown - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [countdown, showUrgency]);

  // Generate persona-specific content
  const primaryCTA = getPersonaCTA(urgencyLevel);
  
  const ctaSubtext = getPersonaText({
    TechEarlyAdopter: "Join 50,000+ developers already using this technology",
    RemoteDad: "Join thousands of dads working smarter, not harder",
    StudentHustler: "Join the student success movement",
    BusinessOwner: "Trusted by 1,000+ businesses worldwide",
    fallback: "Join our growing community of users"
  });

  const valueProposition = getPersonaText({
    TechEarlyAdopter: "Get unlimited API access, premium documentation, and priority support",
    RemoteDad: "30-day money-back guarantee • Family-friendly support • Work-life balance guaranteed",
    StudentHustler: "Student pricing • Instant access • Money-back guarantee",
    BusinessOwner: "Enterprise support • SLA guarantee • ROI tracking included",
    fallback: "Risk-free trial • Full feature access • Cancel anytime"
  });

  const urgencyText = getPersonaText({
    TechEarlyAdopter: "Early access pricing ends soon",
    RemoteDad: "Family special offer expires in",
    StudentHustler: "Student discount expires in",
    BusinessOwner: "Enterprise early bird pricing ends in",
    fallback: "Special offer expires in"
  });

  // Get persona-specific icons and colors
  const getPersonaIcon = () => {
    switch (persona) {
      case 'TechEarlyAdopter': return <Zap className="w-5 h-5" />;
      case 'RemoteDad': return <Shield className="w-5 h-5" />;
      case 'StudentHustler': return <TrendingUp className="w-5 h-5" />;
      case 'BusinessOwner': return <Award className="w-5 h-5" />;
      default: return <Users className="w-5 h-5" />;
    }
  };

  const getPersonaColors = () => {
    switch (persona) {
      case 'TechEarlyAdopter': 
        return {
          primary: 'bg-purple-600 hover:bg-purple-700',
          secondary: 'bg-purple-100 text-purple-700 hover:bg-purple-200',
          accent: 'text-purple-600'
        };
      case 'RemoteDad': 
        return {
          primary: 'bg-green-600 hover:bg-green-700',
          secondary: 'bg-green-100 text-green-700 hover:bg-green-200',
          accent: 'text-green-600'
        };
      case 'StudentHustler': 
        return {
          primary: 'bg-orange-600 hover:bg-orange-700',
          secondary: 'bg-orange-100 text-orange-700 hover:bg-orange-200',
          accent: 'text-orange-600'
        };
      case 'BusinessOwner': 
        return {
          primary: 'bg-blue-600 hover:bg-blue-700',
          secondary: 'bg-blue-100 text-blue-700 hover:bg-blue-200',
          accent: 'text-blue-600'
        };
      default: 
        return {
          primary: 'bg-gray-600 hover:bg-gray-700',
          secondary: 'bg-gray-100 text-gray-700 hover:bg-gray-200',
          accent: 'text-gray-600'
        };
    }
  };

  const colors = getPersonaColors();

  // Format countdown time
  const formatTime = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  // Device-specific layout
  const getDeviceLayout = () => {
    if (device === 'mobile') {
      return optimizations.layout.cta_placement === 'sticky' 
        ? 'fixed bottom-0 left-0 right-0 z-50 p-4 bg-white shadow-lg'
        : 'w-full p-4';
    }
    return 'max-w-lg mx-auto p-6';
  };

  return (
    <div className={`${getDeviceLayout()} ${className}`}>
      <Card className="p-6 border-2 border-gray-200 shadow-lg">
        {/* Urgency Banner */}
        {showUrgency && countdown > 0 && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`
              mb-4 p-3 rounded-lg text-center
              ${urgencyLevel === 'high' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'}
            `}
          >
            <div className="flex items-center justify-center gap-2">
              <Clock className="w-4 h-4" />
              <span className="font-semibold">
                {urgencyText} {formatTime(countdown)}
              </span>
            </div>
          </motion.div>
        )}

        {/* Header */}
        <div className="text-center mb-6">
          <div className="flex items-center justify-center mb-2">
            {getPersonaIcon()}
            <h3 className="ml-2 text-xl font-bold">
              Ready to get started with {productName}?
            </h3>
          </div>
          
          <p className="text-gray-600">
            {ctaSubtext}
          </p>
        </div>

        {/* Pricing */}
        <div className="text-center mb-6">
          <div className="flex items-center justify-center gap-2 mb-2">
            {originalPrice && originalPrice > price && (
              <span className="text-lg text-gray-500 line-through">
                €{originalPrice}
              </span>
            )}
            <span className="text-3xl font-bold text-gray-900">
              €{price}
            </span>
            {persona === 'StudentHustler' && (
              <Badge className="bg-orange-100 text-orange-800">
                50% OFF
              </Badge>
            )}
          </div>
          
          {persona === 'BusinessOwner' && (
            <p className="text-sm text-gray-600">
              One-time payment • Enterprise features included
            </p>
          )}
          
          {persona === 'RemoteDad' && (
            <p className="text-sm text-gray-600">
              Family plan • Share with spouse • Kids accounts free
            </p>
          )}
        </div>

        {/* Primary CTA */}
        <motion.div
          whileHover={shouldUseImmediateResponse ? { scale: 1.02 } : undefined}
          whileTap={shouldUseImmediateResponse ? { scale: 0.98 } : undefined}
          className="mb-4"
        >
          <Button
            onClick={primaryAction}
            size={device === 'mobile' ? 'lg' : 'default'}
            className={`
              w-full text-lg font-semibold py-3
              ${colors.primary}
              ${urgencyLevel === 'high' ? 'animate-pulse' : ''}
              ${shouldUseImmediateResponse ? 'transition-all duration-100' : 'transition-all duration-300'}
            `}
          >
            {primaryCTA}
            {urgencyLevel === 'high' && <span className="ml-2">🔥</span>}
          </Button>
        </motion.div>

        {/* Secondary Actions */}
        <div className="space-y-3">
          {persona === 'TechEarlyAdopter' && (
            <Button
              variant="outline"
              onClick={secondaryAction}
              className="w-full"
            >
              View Technical Documentation
            </Button>
          )}
          
          {persona === 'BusinessOwner' && (
            <Button
              variant="outline"
              onClick={secondaryAction}
              className="w-full"
            >
              Schedule Enterprise Demo
            </Button>
          )}
          
          {persona === 'RemoteDad' && (
            <Button
              variant="ghost"
              onClick={secondaryAction}
              className="w-full text-green-600"
            >
              Learn More About Family Benefits
            </Button>
          )}
          
          {persona === 'StudentHustler' && (
            <Button
              variant="ghost"
              onClick={secondaryAction}
              className="w-full text-orange-600"
            >
              See Student Success Stories
            </Button>
          )}
        </div>

        {/* Value Proposition */}
        <div className="mt-6 pt-4 border-t border-gray-200">
          <p className="text-sm text-gray-600 text-center">
            {valueProposition}
          </p>
        </div>

        {/* Trust Indicators */}
        <div className="mt-4 flex justify-center gap-4 text-xs text-gray-500">
          {getTrustFactors().slice(0, 3).map((factor, index) => (
            <span key={index} className="capitalize">
              ✓ {factor.replace('_', ' ')}
            </span>
          ))}
        </div>

        {/* Persona-specific guarantees */}
        {persona === 'RemoteDad' && (
          <div className="mt-4 p-3 bg-green-50 rounded-lg text-center">
            <p className="text-sm text-green-800 font-medium">
              👨‍👩‍👧‍👦 Family-First Guarantee: If this doesn't improve your work-life balance in 30 days, get your money back!
            </p>
          </div>
        )}

        {persona === 'StudentHustler' && (
          <div className="mt-4 p-3 bg-orange-50 rounded-lg text-center">
            <p className="text-sm text-orange-800 font-medium">
              🎓 Student Success Guarantee: Start earning within 7 days or get a full refund!
            </p>
          </div>
        )}

        {persona === 'BusinessOwner' && (
          <div className="mt-4 p-3 bg-blue-50 rounded-lg text-center">
            <p className="text-sm text-blue-800 font-medium">
              📈 ROI Guarantee: See measurable business growth within 90 days or get your investment back!
            </p>
          </div>
        )}

        {/* Debug info for development */}
        {process.env.NODE_ENV === 'development' && confidence > 0 && (
          <div className="mt-4 p-2 bg-gray-100 rounded text-xs">
            Persona: {persona} ({confidence}%) | Intent: {intent} | Device: {device}
          </div>
        )}
      </Card>
    </div>
  );
}

export default IntelligentCTA;
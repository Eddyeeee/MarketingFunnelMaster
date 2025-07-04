/**
 * Intelligent Hero Section v2.0
 * Demonstrates persona-driven component rendering
 * 
 * Module 3B Week 2 - Intelligence Integration
 */

'use client';

import React, { useState, useEffect } from 'react';
import { useComponentIntelligence, usePersonaContent } from '@/hooks/use-intelligence';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { motion, AnimatePresence } from 'framer-motion';

interface IntelligentHeroSectionProps {
  title?: string;
  subtitle?: string;
  productName?: string;
  onCTAClick?: () => void;
  className?: string;
}

export function IntelligentHeroSection({
  title,
  subtitle,
  productName = "Smart Solution",
  onCTAClick,
  className = ""
}: IntelligentHeroSectionProps) {
  const {
    optimizations,
    persona,
    device,
    intent,
    confidence,
    getLayoutClasses,
    getContentClasses,
    getInteractionClasses,
    shouldUseCompactLayout,
    shouldUseDenseContent
  } = useComponentIntelligence('HeroSection');

  const {
    getPersonaText,
    getPersonaCTA,
    getTrustFactors,
    contentTone,
    contentEmphasis
  } = usePersonaContent();

  const [isVisible, setIsVisible] = useState(false);
  const [showPersonaDebug, setShowPersonaDebug] = useState(false);

  useEffect(() => {
    setIsVisible(true);
  }, []);

  // Generate persona-specific content
  const heroTitle = title || getPersonaText({
    TechEarlyAdopter: `Next-Gen ${productName}: Revolutionary Technology at Your Fingertips`,
    RemoteDad: `${productName}: More Time for What Matters Most`,
    StudentHustler: `${productName}: Your Fast Track to Success`,
    BusinessOwner: `${productName}: Scale Your Business Exponentially`,
    fallback: `Transform Your Life with ${productName}`
  });

  const heroSubtitle = subtitle || getPersonaText({
    TechEarlyAdopter: "Advanced algorithms and cutting-edge infrastructure deliver unparalleled performance and scalability.",
    RemoteDad: "Spend less time on tedious tasks and more quality time with your family. Work smarter, not harder.",
    StudentHustler: "Join thousands of students who are already earning while learning. Get results fast.",
    BusinessOwner: "Enterprise-grade solution with proven ROI. Trusted by industry leaders worldwide.",
    fallback: "The smart choice for modern professionals who demand excellence."
  });

  const ctaText = getPersonaCTA(intent === 'decision' || intent === 'purchase' ? 'high' : 'medium');
  const trustFactors = getTrustFactors();

  // Generate layout classes based on optimizations
  const layoutClasses = getLayoutClasses();
  const contentClasses = getContentClasses();
  const interactionClasses = getInteractionClasses();

  // Persona-specific styling
  const getPersonaStyles = () => {
    const baseStyles = "relative overflow-hidden";
    
    switch (persona) {
      case 'TechEarlyAdopter':
        return `${baseStyles} bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white`;
      case 'RemoteDad':
        return `${baseStyles} bg-gradient-to-br from-green-50 via-blue-50 to-green-50 text-gray-800`;
      case 'StudentHustler':
        return `${baseStyles} bg-gradient-to-br from-orange-400 via-pink-400 to-red-400 text-white`;
      case 'BusinessOwner':
        return `${baseStyles} bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900 text-white`;
      default:
        return `${baseStyles} bg-gradient-to-br from-blue-50 via-indigo-50 to-blue-50 text-gray-800`;
    }
  };

  // Device-specific layout
  const getDeviceLayout = () => {
    if (device === 'mobile') {
      return "min-h-screen px-4 py-8 flex flex-col justify-center";
    }
    if (device === 'tablet') {
      return "min-h-[70vh] px-8 py-12 flex items-center";
    }
    return "min-h-[80vh] px-12 py-16 flex items-center";
  };

  // Animation variants based on persona
  const getAnimationVariants = () => {
    const baseVariants = {
      hidden: { opacity: 0, y: 20 },
      visible: { opacity: 1, y: 0 }
    };

    switch (persona) {
      case 'TechEarlyAdopter':
        return {
          hidden: { opacity: 0, scale: 0.9, rotateX: -10 },
          visible: { opacity: 1, scale: 1, rotateX: 0 }
        };
      case 'StudentHustler':
        return {
          hidden: { opacity: 0, x: -100 },
          visible: { opacity: 1, x: 0 }
        };
      default:
        return baseVariants;
    }
  };

  const animationVariants = getAnimationVariants();

  return (
    <section className={`${getPersonaStyles()} ${getDeviceLayout()} ${className}`}>
      <div className={`container mx-auto ${layoutClasses}`}>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12 items-center">
          
          {/* Content Column */}
          <motion.div
            variants={animationVariants}
            initial="hidden"
            animate={isVisible ? "visible" : "hidden"}
            transition={{ duration: 0.6, ease: "easeOut" }}
            className={`space-y-6 ${contentClasses}`}
          >
            {/* Persona Confidence Badge */}
            {confidence > 70 && (
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.3 }}
              >
                <Badge 
                  variant="secondary" 
                  className="mb-4"
                  onClick={() => setShowPersonaDebug(!showPersonaDebug)}
                >
                  Optimized for {persona} ({confidence}% confidence)
                </Badge>
              </motion.div>
            )}

            {/* Title */}
            <motion.h1
              className={`
                text-4xl md:text-5xl lg:text-6xl font-bold 
                ${shouldUseDenseContent ? 'leading-tight' : 'leading-normal'}
                ${contentTone === 'technical' ? 'font-mono' : ''}
              `}
              variants={animationVariants}
              transition={{ delay: 0.1 }}
            >
              {heroTitle}
            </motion.h1>

            {/* Subtitle */}
            <motion.p
              className={`
                text-lg md:text-xl 
                ${shouldUseDenseContent ? 'leading-snug' : 'leading-relaxed'}
                opacity-90
              `}
              variants={animationVariants}
              transition={{ delay: 0.2 }}
            >
              {heroSubtitle}
            </motion.p>

            {/* Trust Factors */}
            {trustFactors.length > 0 && (
              <motion.div
                className="flex flex-wrap gap-2"
                variants={animationVariants}
                transition={{ delay: 0.3 }}
              >
                {trustFactors.slice(0, 3).map((factor, index) => (
                  <Badge key={index} variant="outline" className="capitalize">
                    {factor.replace('_', ' ')}
                  </Badge>
                ))}
              </motion.div>
            )}

            {/* CTA Section */}
            <motion.div
              className={`
                flex flex-col sm:flex-row gap-4 pt-4
                ${interactionClasses}
              `}
              variants={animationVariants}
              transition={{ delay: 0.4 }}
            >
              <Button
                size={device === 'mobile' ? 'lg' : 'default'}
                className={`
                  ${shouldUseCompactLayout ? 'px-6 py-2' : 'px-8 py-3'}
                  ${persona === 'StudentHustler' ? 'animate-pulse' : ''}
                  ${intent === 'purchase' ? 'bg-red-600 hover:bg-red-700' : ''}
                `}
                onClick={onCTAClick}
              >
                {ctaText}
                {intent === 'purchase' && (
                  <span className="ml-2">🔥</span>
                )}
              </Button>

              {persona === 'BusinessOwner' && (
                <Button variant="outline" size={device === 'mobile' ? 'lg' : 'default'}>
                  Schedule Demo
                </Button>
              )}

              {persona === 'TechEarlyAdopter' && (
                <Button variant="ghost" size={device === 'mobile' ? 'lg' : 'default'}>
                  View Documentation →
                </Button>
              )}
            </motion.div>

            {/* Persona-specific additional elements */}
            {persona === 'RemoteDad' && (
              <motion.div
                className="flex items-center gap-2 text-sm opacity-75"
                variants={animationVariants}
                transition={{ delay: 0.5 }}
              >
                <span>👨‍👩‍👧‍👦</span>
                <span>Family-friendly • Work-life balance guaranteed</span>
              </motion.div>
            )}

            {persona === 'StudentHustler' && (
              <motion.div
                className="bg-yellow-400 text-black px-4 py-2 rounded-lg font-semibold"
                variants={animationVariants}
                transition={{ delay: 0.5 }}
              >
                🎓 Student Discount: 50% OFF Limited Time!
              </motion.div>
            )}
          </motion.div>

          {/* Visual Column */}
          <motion.div
            className="relative"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={isVisible ? { opacity: 1, scale: 1 } : { opacity: 0, scale: 0.8 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            {/* Persona-specific visuals */}
            {contentEmphasis === 'visual' && (
              <div className={`
                aspect-square rounded-2xl 
                ${persona === 'TechEarlyAdopter' ? 'bg-gradient-to-br from-purple-400 to-pink-400' : ''}
                ${persona === 'RemoteDad' ? 'bg-gradient-to-br from-green-400 to-blue-400' : ''}
                ${persona === 'StudentHustler' ? 'bg-gradient-to-br from-yellow-400 to-orange-400' : ''}
                ${persona === 'BusinessOwner' ? 'bg-gradient-to-br from-gray-400 to-blue-400' : ''}
                ${persona === 'unknown' ? 'bg-gradient-to-br from-blue-400 to-purple-400' : ''}
                flex items-center justify-center text-6xl font-bold text-white
              `}>
                {persona === 'TechEarlyAdopter' && '🚀'}
                {persona === 'RemoteDad' && '🏠'}
                {persona === 'StudentHustler' && '⚡'}
                {persona === 'BusinessOwner' && '📈'}
                {persona === 'unknown' && '✨'}
              </div>
            )}

            {contentEmphasis === 'interactive' && persona === 'TechEarlyAdopter' && (
              <Card className="p-6 bg-black/20 backdrop-blur border-purple-500">
                <pre className="text-green-400 font-mono text-sm">
                  {`// Initialize Smart Solution
const solution = new SmartSolution({
  performance: "enterprise-grade",
  scalability: "unlimited",
  security: "military-grade"
});

solution.deploy();
// Ready in 3.2 seconds ⚡`}
                </pre>
              </Card>
            )}
          </motion.div>
        </div>

        {/* Debug Panel */}
        <AnimatePresence>
          {showPersonaDebug && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="mt-8 p-4 bg-black/10 rounded-lg backdrop-blur"
            >
              <h3 className="font-semibold mb-2">Intelligence Debug Panel</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div>
                  <strong>Persona:</strong> {persona}
                </div>
                <div>
                  <strong>Confidence:</strong> {confidence}%
                </div>
                <div>
                  <strong>Device:</strong> {device}
                </div>
                <div>
                  <strong>Intent:</strong> {intent}
                </div>
                <div>
                  <strong>Content Tone:</strong> {contentTone}
                </div>
                <div>
                  <strong>Layout:</strong> {optimizations.layout.spacing}
                </div>
                <div>
                  <strong>CTA Style:</strong> {optimizations.layout.cta_placement}
                </div>
                <div>
                  <strong>Trust Factors:</strong> {trustFactors.length}
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </section>
  );
}

export default IntelligentHeroSection;
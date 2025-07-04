'use client';

import { useState, useEffect } from 'react';
import Image from 'next/image';
import { Button } from '@/components/foundation/ui/Button';
import { Card } from '@/components/foundation/ui/Card';
import { useBrand } from '@/hooks/use-brand';
import { usePersona } from '@/hooks/use-persona';
import { useDevice } from '@/hooks/use-device';
import { useAnalytics } from '@/hooks/use-analytics';
import { cn } from '@/lib/utils';
import { ArrowRight, Play, Star, Users, Zap } from 'lucide-react';

interface HeroSectionProps {
  priority?: boolean;
  className?: string;
}

export function HeroSection({ priority = false, className }: HeroSectionProps) {
  const { brandConfig } = useBrand();
  const { persona, personaConfig } = usePersona();
  const { device } = useDevice();
  const { track } = useAnalytics();
  
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setIsVisible(true);
  }, []);

  // Persona-specific content customization
  const getPersonaContent = () => {
    const baseContent = brandConfig.content.messaging;
    
    const personaVariations = {
      TechEarlyAdopter: {
        headline: `${baseContent.headline} with AI`,
        subheadline: 'Advanced algorithms, cutting-edge technology, unparalleled performance',
        features: ['AI-Powered Analytics', 'Advanced APIs', 'Real-time Processing'],
        cta: 'Explore Technology',
        urgency: 'Early Access Available',
      },
      BusinessOwner: {
        headline: `Scale Your Business with ${brandConfig.name}`,
        subheadline: 'Proven strategies, measurable results, sustainable growth',
        features: ['ROI Optimization', 'Enterprise Security', 'Scalable Solutions'],
        cta: 'Schedule Demo',
        urgency: 'Free Consultation',
      },
      StudentHustler: {
        headline: `Start Your Journey with ${brandConfig.name}`,
        subheadline: 'Affordable pricing, quick results, student-friendly',
        features: ['Student Discount', 'Quick Start Guide', 'Community Support'],
        cta: 'Get Started Free',
        urgency: '50% Student Discount',
      },
      RemoteDad: {
        headline: `Work Smarter with ${brandConfig.name}`,
        subheadline: 'Family-friendly, flexible schedule, work-life balance',
        features: ['Family Plans', 'Flexible Scheduling', 'Home Office Ready'],
        cta: 'Start Today',
        urgency: 'Family Package Available',
      },
      unknown: {
        headline: baseContent.headline,
        subheadline: baseContent.value_proposition,
        features: ['Easy to Use', 'Proven Results', 'Great Support'],
        cta: baseContent.cta_primary,
        urgency: 'Limited Time Offer',
      },
    };

    return personaVariations[persona] || personaVariations.unknown;
  };

  const content = getPersonaContent();

  // Device-specific layout optimization
  const getLayoutClasses = () => {
    const baseClasses = 'container mx-auto px-4';
    
    switch (device) {
      case 'mobile':
        return `${baseClasses} text-center space-y-6`;
      case 'tablet':
        return `${baseClasses} text-center space-y-8 max-w-4xl`;
      case 'desktop':
        return `${baseClasses} grid grid-cols-1 lg:grid-cols-2 gap-12 items-center max-w-7xl`;
      default:
        return `${baseClasses} grid grid-cols-1 lg:grid-cols-2 gap-12 items-center max-w-7xl`;
    }
  };

  const handleCTAClick = (action: string) => {
    track({
      name: 'hero_cta_click',
      category: 'conversion',
      action: 'click',
      label: action,
      custom_parameters: {
        persona,
        device,
        content_variant: action,
      },
    });
  };

  const handleVideoPlay = () => {
    track({
      name: 'hero_video_play',
      category: 'engagement',
      action: 'play',
      label: 'hero_video',
    });
  };

  return (
    <section 
      className={cn(
        'relative py-16 lg:py-24 overflow-hidden',
        `persona-${persona}`,
        className
      )}
    >
      {/* Background Elements */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute inset-0 bg-gradient-to-br from-brand-primary/5 to-brand-secondary/5" />
        <div className="absolute top-1/2 left-1/4 w-72 h-72 bg-brand-accent/10 rounded-full blur-3xl transform -translate-y-1/2" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-brand-primary/10 rounded-full blur-3xl" />
      </div>

      <div className={getLayoutClasses()}>
        {/* Content Section */}
        <div 
          className={cn(
            'space-y-6 lg:space-y-8',
            isVisible && 'animate-fade-in',
            device !== 'desktop' && 'order-2'
          )}
        >
          {/* Urgency Badge */}
          {personaConfig.conversion.preferred_cta_style === 'urgent' && (
            <div className="inline-flex items-center px-3 py-1 rounded-full bg-brand-accent/10 text-brand-accent text-sm font-medium">
              <Zap className="w-4 h-4 mr-2" />
              {content.urgency}
            </div>
          )}

          {/* Headline */}
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold tracking-tight">
            <span className="brand-text-gradient">
              {content.headline}
            </span>
          </h1>

          {/* Subheadline */}
          <p className="text-xl md:text-2xl text-muted-foreground max-w-2xl">
            {content.subheadline}
          </p>

          {/* Features */}
          <div className="flex flex-wrap gap-4 lg:gap-6">
            {content.features.map((feature, index) => (
              <div 
                key={index}
                className="flex items-center space-x-2 text-sm md:text-base"
              >
                <div className="w-2 h-2 bg-brand-primary rounded-full" />
                <span className="font-medium">{feature}</span>
              </div>
            ))}
          </div>

          {/* Social Proof */}
          <div className="flex items-center space-x-6 text-sm text-muted-foreground">
            <div className="flex items-center space-x-1">
              <Users className="w-4 h-4" />
              <span>10,000+ users</span>
            </div>
            <div className="flex items-center space-x-1">
              <Star className="w-4 h-4 fill-current text-yellow-500" />
              <span>4.9/5 rating</span>
            </div>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4">
            <Button
              size="lg"
              variant="brand"
              className="group"
              onClick={() => handleCTAClick('primary')}
              analytics={{
                event: 'hero_primary_cta',
                category: 'conversion',
                label: content.cta,
              }}
            >
              {content.cta}
              <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
            </Button>
            
            {device === 'desktop' && (
              <Button
                size="lg"
                variant="outline"
                className="group"
                onClick={handleVideoPlay}
              >
                <Play className="w-4 h-4 mr-2" />
                Watch Demo
              </Button>
            )}
          </div>
        </div>

        {/* Visual Section */}
        <div 
          className={cn(
            'relative',
            isVisible && 'animate-slide-in-right',
            device !== 'desktop' && 'order-1 mb-8'
          )}
        >
          {device === 'mobile' ? (
            // Mobile: Simple illustration or image
            <div className="relative aspect-video rounded-lg overflow-hidden shadow-2xl">
              <Image
                src="/images/hero-mobile.jpg"
                alt={`${brandConfig.name} Preview`}
                fill
                priority={priority}
                className="object-cover"
                sizes="(max-width: 768px) 100vw, 50vw"
              />
            </div>
          ) : (
            // Desktop/Tablet: Interactive demo or dashboard preview
            <Card 
              variant="elevated" 
              className="relative transform hover:scale-105 transition-transform duration-300"
            >
              <div className="aspect-video rounded-lg overflow-hidden">
                <Image
                  src="/images/hero-dashboard.jpg"
                  alt={`${brandConfig.name} Dashboard`}
                  fill
                  priority={priority}
                  className="object-cover"
                  sizes="(max-width: 1024px) 100vw, 50vw"
                />
                
                {/* Interactive Elements Overlay */}
                <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent" />
                
                {/* Floating Stats Cards */}
                {device === 'desktop' && (
                  <>
                    <div className="absolute top-4 right-4 bg-white/90 backdrop-blur-sm rounded-lg p-3 shadow-lg">
                      <div className="text-2xl font-bold text-green-600">+127%</div>
                      <div className="text-xs text-muted-foreground">Growth Rate</div>
                    </div>
                    
                    <div className="absolute bottom-4 left-4 bg-white/90 backdrop-blur-sm rounded-lg p-3 shadow-lg">
                      <div className="text-2xl font-bold text-blue-600">2.3s</div>
                      <div className="text-xs text-muted-foreground">Load Time</div>
                    </div>
                  </>
                )}
              </div>
            </Card>
          )}

          {/* Decorative Elements */}
          {device === 'desktop' && (
            <>
              <div className="absolute -top-4 -right-4 w-24 h-24 bg-brand-accent/20 rounded-full blur-xl" />
              <div className="absolute -bottom-4 -left-4 w-32 h-32 bg-brand-primary/20 rounded-full blur-xl" />
            </>
          )}
        </div>
      </div>

      {/* Trust Indicators */}
      {persona === 'BusinessOwner' && (
        <div className="container mx-auto px-4 mt-16">
          <div className="flex justify-center items-center space-x-8 opacity-60">
            <div className="text-sm font-medium">Trusted by:</div>
            {/* Company logos would go here */}
            <div className="flex space-x-6">
              {['Company A', 'Company B', 'Company C'].map((company) => (
                <div key={company} className="h-8 w-20 bg-muted rounded opacity-50" />
              ))}
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
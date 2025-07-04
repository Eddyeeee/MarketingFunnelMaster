'use client';

import { Button } from '@/components/foundation/ui/Button';
import { Card } from '@/components/foundation/ui/Card';
import { useBrand } from '@/hooks/use-brand';
import { usePersona } from '@/hooks/use-persona';
import { useDevice } from '@/hooks/use-device';
import { useAnalytics } from '@/hooks/use-analytics';
import { cn } from '@/lib/utils';
import { ArrowRight, CheckCircle, Clock, Gift } from 'lucide-react';

interface CallToActionProps {
  variant?: 'primary' | 'secondary' | 'urgent';
  className?: string;
}

export function CallToAction({ variant = 'primary', className }: CallToActionProps) {
  const { brandConfig } = useBrand();
  const { persona, personaConfig } = usePersona();
  const { device } = useDevice();
  const { track } = useAnalytics();

  // Persona-specific CTA content
  const getCTAContent = () => {
    const personaCTAs = {
      TechEarlyAdopter: {
        headline: 'Ready to Build the Future?',
        subheadline: 'Join thousands of developers already using our cutting-edge platform',
        primaryCTA: 'Start Building Now',
        secondaryCTA: 'View Documentation',
        urgency: 'Early access ends soon',
        benefits: ['Full API Access', 'Priority Support', 'Beta Features'],
        icon: ArrowRight,
      },
      BusinessOwner: {
        headline: 'Ready to Scale Your Business?',
        subheadline: 'Get enterprise-grade tools with proven ROI and dedicated support',
        primaryCTA: 'Schedule Demo',
        secondaryCTA: 'View ROI Calculator',
        urgency: 'Free consultation available',
        benefits: ['Dedicated Support', 'Custom Integration', 'Enterprise Security'],
        icon: CheckCircle,
      },
      StudentHustler: {
        headline: 'Ready to Start Your Journey?',
        subheadline: 'Get started with our student-friendly pricing and community support',
        primaryCTA: 'Claim Student Discount',
        secondaryCTA: 'Join Community',
        urgency: '50% discount ends in 48 hours',
        benefits: ['Student Pricing', 'Community Access', 'Quick Start Guide'],
        icon: Gift,
      },
      RemoteDad: {
        headline: 'Ready for Better Work-Life Balance?',
        subheadline: 'Set up in minutes and start generating passive income while with family',
        primaryCTA: 'Start Family Plan',
        secondaryCTA: 'Learn More',
        urgency: 'Family package available',
        benefits: ['Family-Friendly', 'Passive Income', 'Flexible Schedule'],
        icon: CheckCircle,
      },
      unknown: {
        headline: `Ready to Get Started with ${brandConfig.name}?`,
        subheadline: 'Join thousands of satisfied customers and transform your business today',
        primaryCTA: brandConfig.content.messaging.cta_primary,
        secondaryCTA: brandConfig.content.messaging.cta_secondary,
        urgency: 'Limited time offer',
        benefits: ['Easy Setup', 'Great Support', 'Proven Results'],
        icon: ArrowRight,
      },
    };

    return personaCTAs[persona] || personaCTAs.unknown;
  };

  const content = getCTAContent();
  const isUrgent = personaConfig.conversion.preferred_cta_style === 'urgent';

  const handleCTAClick = (type: 'primary' | 'secondary') => {
    track({
      name: 'final_cta_click',
      category: 'conversion',
      action: 'click',
      label: type,
      custom_parameters: {
        persona,
        device,
        cta_variant: variant,
        cta_text: type === 'primary' ? content.primaryCTA : content.secondaryCTA,
      },
    });
  };

  return (
    <section className={cn('container mx-auto px-4', className)}>
      <Card 
        variant="brand" 
        className={cn(
          'relative overflow-hidden',
          isUrgent && 'border-2 border-brand-accent'
        )}
      >
        {/* Background Pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 right-0 w-64 h-64 bg-brand-accent rounded-full transform translate-x-32 -translate-y-32" />
          <div className="absolute bottom-0 left-0 w-96 h-96 bg-brand-primary rounded-full transform -translate-x-48 translate-y-48" />
        </div>

        <div className="relative p-8 lg:p-12">
          <div className={cn(
            'text-center space-y-6',
            device === 'desktop' && 'max-w-4xl mx-auto'
          )}>
            {/* Urgency Badge */}
            {isUrgent && (
              <div className="inline-flex items-center px-4 py-2 rounded-full bg-brand-accent text-white text-sm font-medium">
                <Clock className="w-4 h-4 mr-2" />
                {content.urgency}
              </div>
            )}

            {/* Headlines */}
            <div className="space-y-4">
              <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-white">
                {content.headline}
              </h2>
              <p className="text-xl text-white/80 max-w-2xl mx-auto">
                {content.subheadline}
              </p>
            </div>

            {/* Benefits */}
            <div className="flex flex-wrap justify-center gap-6 lg:gap-8">
              {content.benefits.map((benefit, index) => (
                <div key={index} className="flex items-center space-x-2 text-white/90">
                  <content.icon className="w-5 h-5 text-brand-accent" />
                  <span className="font-medium">{benefit}</span>
                </div>
              ))}
            </div>

            {/* CTA Buttons */}
            <div className={cn(
              'flex gap-4',
              device === 'mobile' ? 'flex-col' : 'flex-col sm:flex-row justify-center'
            )}>
              <Button
                size="xl"
                variant="conversion"
                className="group shadow-2xl"
                onClick={() => handleCTAClick('primary')}
                analytics={{
                  event: 'final_primary_cta',
                  category: 'conversion',
                  label: content.primaryCTA,
                }}
              >
                {content.primaryCTA}
                <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
              </Button>
              
              <Button
                size="xl"
                variant="outline"
                className="bg-white/10 border-white/20 text-white hover:bg-white/20"
                onClick={() => handleCTAClick('secondary')}
              >
                {content.secondaryCTA}
              </Button>
            </div>

            {/* Trust Indicators */}
            <div className="flex justify-center items-center space-x-6 text-sm text-white/70 pt-6">
              <div className="flex items-center space-x-1">
                <CheckCircle className="w-4 h-4 text-green-400" />
                <span>No credit card required</span>
              </div>
              <div className="flex items-center space-x-1">
                <CheckCircle className="w-4 h-4 text-green-400" />
                <span>30-day money back</span>
              </div>
              {device !== 'mobile' && (
                <div className="flex items-center space-x-1">
                  <CheckCircle className="w-4 h-4 text-green-400" />
                  <span>Cancel anytime</span>
                </div>
              )}
            </div>
          </div>
        </div>
      </Card>

      {/* Additional Trust Elements for Business Owners */}
      {persona === 'BusinessOwner' && (
        <div className="mt-8 text-center">
          <p className="text-muted-foreground text-sm">
            Trusted by 500+ businesses worldwide • SOC 2 Compliant • GDPR Ready
          </p>
        </div>
      )}
    </section>
  );
}
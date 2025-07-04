'use client';

import { Card, CardContent } from '@/components/foundation/ui/Card';
import { useBrand } from '@/hooks/use-brand';
import { usePersona } from '@/hooks/use-persona';
import { useDevice } from '@/hooks/use-device';
import { cn } from '@/lib/utils';
import { CheckCircle, Zap, Shield, TrendingUp } from 'lucide-react';

export function ValueProposition() {
  const { brandConfig } = useBrand();
  const { persona } = usePersona();
  const { device } = useDevice();

  // Persona-specific value propositions
  const getValueProps = () => {
    const personaProps = {
      TechEarlyAdopter: [
        {
          icon: Zap,
          title: 'Cutting-Edge Technology',
          description: 'Built with the latest frameworks and AI-powered features',
          highlight: 'Next.js 14 + AI',
        },
        {
          icon: Shield,
          title: 'Enterprise Security',
          description: 'Bank-level security with advanced encryption and compliance',
          highlight: 'SOC 2 Compliant',
        },
        {
          icon: TrendingUp,
          title: 'Performance Optimized',
          description: '95+ Lighthouse scores and sub-2s load times guaranteed',
          highlight: '<2s Load Time',
        },
      ],
      BusinessOwner: [
        {
          icon: TrendingUp,
          title: 'Proven ROI',
          description: 'Average 300% increase in conversion rates within 90 days',
          highlight: '300% ROI',
        },
        {
          icon: Shield,
          title: 'Enterprise Ready',
          description: 'Scales with your business from startup to enterprise',
          highlight: 'Unlimited Scale',
        },
        {
          icon: CheckCircle,
          title: 'Expert Support',
          description: '24/7 dedicated support and strategic consultation',
          highlight: '24/7 Support',
        },
      ],
      StudentHustler: [
        {
          icon: Zap,
          title: 'Quick Setup',
          description: 'Get started in under 5 minutes with our guided setup',
          highlight: '5min Setup',
        },
        {
          icon: TrendingUp,
          title: 'Affordable Pricing',
          description: 'Student discounts and flexible payment plans available',
          highlight: '50% Student Discount',
        },
        {
          icon: CheckCircle,
          title: 'Community Support',
          description: 'Active community of students and young entrepreneurs',
          highlight: '10k+ Students',
        },
      ],
      RemoteDad: [
        {
          icon: CheckCircle,
          title: 'Work-Life Balance',
          description: 'Designed for busy parents with flexible scheduling',
          highlight: 'Family First',
        },
        {
          icon: Shield,
          title: 'Reliable & Stable',
          description: 'Set it up once and it works consistently',
          highlight: '99.9% Uptime',
        },
        {
          icon: TrendingUp,
          title: 'Passive Income',
          description: 'Generate revenue while spending time with family',
          highlight: 'Passive Revenue',
        },
      ],
      unknown: [
        {
          icon: CheckCircle,
          title: 'Easy to Use',
          description: 'Intuitive interface that anyone can master',
          highlight: 'User Friendly',
        },
        {
          icon: TrendingUp,
          title: 'Proven Results',
          description: 'Thousands of successful users worldwide',
          highlight: '10k+ Users',
        },
        {
          icon: Shield,
          title: 'Secure & Reliable',
          description: 'Enterprise-grade security and 99.9% uptime',
          highlight: 'Enterprise Grade',
        },
      ],
    };

    return personaProps[persona] || personaProps.unknown;
  };

  const valueProps = getValueProps();

  return (
    <section className="container mx-auto px-4">
      <div className="text-center space-y-4 mb-12">
        <h2 className="text-3xl md:text-4xl font-bold">
          Why Choose <span className="brand-text-gradient">{brandConfig.name}</span>?
        </h2>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          {brandConfig.content.messaging.value_proposition}
        </p>
      </div>

      <div className={cn(
        'grid gap-6',
        device === 'mobile' ? 'grid-cols-1' : 'grid-cols-1 md:grid-cols-3'
      )}>
        {valueProps.map((prop, index) => (
          <Card 
            key={index} 
            variant="elevated" 
            hover="lift"
            persona={persona}
            device={device}
            className="text-center p-6"
          >
            <CardContent className="space-y-4">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-brand-primary/10">
                <prop.icon className="w-8 h-8 text-brand-primary" />
              </div>
              
              <div className="space-y-2">
                <h3 className="text-xl font-semibold">{prop.title}</h3>
                <p className="text-muted-foreground">{prop.description}</p>
              </div>
              
              <div className="inline-flex items-center px-3 py-1 rounded-full bg-brand-accent/10 text-brand-accent text-sm font-medium">
                {prop.highlight}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  );
}
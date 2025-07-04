import { Metadata } from 'next';
import { Suspense } from 'react';
import { HeroSection } from '@/components/business/marketing/HeroSection';
import { ValueProposition } from '@/components/business/marketing/ValueProposition';
import { SocialProof } from '@/components/business/marketing/SocialProof';
import { CallToAction } from '@/components/business/marketing/CallToAction';
import { PersonaDetector } from '@/components/business/intelligence/PersonaDetector';
import { DeviceOptimizer } from '@/components/business/intelligence/DeviceOptimizer';
import { BehaviorTracker } from '@/components/business/intelligence/BehaviorTracker';
import { HeroSkeleton } from '@/components/foundation/ui/Skeleton';

export const metadata: Metadata = {
  title: 'AI-Powered Marketing Funnel System',
  description: 'Transform your business with intelligent marketing funnels that adapt to your customers in real-time.',
  openGraph: {
    title: 'AI-Powered Marketing Funnel System',
    description: 'Transform your business with intelligent marketing funnels that adapt to your customers in real-time.',
    type: 'website',
    url: 'https://marketingfunnelmaster.com',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'AI-Powered Marketing Funnel System',
    description: 'Transform your business with intelligent marketing funnels that adapt to your customers in real-time.',
  },
  alternates: {
    canonical: 'https://marketingfunnelmaster.com',
  },
};

export default function HomePage() {
  return (
    <>
      {/* Intelligence Components */}
      <PersonaDetector />
      <DeviceOptimizer />
      <BehaviorTracker />

      {/* Main Content */}
      <main className="min-h-screen">
        {/* Hero Section - Above the fold, critical for LCP */}
        <Suspense fallback={<HeroSkeleton />}>
          <HeroSection 
            priority={true}
            className="hero-section"
          />
        </Suspense>

        {/* Value Proposition - Below the fold */}
        <section className="py-16 lg:py-24">
          <ValueProposition />
        </section>

        {/* Social Proof - Progressive enhancement */}
        <section className="py-16 lg:py-24 bg-muted/30">
          <Suspense fallback={<div className="h-64 animate-pulse bg-muted rounded-lg" />}>
            <SocialProof />
          </Suspense>
        </section>

        {/* Call to Action - Conversion critical */}
        <section className="py-16 lg:py-24">
          <CallToAction 
            variant="primary"
            className="conversion-section"
          />
        </section>
      </main>
    </>
  );
}
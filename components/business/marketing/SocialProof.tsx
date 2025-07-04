'use client';

import { Card, CardContent } from '@/components/foundation/ui/Card';
import { useBrand } from '@/hooks/use-brand';
import { usePersona } from '@/hooks/use-persona';
import { useDevice } from '@/hooks/use-device';
import { cn } from '@/lib/utils';
import { Star, Quote } from 'lucide-react';

export function SocialProof() {
  const { brandConfig } = useBrand();
  const { persona } = usePersona();
  const { device } = useDevice();

  // Persona-specific testimonials
  const getTestimonials = () => {
    const personaTestimonials = {
      TechEarlyAdopter: [
        {
          name: 'Alex Chen',
          role: 'Senior Developer at TechCorp',
          avatar: '/images/testimonials/alex.jpg',
          content: 'The API documentation is incredible and the performance optimizations saved us weeks of work.',
          rating: 5,
          highlight: 'API Excellence',
        },
        {
          name: 'Sarah Kumar',
          role: 'CTO at StartupX',
          avatar: '/images/testimonials/sarah.jpg',
          content: 'Best developer experience I\'ve had. The TypeScript integration is flawless.',
          rating: 5,
          highlight: 'Developer Experience',
        },
        {
          name: 'Mike Rodriguez',
          role: 'Full Stack Engineer',
          avatar: '/images/testimonials/mike.jpg',
          content: 'Finally, a platform that understands modern development workflows.',
          rating: 5,
          highlight: 'Modern Workflow',
        },
      ],
      BusinessOwner: [
        {
          name: 'Jennifer Walsh',
          role: 'CEO, GrowthCorp',
          avatar: '/images/testimonials/jennifer.jpg',
          content: 'Increased our conversion rate by 340% in just 2 months. The ROI is incredible.',
          rating: 5,
          highlight: '340% Increase',
        },
        {
          name: 'David Park',
          role: 'VP Marketing, ScaleCo',
          avatar: '/images/testimonials/david.jpg',
          content: 'This platform transformed our entire marketing strategy. Worth every penny.',
          rating: 5,
          highlight: 'Strategy Transformation',
        },
        {
          name: 'Lisa Thompson',
          role: 'Founder, SuccessLab',
          avatar: '/images/testimonials/lisa.jpg',
          content: 'The enterprise features and support team are absolutely outstanding.',
          rating: 5,
          highlight: 'Enterprise Ready',
        },
      ],
      StudentHustler: [
        {
          name: 'Jake Williams',
          role: 'Computer Science Student',
          avatar: '/images/testimonials/jake.jpg',
          content: 'The student discount made this accessible and the community is amazing!',
          rating: 5,
          highlight: 'Student Friendly',
        },
        {
          name: 'Emma Davis',
          role: 'Marketing Student',
          avatar: '/images/testimonials/emma.jpg',
          content: 'Learned more in 2 weeks than in my entire semester. Quick setup was a game-changer.',
          rating: 5,
          highlight: 'Quick Learning',
        },
        {
          name: 'Carlos Mendez',
          role: 'Young Entrepreneur',
          avatar: '/images/testimonials/carlos.jpg',
          content: 'Started making money within the first week. Perfect for side hustles.',
          rating: 5,
          highlight: 'Fast Results',
        },
      ],
      RemoteDad: [
        {
          name: 'Tom Anderson',
          role: 'Remote Worker & Dad of 2',
          avatar: '/images/testimonials/tom.jpg',
          content: 'Finally have time for family dinners again. This runs itself beautifully.',
          rating: 5,
          highlight: 'Work-Life Balance',
        },
        {
          name: 'Mark Johnson',
          role: 'Freelancer & Father',
          avatar: '/images/testimonials/mark.jpg',
          content: 'Set it up during nap time, now it generates passive income while I\'m with the kids.',
          rating: 5,
          highlight: 'Passive Income',
        },
        {
          name: 'Chris Wilson',
          role: 'Remote Consultant & Dad',
          avatar: '/images/testimonials/chris.jpg',
          content: 'The reliability is perfect for busy parents. No constant maintenance needed.',
          rating: 5,
          highlight: 'Set & Forget',
        },
      ],
      unknown: [
        {
          name: 'Alex Johnson',
          role: 'Business Owner',
          avatar: '/images/testimonials/alex-unknown.jpg',
          content: 'Easy to use and delivers real results. Highly recommend!',
          rating: 5,
          highlight: 'Real Results',
        },
        {
          name: 'Sarah Brown',
          role: 'Marketing Manager',
          avatar: '/images/testimonials/sarah-unknown.jpg',
          content: 'Great platform with excellent support. Very satisfied.',
          rating: 5,
          highlight: 'Excellent Support',
        },
        {
          name: 'Mike Davis',
          role: 'Entrepreneur',
          avatar: '/images/testimonials/mike-unknown.jpg',
          content: 'Simple setup and powerful features. Worth the investment.',
          rating: 5,
          highlight: 'Worth It',
        },
      ],
    };

    return personaTestimonials[persona] || personaTestimonials.unknown;
  };

  const testimonials = getTestimonials();

  return (
    <section className="container mx-auto px-4">
      <div className="text-center space-y-4 mb-12">
        <h2 className="text-3xl md:text-4xl font-bold">
          Loved by <span className="brand-text-gradient">Thousands</span>
        </h2>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Join thousands of satisfied customers who have transformed their business with {brandConfig.name}
        </p>
      </div>

      <div className={cn(
        'grid gap-6',
        device === 'mobile' 
          ? 'grid-cols-1' 
          : device === 'tablet' 
          ? 'grid-cols-2' 
          : 'grid-cols-3'
      )}>
        {testimonials.map((testimonial, index) => (
          <Card 
            key={index} 
            variant="elevated" 
            hover="lift"
            persona={persona}
            device={device}
            className="relative"
          >
            <CardContent className="p-6 space-y-4">
              {/* Quote Icon */}
              <div className="absolute top-4 right-4 opacity-10">
                <Quote className="w-8 h-8" />
              </div>

              {/* Rating */}
              <div className="flex items-center space-x-1">
                {[...Array(testimonial.rating)].map((_, i) => (
                  <Star key={i} className="w-4 h-4 fill-current text-yellow-500" />
                ))}
              </div>

              {/* Testimonial Content */}
              <blockquote className="text-muted-foreground italic">
                "{testimonial.content}"
              </blockquote>

              {/* Author Info */}
              <div className="flex items-center space-x-3 pt-4 border-t border-border/50">
                <div className="w-10 h-10 rounded-full bg-muted flex items-center justify-center">
                  <span className="text-sm font-medium">
                    {testimonial.name.split(' ').map(n => n[0]).join('')}
                  </span>
                </div>
                <div className="flex-1">
                  <div className="font-medium text-sm">{testimonial.name}</div>
                  <div className="text-xs text-muted-foreground">{testimonial.role}</div>
                </div>
              </div>

              {/* Highlight Badge */}
              <div className="inline-flex items-center px-2 py-1 rounded-full bg-brand-primary/10 text-brand-primary text-xs font-medium">
                {testimonial.highlight}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Trust Metrics */}
      <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
        <div className="space-y-2">
          <div className="text-3xl font-bold brand-text-gradient">10k+</div>
          <div className="text-sm text-muted-foreground">Happy Customers</div>
        </div>
        <div className="space-y-2">
          <div className="text-3xl font-bold brand-text-gradient">4.9/5</div>
          <div className="text-sm text-muted-foreground">Average Rating</div>
        </div>
        <div className="space-y-2">
          <div className="text-3xl font-bold brand-text-gradient">99.9%</div>
          <div className="text-sm text-muted-foreground">Uptime</div>
        </div>
        <div className="space-y-2">
          <div className="text-3xl font-bold brand-text-gradient">24/7</div>
          <div className="text-sm text-muted-foreground">Support</div>
        </div>
      </div>
    </section>
  );
}
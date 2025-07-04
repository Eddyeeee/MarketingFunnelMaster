'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Button } from '@/components/foundation/ui/Button';
import { Sheet, SheetContent, SheetTrigger } from '@/components/foundation/ui/Sheet';
import { Menu, X } from 'lucide-react';
import { cn } from '@/lib/utils';
import { BrandConfig, PersonaType, DeviceType } from '@/types';

interface NavigationProps {
  variant?: 'default' | 'minimal' | 'sidebar';
  brand: string;
  persona: PersonaType;
  device: DeviceType;
  className?: string;
}

interface NavigationItem {
  href: string;
  label: string;
  icon?: React.ComponentType<{ className?: string }>;
  personaRelevance?: PersonaType[];
  deviceVisibility?: DeviceType[];
}

export function Navigation({
  variant = 'default',
  brand,
  persona,
  device,
  className,
}: NavigationProps) {
  const pathname = usePathname();
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  // Handle scroll effect for navigation background
  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 10);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Define navigation items based on persona and device
  const getNavigationItems = (): NavigationItem[] => {
    const baseItems: NavigationItem[] = [
      { href: '/', label: 'Home' },
      { href: '/features', label: 'Features' },
      { href: '/pricing', label: 'Pricing' },
    ];

    // Add persona-specific navigation items
    const personaItems: Record<PersonaType, NavigationItem[]> = {
      TechEarlyAdopter: [
        { href: '/tech-specs', label: 'Tech Specs' },
        { href: '/api-docs', label: 'API' },
      ],
      RemoteDad: [
        { href: '/work-life-balance', label: 'Work-Life Balance' },
        { href: '/family-friendly', label: 'Family Focus' },
      ],
      StudentHustler: [
        { href: '/student-discounts', label: 'Student Pricing' },
        { href: '/quick-start', label: 'Quick Start' },
      ],
      BusinessOwner: [
        { href: '/enterprise', label: 'Enterprise' },
        { href: '/roi-calculator', label: 'ROI Calculator' },
      ],
      unknown: [],
    };

    return [...baseItems, ...personaItems[persona]];
  };

  const navigationItems = getNavigationItems();

  // Filter items based on device visibility
  const visibleItems = navigationItems.filter(item => {
    if (!item.deviceVisibility) return true;
    return item.deviceVisibility.includes(device);
  });

  const NavContent = () => (
    <>
      <div className="flex items-center space-x-8">
        {visibleItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={cn(
              'text-sm font-medium transition-colors hover:text-primary',
              pathname === item.href 
                ? 'text-primary' 
                : 'text-muted-foreground'
            )}
            onClick={() => setIsOpen(false)}
          >
            {item.label}
          </Link>
        ))}
      </div>

      <div className="flex items-center space-x-4">
        <Button variant="ghost" size="sm" asChild>
          <Link href="/login">Login</Link>
        </Button>
        <Button size="sm" asChild>
          <Link href="/signup">Get Started</Link>
        </Button>
      </div>
    </>
  );

  if (variant === 'minimal') {
    return (
      <nav className={cn('py-4', className)}>
        <div className="container flex items-center justify-between">
          <Link href="/" className="font-bold text-xl">
            Logo
          </Link>
          <Button asChild>
            <Link href="/get-started">Get Started</Link>
          </Button>
        </div>
      </nav>
    );
  }

  return (
    <nav 
      className={cn(
        'sticky top-0 z-50 w-full border-b transition-all duration-200',
        scrolled 
          ? 'bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60' 
          : 'bg-background',
        className
      )}
    >
      <div className="container flex h-16 items-center justify-between">
        {/* Logo */}
        <Link href="/" className="font-bold text-xl">
          <span className="brand-text-gradient">
            {brand === 'tech' && 'TechFlow'}
            {brand === 'wealth' && 'WealthMax'}
            {brand === 'crypto' && 'CryptoFlow'}
            {brand === 'affiliate' && 'AffiliPro'}
          </span>
        </Link>

        {/* Desktop Navigation */}
        <div className="hidden md:flex md:flex-1 md:items-center md:justify-between md:space-x-8 md:ml-8">
          <NavContent />
        </div>

        {/* Mobile Navigation */}
        <div className="md:hidden">
          <Sheet open={isOpen} onOpenChange={setIsOpen}>
            <SheetTrigger asChild>
              <Button variant="ghost" size="sm">
                <Menu className="h-5 w-5" />
                <span className="sr-only">Toggle menu</span>
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="w-80">
              <div className="flex flex-col space-y-6 mt-6">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-lg brand-text-gradient">
                    Menu
                  </span>
                  <Button 
                    variant="ghost" 
                    size="sm"
                    onClick={() => setIsOpen(false)}
                  >
                    <X className="h-5 w-5" />
                  </Button>
                </div>
                
                <div className="flex flex-col space-y-4">
                  {visibleItems.map((item) => (
                    <Link
                      key={item.href}
                      href={item.href}
                      className={cn(
                        'text-sm font-medium py-2 px-3 rounded-md transition-colors',
                        pathname === item.href 
                          ? 'bg-primary text-primary-foreground' 
                          : 'text-muted-foreground hover:text-primary hover:bg-muted'
                      )}
                      onClick={() => setIsOpen(false)}
                    >
                      {item.label}
                    </Link>
                  ))}
                </div>

                <div className="flex flex-col space-y-2 pt-4 border-t">
                  <Button variant="ghost" asChild className="justify-start">
                    <Link href="/login" onClick={() => setIsOpen(false)}>
                      Login
                    </Link>
                  </Button>
                  <Button asChild className="justify-start">
                    <Link href="/signup" onClick={() => setIsOpen(false)}>
                      Get Started
                    </Link>
                  </Button>
                </div>
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </nav>
  );
}
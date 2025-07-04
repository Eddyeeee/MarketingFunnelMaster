'use client';

import { ReactNode } from 'react';
import { Navigation } from './Navigation';
import { Footer } from './Footer';
import { useBrand } from '@/hooks/use-brand';
import { usePersona } from '@/hooks/use-persona';
import { useDevice } from '@/hooks/use-device';
import { cn } from '@/lib/utils';

interface AppShellProps {
  children: ReactNode;
  className?: string;
  showNavigation?: boolean;
  showFooter?: boolean;
  navigationVariant?: 'default' | 'minimal' | 'sidebar';
  footerVariant?: 'default' | 'minimal' | 'extended';
}

export function AppShell({
  children,
  className,
  showNavigation = true,
  showFooter = true,
  navigationVariant = 'default',
  footerVariant = 'default',
}: AppShellProps) {
  const { brand } = useBrand();
  const { persona } = usePersona();
  const { device } = useDevice();

  return (
    <div 
      className={cn(
        'min-h-screen flex flex-col',
        `brand-${brand}`,
        `persona-${persona}`,
        `device-${device}`,
        className
      )}
      data-brand={brand}
      data-persona={persona}
      data-device={device}
    >
      {/* Navigation */}
      {showNavigation && (
        <Navigation 
          variant={navigationVariant}
          brand={brand}
          persona={persona}
          device={device}
        />
      )}

      {/* Main Content Area */}
      <main className="flex-1">
        {children}
      </main>

      {/* Footer */}
      {showFooter && (
        <Footer 
          variant={footerVariant}
          brand={brand}
          persona={persona}
          device={device}
        />
      )}
    </div>
  );
}
'use client';

import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';
import { PersonaType, DeviceType, BrandType } from '@/types';

const cardVariants = cva(
  'rounded-lg border bg-card text-card-foreground shadow-sm transition-all duration-200',
  {
    variants: {
      variant: {
        default: 'border-border',
        elevated: 'shadow-lg hover:shadow-xl',
        outline: 'border-2 border-primary/20 hover:border-primary/40',
        ghost: 'border-transparent bg-transparent shadow-none',
        brand: 'border-brand-primary/20 bg-gradient-to-br from-card to-brand-primary/5',
      },
      size: {
        sm: 'p-4',
        default: 'p-6',
        lg: 'p-8',
        xl: 'p-10',
      },
      hover: {
        none: '',
        lift: 'hover:-translate-y-1 hover:shadow-lg',
        glow: 'hover:shadow-lg hover:shadow-primary/25',
        scale: 'hover:scale-105',
      },
      // Persona-specific styling
      persona: {
        TechEarlyAdopter: 'border-blue-200 dark:border-blue-800',
        RemoteDad: 'border-green-200 dark:border-green-800',
        StudentHustler: 'border-orange-200 dark:border-orange-800',
        BusinessOwner: 'border-purple-200 dark:border-purple-800',
        unknown: '',
      },
      // Device-specific optimizations
      device: {
        mobile: 'touch-manipulation',
        tablet: 'touch-manipulation',
        desktop: 'cursor-pointer',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
      hover: 'none',
      persona: 'unknown',
      device: 'desktop',
    },
  }
);

export interface CardProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof cardVariants> {
  persona?: PersonaType;
  device?: DeviceType;
  brand?: BrandType;
  interactive?: boolean;
  loading?: boolean;
}

const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ 
    className, 
    variant, 
    size, 
    hover, 
    persona = 'unknown',
    device = 'desktop',
    interactive = false,
    loading = false,
    children,
    ...props 
  }, ref) => {
    const cardHover = interactive ? (hover || 'lift') : 'none';

    return (
      <div
        ref={ref}
        className={cn(
          cardVariants({ variant, size, hover: cardHover, persona, device }),
          loading && 'animate-pulse',
          interactive && 'transition-transform duration-200',
          className
        )}
        {...props}
      >
        {loading ? (
          <div className="space-y-3">
            <div className="h-4 bg-muted rounded animate-pulse" />
            <div className="h-4 bg-muted rounded animate-pulse w-3/4" />
            <div className="h-4 bg-muted rounded animate-pulse w-1/2" />
          </div>
        ) : (
          children
        )}
      </div>
    );
  }
);

Card.displayName = 'Card';

const CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn('flex flex-col space-y-1.5 p-6', className)}
    {...props}
  />
));
CardHeader.displayName = 'CardHeader';

const CardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, children, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn(
      'text-2xl font-semibold leading-none tracking-tight',
      className
    )}
    {...props}
  >
    {children}
  </h3>
));
CardTitle.displayName = 'CardTitle';

const CardDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn('text-sm text-muted-foreground', className)}
    {...props}
  />
));
CardDescription.displayName = 'CardDescription';

const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn('p-6 pt-0', className)} {...props} />
));
CardContent.displayName = 'CardContent';

const CardFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn('flex items-center p-6 pt-0', className)}
    {...props}
  />
));
CardFooter.displayName = 'CardFooter';

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent };
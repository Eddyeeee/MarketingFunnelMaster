'use client';

import * as React from 'react';
import { Slot } from '@radix-ui/react-slot';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';
import { useAnalytics } from '@/hooks/use-analytics';

const buttonVariants = cva(
  'inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
        secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'text-primary underline-offset-4 hover:underline',
        // Brand-specific variants
        brand: 'brand-gradient text-white hover:opacity-90 shadow-lg',
        conversion: 'bg-green-600 text-white hover:bg-green-700 shadow-lg pulse-gentle',
        // Persona-specific variants
        tech: 'bg-blue-600 text-white hover:bg-blue-700 border border-blue-500/20',
        wealth: 'bg-yellow-600 text-white hover:bg-yellow-700 border border-yellow-500/20',
        crypto: 'bg-purple-600 text-white hover:bg-purple-700 border border-purple-500/20',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 rounded-md px-3',
        lg: 'h-11 rounded-md px-8',
        xl: 'h-12 rounded-lg px-10 text-base',
        icon: 'h-10 w-10',
      },
      loading: {
        true: 'cursor-not-allowed',
        false: '',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
      loading: false,
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
  loading?: boolean;
  loadingText?: string;
  analytics?: {
    event?: string;
    category?: string;
    label?: string;
  };
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ 
    className, 
    variant, 
    size, 
    asChild = false, 
    loading = false,
    loadingText = 'Loading...',
    analytics,
    children,
    onClick,
    ...props 
  }, ref) => {
    const { track } = useAnalytics();
    const Comp = asChild ? Slot : 'button';

    const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
      // Track analytics if provided
      if (analytics) {
        track({
          name: analytics.event || 'button_click',
          category: analytics.category || 'interaction',
          action: 'click',
          label: analytics.label || String(children),
        });
      }

      // Call original onClick handler
      onClick?.(event);
    };

    return (
      <Comp
        className={cn(buttonVariants({ variant, size, loading, className }))}
        ref={ref}
        onClick={handleClick}
        disabled={loading || props.disabled}
        {...props}
      >
        {loading && (
          <div className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
        )}
        {loading ? loadingText : children}
      </Comp>
    );
  }
);

Button.displayName = 'Button';

export { Button, buttonVariants };
'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';

function Skeleton({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn('animate-pulse rounded-md bg-muted', className)}
      {...props}
    />
  );
}

// Specific skeleton components for different sections
function HeroSkeleton({ className }: { className?: string }) {
  return (
    <div className={cn('hero-section py-16 lg:py-24', className)}>
      <div className="container">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Text Content Skeleton */}
          <div className="space-y-6">
            <Skeleton className="h-8 w-3/4" />
            <Skeleton className="h-12 w-full" />
            <Skeleton className="h-6 w-5/6" />
            <Skeleton className="h-6 w-4/6" />
            <div className="flex space-x-4 pt-4">
              <Skeleton className="h-12 w-32" />
              <Skeleton className="h-12 w-24" />
            </div>
          </div>
          
          {/* Image Skeleton */}
          <div className="relative">
            <Skeleton className="aspect-video w-full rounded-lg" />
          </div>
        </div>
      </div>
    </div>
  );
}

function CardSkeleton({ className }: { className?: string }) {
  return (
    <div className={cn('rounded-lg border bg-card p-6', className)}>
      <div className="space-y-4">
        <Skeleton className="h-6 w-3/4" />
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-5/6" />
        <Skeleton className="h-4 w-4/6" />
        <div className="pt-4">
          <Skeleton className="h-10 w-24" />
        </div>
      </div>
    </div>
  );
}

function NavigationSkeleton({ className }: { className?: string }) {
  return (
    <nav className={cn('border-b py-4', className)}>
      <div className="container flex items-center justify-between">
        <Skeleton className="h-8 w-32" />
        <div className="hidden md:flex space-x-6">
          <Skeleton className="h-6 w-16" />
          <Skeleton className="h-6 w-20" />
          <Skeleton className="h-6 w-18" />
          <Skeleton className="h-6 w-14" />
        </div>
        <div className="flex space-x-2">
          <Skeleton className="h-9 w-16" />
          <Skeleton className="h-9 w-20" />
        </div>
      </div>
    </nav>
  );
}

function FooterSkeleton({ className }: { className?: string }) {
  return (
    <footer className={cn('border-t bg-muted/30 py-12', className)}>
      <div className="container">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="space-y-4">
            <Skeleton className="h-6 w-24" />
            <Skeleton className="h-4 w-32" />
            <div className="flex space-x-2">
              <Skeleton className="h-5 w-5 rounded" />
              <Skeleton className="h-5 w-5 rounded" />
              <Skeleton className="h-5 w-5 rounded" />
            </div>
          </div>
          {[...Array(3)].map((_, i) => (
            <div key={i} className="space-y-4">
              <Skeleton className="h-5 w-20" />
              <div className="space-y-2">
                <Skeleton className="h-4 w-16" />
                <Skeleton className="h-4 w-20" />
                <Skeleton className="h-4 w-18" />
                <Skeleton className="h-4 w-14" />
              </div>
            </div>
          ))}
        </div>
      </div>
    </footer>
  );
}

function FormSkeleton({ className }: { className?: string }) {
  return (
    <div className={cn('space-y-6', className)}>
      <div className="space-y-2">
        <Skeleton className="h-4 w-20" />
        <Skeleton className="h-10 w-full" />
      </div>
      <div className="space-y-2">
        <Skeleton className="h-4 w-16" />
        <Skeleton className="h-10 w-full" />
      </div>
      <div className="space-y-2">
        <Skeleton className="h-4 w-24" />
        <Skeleton className="h-24 w-full" />
      </div>
      <Skeleton className="h-10 w-full" />
    </div>
  );
}

function TestimonialSkeleton({ className }: { className?: string }) {
  return (
    <div className={cn('rounded-lg border bg-card p-6', className)}>
      <div className="space-y-4">
        <div className="flex items-start space-x-4">
          <Skeleton className="h-12 w-12 rounded-full" />
          <div className="space-y-2 flex-1">
            <Skeleton className="h-4 w-24" />
            <Skeleton className="h-3 w-32" />
          </div>
        </div>
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-5/6" />
        <Skeleton className="h-4 w-3/4" />
        <div className="flex space-x-1 pt-2">
          {[...Array(5)].map((_, i) => (
            <Skeleton key={i} className="h-4 w-4" />
          ))}
        </div>
      </div>
    </div>
  );
}

function TableSkeleton({ className }: { className?: string }) {
  return (
    <div className={cn('rounded-lg border', className)}>
      <div className="border-b p-4">
        <div className="grid grid-cols-4 gap-4">
          <Skeleton className="h-4 w-16" />
          <Skeleton className="h-4 w-20" />
          <Skeleton className="h-4 w-18" />
          <Skeleton className="h-4 w-14" />
        </div>
      </div>
      {[...Array(5)].map((_, i) => (
        <div key={i} className="border-b p-4 last:border-b-0">
          <div className="grid grid-cols-4 gap-4">
            <Skeleton className="h-4 w-24" />
            <Skeleton className="h-4 w-32" />
            <Skeleton className="h-4 w-20" />
            <Skeleton className="h-4 w-16" />
          </div>
        </div>
      ))}
    </div>
  );
}

export { 
  Skeleton,
  HeroSkeleton,
  CardSkeleton,
  NavigationSkeleton,
  FooterSkeleton,
  FormSkeleton,
  TestimonialSkeleton,
  TableSkeleton,
};
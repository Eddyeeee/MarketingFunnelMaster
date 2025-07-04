'use client';

import { ReactNode } from 'react';
import { BrandContext, useBrandInternal } from '@/hooks/use-brand';

interface BrandProviderProps {
  children: ReactNode;
}

export function BrandProvider({ children }: BrandProviderProps) {
  const brandValue = useBrandInternal();

  return (
    <BrandContext.Provider value={brandValue}>
      {children}
    </BrandContext.Provider>
  );
}
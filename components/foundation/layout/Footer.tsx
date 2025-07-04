'use client';

import Link from 'next/link';
import { BrandConfig, PersonaType, DeviceType } from '@/types';
import { cn } from '@/lib/utils';

interface FooterProps {
  variant?: 'default' | 'minimal' | 'extended';
  brand: string;
  persona: PersonaType;
  device: DeviceType;
  className?: string;
}

interface FooterSection {
  title: string;
  links: Array<{
    href: string;
    label: string;
    external?: boolean;
  }>;
  personaRelevance?: PersonaType[];
}

export function Footer({
  variant = 'default',
  brand,
  persona,
  device,
  className,
}: FooterProps) {
  
  // Define footer sections based on persona
  const getFooterSections = (): FooterSection[] => {
    const baseSections: FooterSection[] = [
      {
        title: 'Product',
        links: [
          { href: '/features', label: 'Features' },
          { href: '/pricing', label: 'Pricing' },
          { href: '/integrations', label: 'Integrations' },
          { href: '/updates', label: 'Updates' },
        ],
      },
      {
        title: 'Resources',
        links: [
          { href: '/docs', label: 'Documentation' },
          { href: '/guides', label: 'Guides' },
          { href: '/blog', label: 'Blog' },
          { href: '/support', label: 'Support' },
        ],
      },
      {
        title: 'Company',
        links: [
          { href: '/about', label: 'About' },
          { href: '/careers', label: 'Careers' },
          { href: '/contact', label: 'Contact' },
          { href: '/press', label: 'Press' },
        ],
      },
    ];

    // Add persona-specific sections
    const personaSections: Record<PersonaType, FooterSection[]> = {
      TechEarlyAdopter: [
        {
          title: 'Developer',
          links: [
            { href: '/api', label: 'API Reference' },
            { href: '/sdk', label: 'SDK' },
            { href: '/webhooks', label: 'Webhooks' },
            { href: '/github', label: 'GitHub', external: true },
          ],
        },
      ],
      BusinessOwner: [
        {
          title: 'Enterprise',
          links: [
            { href: '/enterprise', label: 'Enterprise' },
            { href: '/security', label: 'Security' },
            { href: '/compliance', label: 'Compliance' },
            { href: '/roi', label: 'ROI Calculator' },
          ],
        },
      ],
      StudentHustler: [
        {
          title: 'Student',
          links: [
            { href: '/student-discount', label: 'Student Discount' },
            { href: '/learn', label: 'Learning Center' },
            { href: '/community', label: 'Community' },
            { href: '/jobs', label: 'Job Board' },
          ],
        },
      ],
      RemoteDad: [
        {
          title: 'Work-Life',
          links: [
            { href: '/remote-work', label: 'Remote Work' },
            { href: '/family-plans', label: 'Family Plans' },
            { href: '/time-management', label: 'Time Management' },
            { href: '/wellness', label: 'Wellness' },
          ],
        },
      ],
      unknown: [],
    };

    return [...baseSections, ...personaSections[persona]];
  };

  const footerSections = getFooterSections();

  // Brand-specific social links and information
  const getBrandInfo = () => {
    const brandInfo = {
      tech: {
        name: 'TechFlow',
        tagline: 'Accelerate Your Technical Journey',
        social: {
          twitter: '@techflow',
          github: 'techflow',
          linkedin: 'techflow',
        },
      },
      wealth: {
        name: 'WealthMax',
        tagline: 'Maximize Your Financial Potential',
        social: {
          twitter: '@wealthmax',
          linkedin: 'wealthmax',
          youtube: 'wealthmax',
        },
      },
      crypto: {
        name: 'CryptoFlow',
        tagline: 'Navigate the Crypto Revolution',
        social: {
          twitter: '@cryptoflow',
          discord: 'cryptoflow',
          telegram: 'cryptoflow',
        },
      },
      affiliate: {
        name: 'AffiliPro',
        tagline: 'Professional Affiliate Marketing',
        social: {
          twitter: '@affilipro',
          linkedin: 'affilipro',
          facebook: 'affilipro',
        },
      },
    };

    return brandInfo[brand as keyof typeof brandInfo] || brandInfo.tech;
  };

  const brandInfo = getBrandInfo();

  if (variant === 'minimal') {
    return (
      <footer className={cn('border-t py-6', className)}>
        <div className="container flex flex-col items-center justify-between space-y-4 sm:flex-row sm:space-y-0">
          <div className="text-center sm:text-left">
            <p className="text-sm text-muted-foreground">
              © 2024 {brandInfo.name}. All rights reserved.
            </p>
          </div>
          <div className="flex space-x-4">
            <Link href="/privacy" className="text-sm text-muted-foreground hover:text-primary">
              Privacy
            </Link>
            <Link href="/terms" className="text-sm text-muted-foreground hover:text-primary">
              Terms
            </Link>
          </div>
        </div>
      </footer>
    );
  }

  return (
    <footer className={cn('border-t bg-muted/30', className)}>
      <div className="container py-12 lg:py-16">
        <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
          {/* Brand Section */}
          <div className="space-y-4">
            <div>
              <h3 className="font-bold text-lg brand-text-gradient">
                {brandInfo.name}
              </h3>
              <p className="text-sm text-muted-foreground mt-2">
                {brandInfo.tagline}
              </p>
            </div>
            
            {/* Social Links */}
            <div className="flex space-x-4">
              {Object.entries(brandInfo.social).map(([platform, handle]) => (
                <Link
                  key={platform}
                  href={`https://${platform}.com/${handle}`}
                  className="text-muted-foreground hover:text-primary transition-colors"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <span className="sr-only">{platform}</span>
                  {/* Add social icons here */}
                  <div className="w-5 h-5 bg-current rounded opacity-60 hover:opacity-100" />
                </Link>
              ))}
            </div>
          </div>

          {/* Footer Sections */}
          {footerSections.map((section) => (
            <div key={section.title} className="space-y-4">
              <h4 className="font-semibold text-sm uppercase tracking-wider">
                {section.title}
              </h4>
              <ul className="space-y-2">
                {section.links.map((link) => (
                  <li key={link.href}>
                    <Link
                      href={link.href}
                      className="text-sm text-muted-foreground hover:text-primary transition-colors"
                      target={link.external ? '_blank' : undefined}
                      rel={link.external ? 'noopener noreferrer' : undefined}
                    >
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Bottom Section */}
        <div className="mt-12 pt-8 border-t border-border/50">
          <div className="flex flex-col items-center justify-between space-y-4 sm:flex-row sm:space-y-0">
            <div className="text-sm text-muted-foreground">
              © 2024 {brandInfo.name}. All rights reserved.
            </div>
            
            <div className="flex flex-wrap items-center space-x-6 text-sm">
              <Link href="/privacy" className="text-muted-foreground hover:text-primary">
                Privacy Policy
              </Link>
              <Link href="/terms" className="text-muted-foreground hover:text-primary">
                Terms of Service
              </Link>
              <Link href="/cookies" className="text-muted-foreground hover:text-primary">
                Cookie Policy
              </Link>
              {persona === 'BusinessOwner' && (
                <Link href="/compliance" className="text-muted-foreground hover:text-primary">
                  Compliance
                </Link>
              )}
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
/**
 * Intelligent Navigation v2.0
 * Adaptive navigation component based on persona, device, and context
 * 
 * Module 3B Week 2 - Intelligence Integration
 */

'use client';

import React, { useState, useEffect } from 'react';
import { useComponentIntelligence, usePersonaContent } from '@/hooks/use-intelligence';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Sheet, SheetContent, SheetTrigger, SheetHeader, SheetTitle } from '@/components/ui/sheet';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Menu, 
  Home, 
  BookOpen, 
  Users, 
  Zap, 
  Shield, 
  TrendingUp, 
  Building,
  Code,
  DollarSign,
  FileText,
  Phone,
  Settings
} from 'lucide-react';

interface NavigationItem {
  label: string;
  href: string;
  icon: React.ReactNode;
  priority: 'high' | 'medium' | 'low';
  personas: string[];
  showBadge?: boolean;
  badgeText?: string;
}

interface IntelligentNavigationProps {
  brandName?: string;
  className?: string;
  onItemClick?: (href: string) => void;
}

export function IntelligentNavigation({
  brandName = "SmartSolution",
  className = "",
  onItemClick
}: IntelligentNavigationProps) {
  const {
    optimizations,
    persona,
    device,
    intent,
    confidence,
    shouldUseCompactLayout
  } = useComponentIntelligence('Navigation');

  const {
    getPersonaText,
    getPersonaCTA,
    contentTone
  } = usePersonaContent();

  const [isOpen, setIsOpen] = useState(false);
  const [activeItem, setActiveItem] = useState('/');

  // Define navigation items with persona targeting
  const allNavigationItems: NavigationItem[] = [
    {
      label: 'Home',
      href: '/',
      icon: <Home className="w-4 h-4" />,
      priority: 'high',
      personas: ['all']
    },
    {
      label: getPersonaText({
        TechEarlyAdopter: 'API Docs',
        RemoteDad: 'How It Works',
        StudentHustler: 'Quick Start',
        BusinessOwner: 'Features',
        fallback: 'Features'
      }),
      href: '/features',
      icon: persona === 'TechEarlyAdopter' ? <Code className="w-4 h-4" /> : <BookOpen className="w-4 h-4" />,
      priority: 'high',
      personas: ['all']
    },
    {
      label: 'Pricing',
      href: '/pricing',
      icon: <DollarSign className="w-4 h-4" />,
      priority: 'high',
      personas: ['all'],
      showBadge: persona === 'StudentHustler',
      badgeText: '50% OFF'
    },
    {
      label: getPersonaText({
        TechEarlyAdopter: 'Case Studies',
        RemoteDad: 'Success Stories',
        StudentHustler: 'Student Wins',
        BusinessOwner: 'ROI Reports',
        fallback: 'Success Stories'
      }),
      href: '/testimonials',
      icon: <Users className="w-4 h-4" />,
      priority: 'medium',
      personas: ['RemoteDad', 'StudentHustler', 'BusinessOwner']
    },
    {
      label: 'Technical Specs',
      href: '/technical',
      icon: <Zap className="w-4 h-4" />,
      priority: 'high',
      personas: ['TechEarlyAdopter'],
      showBadge: true,
      badgeText: 'NEW'
    },
    {
      label: 'Enterprise',
      href: '/enterprise',
      icon: <Building className="w-4 h-4" />,
      priority: 'high',
      personas: ['BusinessOwner']
    },
    {
      label: 'Student Hub',
      href: '/students',
      icon: <TrendingUp className="w-4 h-4" />,
      priority: 'high',
      personas: ['StudentHustler'],
      showBadge: true,
      badgeText: 'HOT'
    },
    {
      label: 'Family Plan',
      href: '/family',
      icon: <Shield className="w-4 h-4" />,
      priority: 'high',
      personas: ['RemoteDad']
    },
    {
      label: 'Blog',
      href: '/blog',
      icon: <FileText className="w-4 h-4" />,
      priority: 'low',
      personas: ['TechEarlyAdopter', 'BusinessOwner']
    },
    {
      label: getPersonaText({
        TechEarlyAdopter: 'Support',
        RemoteDad: 'Help Center',
        StudentHustler: 'Get Help',
        BusinessOwner: 'Contact',
        fallback: 'Support'
      }),
      href: '/support',
      icon: <Phone className="w-4 h-4" />,
      priority: 'medium',
      personas: ['all']
    }
  ];

  // Filter navigation items based on persona and priority
  const getFilteredNavItems = (): NavigationItem[] => {
    let items = allNavigationItems.filter(item => 
      item.personas.includes('all') || 
      item.personas.includes(persona) ||
      (confidence < 50 && item.priority === 'high') // Show high priority items for unknown personas
    );

    // Limit items based on device and layout
    if (device === 'mobile' && shouldUseCompactLayout) {
      items = items.filter(item => item.priority === 'high');
    } else if (device === 'tablet') {
      items = items.filter(item => item.priority !== 'low');
    }

    return items.sort((a, b) => {
      const priorityOrder = { high: 3, medium: 2, low: 1 };
      return priorityOrder[b.priority] - priorityOrder[a.priority];
    });
  };

  const filteredNavItems = getFilteredNavItems();

  // Get persona-specific CTA
  const navCTA = getPersonaCTA(intent === 'decision' || intent === 'purchase' ? 'high' : 'medium');

  // Handle navigation item click
  const handleItemClick = (href: string) => {
    setActiveItem(href);
    setIsOpen(false);
    onItemClick?.(href);
  };

  // Get persona-specific brand styling
  const getBrandStyling = () => {
    switch (persona) {
      case 'TechEarlyAdopter':
        return 'text-purple-600 font-mono';
      case 'RemoteDad':
        return 'text-green-600 font-semibold';
      case 'StudentHustler':
        return 'text-orange-600 font-bold';
      case 'BusinessOwner':
        return 'text-blue-600 font-medium';
      default:
        return 'text-gray-800 font-semibold';
    }
  };

  // Navigation layout based on device and optimization
  if (device === 'mobile' || optimizations.layout.navigation === 'hamburger') {
    return (
      <nav className={`border-b bg-white/95 backdrop-blur-sm sticky top-0 z-50 ${className}`}>
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            {/* Brand */}
            <div className={`text-xl ${getBrandStyling()}`}>
              {brandName}
              {confidence > 70 && (
                <Badge variant="secondary" className="ml-2 text-xs">
                  for {persona}
                </Badge>
              )}
            </div>

            {/* Mobile Menu */}
            <div className="flex items-center gap-2">
              {/* Quick CTA for high intent */}
              {(intent === 'decision' || intent === 'purchase') && (
                <Button size="sm" className="text-xs">
                  {navCTA}
                </Button>
              )}
              
              <Sheet open={isOpen} onOpenChange={setIsOpen}>
                <SheetTrigger asChild>
                  <Button variant="ghost" size="icon">
                    <Menu className="w-5 h-5" />
                  </Button>
                </SheetTrigger>
                <SheetContent side="right" className="w-80">
                  <SheetHeader>
                    <SheetTitle className={getBrandStyling()}>
                      {brandName}
                    </SheetTitle>
                  </SheetHeader>
                  
                  <div className="mt-6 space-y-1">
                    {filteredNavItems.map((item, index) => (
                      <motion.button
                        key={item.href}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                        onClick={() => handleItemClick(item.href)}
                        className={`
                          w-full flex items-center gap-3 px-3 py-3 rounded-lg text-left
                          transition-colors duration-200
                          ${activeItem === item.href 
                            ? 'bg-blue-100 text-blue-700' 
                            : 'hover:bg-gray-100'
                          }
                        `}
                      >
                        {item.icon}
                        <span className="flex-1">{item.label}</span>
                        {item.showBadge && (
                          <Badge variant="secondary" className="text-xs">
                            {item.badgeText}
                          </Badge>
                        )}
                      </motion.button>
                    ))}
                  </div>

                  {/* Mobile CTA */}
                  <div className="mt-6 pt-6 border-t">
                    <Button 
                      className="w-full" 
                      onClick={() => handleItemClick('/get-started')}
                    >
                      {navCTA}
                    </Button>
                  </div>
                </SheetContent>
              </Sheet>
            </div>
          </div>
        </div>
      </nav>
    );
  }

  // Desktop horizontal navigation
  if (optimizations.layout.navigation === 'horizontal') {
    return (
      <nav className={`border-b bg-white/95 backdrop-blur-sm sticky top-0 z-50 ${className}`}>
        <div className="container mx-auto px-6">
          <div className="flex items-center justify-between h-16">
            {/* Brand */}
            <div className={`text-xl ${getBrandStyling()}`}>
              {brandName}
              {confidence > 70 && (
                <Badge variant="secondary" className="ml-2 text-xs">
                  for {persona}
                </Badge>
              )}
            </div>

            {/* Navigation Items */}
            <div className="hidden md:flex items-center space-x-1">
              {filteredNavItems.slice(0, 6).map((item, index) => (
                <motion.button
                  key={item.href}
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                  onClick={() => handleItemClick(item.href)}
                  className={`
                    relative px-3 py-2 rounded-md text-sm font-medium
                    transition-colors duration-200
                    ${activeItem === item.href 
                      ? 'text-blue-600 bg-blue-50' 
                      : 'text-gray-700 hover:text-gray-900 hover:bg-gray-50'
                    }
                  `}
                >
                  <div className="flex items-center gap-2">
                    {device !== 'desktop' && item.icon}
                    <span>{item.label}</span>
                    {item.showBadge && (
                      <Badge variant="secondary" className="text-xs">
                        {item.badgeText}
                      </Badge>
                    )}
                  </div>
                </motion.button>
              ))}
            </div>

            {/* Desktop CTA */}
            <div className="flex items-center gap-4">
              {persona === 'BusinessOwner' && (
                <Button variant="ghost" size="sm">
                  Schedule Demo
                </Button>
              )}
              <Button size="sm">
                {navCTA}
              </Button>
            </div>
          </div>
        </div>
      </nav>
    );
  }

  // Sidebar navigation (for tablet or specific optimization)
  return (
    <nav className={`fixed left-0 top-0 h-full w-64 bg-white border-r z-40 ${className}`}>
      <div className="p-6">
        {/* Brand */}
        <div className={`text-xl mb-8 ${getBrandStyling()}`}>
          {brandName}
          {confidence > 70 && (
            <Badge variant="secondary" className="block mt-2 text-xs w-fit">
              Optimized for {persona}
            </Badge>
          )}
        </div>

        {/* Navigation Items */}
        <div className="space-y-1">
          {filteredNavItems.map((item, index) => (
            <motion.button
              key={item.href}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.05 }}
              onClick={() => handleItemClick(item.href)}
              className={`
                w-full flex items-center gap-3 px-3 py-2 rounded-lg text-left
                transition-colors duration-200
                ${activeItem === item.href 
                  ? 'bg-blue-100 text-blue-700' 
                  : 'hover:bg-gray-100'
                }
              `}
            >
              {item.icon}
              <span className="flex-1">{item.label}</span>
              {item.showBadge && (
                <Badge variant="secondary" className="text-xs">
                  {item.badgeText}
                </Badge>
              )}
            </motion.button>
          ))}
        </div>

        {/* Sidebar CTA */}
        <div className="mt-8 pt-6 border-t">
          <Button 
            className="w-full" 
            onClick={() => handleItemClick('/get-started')}
          >
            {navCTA}
          </Button>
          
          {persona === 'BusinessOwner' && (
            <Button 
              variant="outline" 
              className="w-full mt-2" 
              onClick={() => handleItemClick('/enterprise-demo')}
            >
              Schedule Demo
            </Button>
          )}
        </div>
      </div>
    </nav>
  );
}

export default IntelligentNavigation;
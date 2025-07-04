import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { BrandProvider } from '@/components/templates/common/BrandProvider';
import { ThemeProvider } from '@/components/templates/common/ThemeProvider';
import { AnalyticsProvider } from '@/components/providers/AnalyticsProvider';
import { PerformanceMonitor } from '@/components/foundation/seo/PerformanceMonitor';

const inter = Inter({ 
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

export const metadata: Metadata = {
  title: {
    template: '%s | Marketing Funnel Master',
    default: 'Marketing Funnel Master - AI-Powered Digital Empire',
  },
  description: 'AI-powered marketing funnel system with intelligent personalization and conversion optimization.',
  keywords: ['marketing', 'funnel', 'AI', 'conversion', 'automation', 'personalization'],
  authors: [{ name: 'Marketing Funnel Master' }],
  creator: 'Marketing Funnel Master',
  publisher: 'Marketing Funnel Master',
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://marketingfunnelmaster.com',
    siteName: 'Marketing Funnel Master',
    title: 'Marketing Funnel Master - AI-Powered Digital Empire',
    description: 'AI-powered marketing funnel system with intelligent personalization and conversion optimization.',
    images: [
      {
        url: '/images/og-image.png',
        width: 1200,
        height: 630,
        alt: 'Marketing Funnel Master',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Marketing Funnel Master - AI-Powered Digital Empire',
    description: 'AI-powered marketing funnel system with intelligent personalization and conversion optimization.',
    images: ['/images/twitter-image.png'],
  },
  verification: {
    google: 'google-site-verification-code',
  },
  alternates: {
    canonical: 'https://marketingfunnelmaster.com',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.variable} suppressHydrationWarning>
      <body className={`${inter.className} antialiased`}>
        <BrandProvider>
          <ThemeProvider
            attribute="class"
            defaultTheme="light"
            enableSystem
            disableTransitionOnChange
          >
            <AnalyticsProvider>
              <PerformanceMonitor />
              <div className="min-h-screen bg-background">
                {children}
              </div>
            </AnalyticsProvider>
          </ThemeProvider>
        </BrandProvider>
      </body>
    </html>
  );
}
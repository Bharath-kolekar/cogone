import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Providers } from '@/components/providers'
import { Toaster } from '@/components/ui/toaster'

import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  integrations: [
    new Sentry.BrowserTracing(),
    new Sentry.Replay(),
  ],
  tracesSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
  environment: process.env.NODE_ENV,
});

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Voice-to-App SaaS Platform',
  description: 'Convert voice commands to working apps in 30 seconds',
  keywords: ['voice', 'app', 'generation', 'AI', 'India', 'SaaS'],
  authors: [{ name: 'Voice-to-App Team' }],
  viewport: 'width=device-width, initial-scale=1',
  themeColor: '#3b82f6',
  manifest: '/manifest.json',
  icons: {
    icon: '/favicon.ico',
    apple: '/apple-touch-icon.png',
  },
  openGraph: {
    title: 'Voice-to-App SaaS Platform',
    description: 'Convert voice commands to working apps in 30 seconds',
    type: 'website',
    locale: 'en_IN',
    siteName: 'Voice-to-App',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Voice-to-App SaaS Platform',
    description: 'Convert voice commands to working apps in 30 seconds',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="theme-color" content="#3b82f6" />
        <link rel="icon" href="/favicon.ico" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <link rel="manifest" href="/manifest.json" />
      </head>
      <body className={inter.className}>
        <Providers>
          <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
            {children}
            <Toaster />
          </div>
        </Providers>
      </body>
    </html>
  )
}
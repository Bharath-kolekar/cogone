import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Providers } from '@/components/providers'
import { Toaster } from '@/components/ui/toaster'

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
          {children}
          <Toaster />
        </Providers>
      </body>
    </html>
  )
}
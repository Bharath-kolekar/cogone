'use client'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Provider as JotaiProvider } from 'jotai'
import { ThemeProvider } from 'next-themes'
import { useState } from 'react'
import { trpc } from '@/lib/trpc'

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 60 * 1000, // 1 minute
        retry: 1,
      },
    },
  }))

  const [trpcClient] = useState(() =>
    trpc.createClient({
      links: [
        trpc.httpBatchLink({
          url: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/trpc',
          headers() {
            return {
              authorization: `Bearer ${localStorage.getItem('access_token')}`,
            }
          },
        }),
      ],
    })
  )

  return (
    <trpc.Provider client={trpcClient} queryClient={queryClient}>
      <QueryClientProvider client={queryClient}>
        <JotaiProvider>
          <ThemeProvider
            attribute="class"
            defaultTheme="system"
            enableSystem
            disableTransitionOnChange
          >
            {children}
          </ThemeProvider>
        </JotaiProvider>
      </QueryClientProvider>
    </trpc.Provider>
  )
}
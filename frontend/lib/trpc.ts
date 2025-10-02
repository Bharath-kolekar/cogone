import { createTRPCNext } from '@trpc/next'
import { httpBatchLink } from '@trpc/client'
import type { AppRouter } from '../../backend/app/routers/index'

export const trpc = createTRPCNext<AppRouter>({
  config() {
    return {
      links: [
        httpBatchLink({
          url: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/trpc',
          headers() {
            return {
              authorization: `Bearer ${typeof window !== 'undefined' ? localStorage.getItem('access_token') : ''}`,
            }
          },
        }),
      ],
    }
  },
  ssr: false,
})
import { createTRPCNext } from '@trpc/next'
import { httpBatchLink } from '@trpc/client'
import type { inferRouterInputs, inferRouterOutputs } from '@trpc/server'

/**
 * AppRouter type definition
 * 
 * Note: Since we're using FastAPI backend (not tRPC server), we manually define the router types.
 * This creates a type-safe interface for our FastAPI endpoints.
 */

// Helper types for procedure definitions
type Query<TInput, TOutput> = {
  input: TInput
  output: TOutput
}

type Mutation<TInput, TOutput> = {
  input: TInput
  output: TOutput
}

// Define the router structure
export interface AppRouter {
  auth: {
    getProfile: Query<void, {
      id: string
      email: string
      name?: string
      avatar?: string
      created_at: string
      updated_at: string
    }>
    updateProfile: Mutation<{
      name?: string
      avatar?: string
    }, {
      success: boolean
      message: string
    }>
  }
  voice: {
    generateApp: Mutation<{
      audio_data: string
      language?: string
      app_type?: string
      complexity_level?: string
    }, {
      request_id: string
      status: string
      transcript: string
      app_type: string
      execution_time: number
      confidence_score: number
    }>
    getStatus: Query<{
      request_id: string
    }, any>
  }
  payment: {
    createOrder: Mutation<{
      amount: number
      currency?: string
      provider?: string
      description?: string
    }, {
      order_id: string
      provider: string
      amount: number
      currency: string
      payment_data: any
    }>
    verify: Mutation<{
      order_id: string
      payment_data: any
    }, {
      order_id: string
      payment_id?: string
      status: string
      amount: number
      currency: string
      provider: string
    }>
    getStatus: Query<{
      order_id: string
    }, any>
  }
  orchestrator: {
    createPlan: Mutation<{
      transcript: string
    }, {
      plan_id: string
      confidence: number
      estimated_timeline: any
      status: string
    }>
    getStatus: Query<{
      plan_id: string
    }, any>
  }
  agent: {
    createAgent: Mutation<{
      name: string
      description: string
      agent_type?: string
      capabilities?: string[]
      smarty_mode?: string
      code_capability?: string
    }, {
      agent_id: string
      name: string
      description: string
      agent_type: string
      capabilities: string[]
      status: string
    }>
    generateCode: Mutation<{
      agent_id: string
      prompt: string
      context?: any
      code_type?: string
      complexity_level?: string
    }, {
      generated_code: string
      confidence_score: number
      quality_metrics: any
      execution_time: number
    }>
  }
}

// Type inference helpers
export type RouterInput = inferRouterInputs<AppRouter>
export type RouterOutput = inferRouterOutputs<AppRouter>

/**
 * tRPC client configuration
 * 
 * Configures the tRPC client to communicate with our FastAPI backend.
 * The backend has a tRPC-compatible endpoint at /trpc/* that handles all procedures.
 */
export const trpc = createTRPCNext<AppRouter>({
  config({ ctx }) {
    return {
      links: [
        httpBatchLink({
          /**
           * API endpoint - connects to FastAPI backend
           * Backend route: POST /trpc/{procedure:path}
           */
          url: `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/trpc`,
          
          /**
           * Headers configuration
           * Includes authentication token from localStorage
           */
          headers() {
            const token = typeof window !== 'undefined' 
              ? localStorage.getItem('access_token') 
              : ''
            
            return {
              authorization: token ? `Bearer ${token}` : '',
              'content-type': 'application/json',
            }
          },
          
          /**
           * Fetch options
           * Includes credentials for CORS
           */
          fetch(url, options) {
            return fetch(url, {
              ...options,
              credentials: 'include',
            })
          },
        }),
      ],
      
      /**
       * Query client config
       */
      queryClientConfig: {
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000, // 1 minute
            retry: 1,
            refetchOnWindowFocus: false,
          },
        },
      },
    }
  },
  
  /**
   * SSR configuration
   * Disabled for now since we're using client-side rendering
   */
  ssr: false,
})

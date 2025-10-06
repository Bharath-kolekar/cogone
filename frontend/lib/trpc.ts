import { createTRPCNext } from '@trpc/next'
import { httpBatchLink } from '@trpc/client'

// Define AppRouter type based on our FastAPI backend
type AppRouter = {
  auth: {
    getProfile: {
      input: void
      output: {
        id: string
        email: string
        name?: string
        avatar?: string
        created_at: string
        updated_at: string
      }
    }
    updateProfile: {
      input: {
        name?: string
        avatar?: string
      }
      output: {
        success: boolean
        message: string
      }
    }
  }
  voice: {
    generateApp: {
      input: {
        audio_data: string
        language?: string
        app_type?: string
        complexity_level?: string
      }
      output: {
        request_id: string
        status: string
        transcript: string
        app_type: string
        execution_time: number
        confidence_score: number
      }
    }
    getStatus: {
      input: {
        request_id: string
      }
      output: any
    }
  }
  payment: {
    createOrder: {
      input: {
        amount: number
        currency?: string
        provider?: string
        description?: string
      }
      output: {
        order_id: string
        provider: string
        amount: number
        currency: string
        payment_data: any
      }
    }
    verify: {
      input: {
        order_id: string
        payment_data: any
      }
      output: {
        order_id: string
        payment_id?: string
        status: string
        amount: number
        currency: string
        provider: string
      }
    }
    getStatus: {
      input: {
        order_id: string
      }
      output: any
    }
  }
  orchestrator: {
    createPlan: {
      input: {
        transcript: string
      }
      output: {
        plan_id: string
        confidence: number
        estimated_timeline: any
        status: string
      }
    }
    getStatus: {
      input: {
        plan_id: string
      }
      output: any
    }
  }
  agent: {
    createAgent: {
      input: {
        name: string
        description: string
        agent_type?: string
        capabilities?: string[]
        smarty_mode?: string
        code_capability?: string
      }
      output: {
        agent_id: string
        name: string
        description: string
        agent_type: string
        capabilities: string[]
        status: string
      }
    }
    generateCode: {
      input: {
        agent_id: string
        prompt: string
        context?: any
        code_type?: string
        complexity_level?: string
      }
      output: {
        generated_code: string
        confidence_score: number
        quality_metrics: any
        execution_time: number
      }
    }
  }
}

export const trpc = createTRPCNext<AppRouter>({
  config() {
    return {
      links: [
        httpBatchLink({
          url: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api',
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
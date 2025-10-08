/**
 * Type Definitions
 * Extracted from large file for better organization
 */

export interface AIComponent {
  id: string
  name: string
  type: 'orchestrator' | 'smarty' | 'dna' | 'ethical' | 'advanced' | 'business' | 'system' | 'communication' | 'admin' | 'tools'
  status: 'active' | 'inactive' | 'error'
  capabilities: string[]
  voiceCommands: string[]
  priority: 'high' | 'medium' | 'low'
  category: string
}



export interface VoiceAIState {
  isConnected: boolean
  activeComponents: AIComponent[]
  lastCommand: string | null
  aiResponse: string | null
  processingStatus: 'idle' | 'processing' | 'completed' | 'error'
  error: string | null
}



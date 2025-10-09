/**
 * Type Definitions
 * Extracted from large file for better organization
 */

interface AIComponent {
  id: string
  name: string
  type: string
  category: string
  status: 'active' | 'inactive' | 'error' | 'loading'
  confidence: number
  lastUsed?: string
  capabilities: string[]
  voiceCommands: string[]
}



interface IntegrationResult {
  responseId: string
  primaryResponse: any
  supportingResponses: Record<string, any>
  confidence: number
  integrationMetadata: Record<string, any>
  timestamp: string
}



interface SmartCodingAIDashboardProps {
  onIntegrationResult?: (result: IntegrationResult) => void
  onComponentStatusChange?: (componentId: string, status: string) => void
}



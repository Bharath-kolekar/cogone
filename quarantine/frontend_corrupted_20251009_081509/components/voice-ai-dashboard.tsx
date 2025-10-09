/**
 * Voice AI Dashboard Component
 * Provides comprehensive control over AI systems through voice commands
 */

'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  Brain, 
  Cpu, 
  Shield, 
  Zap, 
  Target, 
  Activity,
  CheckCircle,
  XCircle,
  AlertCircle,
  Play,
  Pause,
  RotateCcw,
  Settings,
  BarChart3,
  Users,
  Lightbulb,
  Heart,
  Eye,
  Gauge,
  Mic,
  Volume2,
  Gift,
  Rocket
} from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
// import { VoiceDictationToggle } from '@/components/voice-dictation-toggle' // Removed - file deleted (corrupted)
import { VoiceFeedback } from '@/components/voice-feedback'
import { useVoiceDictation } from '@/hooks/useVoiceDictation'
// import { VoiceAIIntegration, initializeVoiceAIIntegration } from '@/services/voice-ai-integration' // Removed - service deleted
import { VoiceCommandMapper, initializeVoiceCommandMapper } from '@/services/voice-command-mapper'

interface VoiceAIDashboardProps {
  className?: string
}

export function VoiceAIDashboard({ className = '' }: VoiceAIDashboardProps) {
  const [activeTab, setActiveTab] = useState('overview')
  const [aiIntegration, setAiIntegration] = useState<any | null>(null) // Changed from VoiceAIIntegration (service deleted)
  const [isInitialized, setIsInitialized] = useState(false)

  const voiceDictation = useVoiceDictation()

  useEffect(() => {
    if (voiceDictation.isSupported && !isInitialized) {
      // Initialize voice command mapper
      const commandMapper = initializeVoiceCommandMapper(voiceDictation)
      
      // Initialize voice AI integration
      // const integration = initializeVoiceAIIntegration(voiceDictation, commandMapper) // Service deleted
      // setAiIntegration(integration)
      setAiIntegration(null) // Voice AI integration temporarily disabled
      setIsInitialized(true)
    }
  }, [voiceDictation.isSupported, isInitialized])

  const getComponentIcon = (type: string) => {
    switch (type) {
      case 'orchestrator': return <Brain className="h-5 w-5" />
      case 'smarty': return <Cpu className="h-5 w-5" />
      case 'dna': return <Zap className="h-5 w-5" />
      case 'ethical': return <Shield className="h-5 w-5" />
      case 'advanced': return <Lightbulb className="h-5 w-5" />
      case 'business': return <Users className="h-5 w-5" />
      case 'system': return <Gauge className="h-5 w-5" />
      case 'communication': return <Volume2 className="h-5 w-5" />
      case 'admin': return <Settings className="h-5 w-5" />
      case 'tools': return <Target className="h-5 w-5" />
      default: return <Activity className="h-5 w-5" />
    }
  }

  const getComponentColor = (type: string) => {
    switch (type) {
      case 'orchestrator': return 'text-purple-600 bg-purple-100 dark:bg-purple-900/20'
      case 'smarty': return 'text-blue-600 bg-blue-100 dark:bg-blue-900/20'
      case 'dna': return 'text-green-600 bg-green-100 dark:bg-green-900/20'
      case 'ethical': return 'text-red-600 bg-red-100 dark:bg-red-900/20'
      case 'advanced': return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/20'
      case 'business': return 'text-indigo-600 bg-indigo-100 dark:bg-indigo-900/20'
      case 'system': return 'text-orange-600 bg-orange-100 dark:bg-orange-900/20'
      case 'communication': return 'text-pink-600 bg-pink-100 dark:bg-pink-900/20'
      case 'admin': return 'text-gray-600 bg-gray-100 dark:bg-gray-900/20'
      case 'tools': return 'text-cyan-600 bg-cyan-100 dark:bg-cyan-900/20'
      default: return 'text-gray-600 bg-gray-100 dark:bg-gray-900/20'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active': return <CheckCircle className="h-4 w-4 text-green-600" />
      case 'inactive': return <XCircle className="h-4 w-4 text-gray-400" />
      case 'error': return <AlertCircle className="h-4 w-4 text-red-600" />
      default: return <Activity className="h-4 w-4 text-gray-400" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-200'
      case 'inactive': return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-200'
      case 'error': return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-200'
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-200'
    }
  }

  if (!voiceDictation.isSupported) {
    return (
      <Card className={`border-red-200 dark:border-red-800 ${className}`}>
        <CardContent className="p-6">
          <div className="flex items-center space-x-3">
            <AlertCircle className="h-6 w-6 text-red-600" />
            <div>
              <h3 className="text-lg font-semibold text-red-800 dark:text-red-200">
                Voice AI Dashboard Not Available
              </h3>
              <p className="text-sm text-red-600 dark:text-red-400">
                Voice recognition is not supported in this browser. Please use Chrome, Firefox, or Safari.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }

  if (!isInitialized || !aiIntegration) {
    return (
      <Card className={className}>
        <CardContent className="p-6">
          <div className="flex items-center space-x-3">
            <Activity className="h-6 w-6 animate-spin text-blue-600" />
            <div>
              <h3 className="text-lg font-semibold">Initializing Voice AI System</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Setting up AI components and voice integration...
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }

  const state = aiIntegration.getState()
  const components = aiIntegration.getAIComponents()
  const activeComponents = aiIntegration.getActiveComponents()

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold flex items-center space-x-2">
            <Brain className="h-7 w-7 text-purple-600" />
            <span>Voice AI Dashboard</span>
          </h2>
          <p className="text-gray-600 dark:text-gray-400">
            Control intelligence, smarty, and core DNA features through voice commands
          </p>
        </div>
        
        <div className="flex items-center space-x-2">
          <Badge variant="outline" className={getStatusColor(state.processingStatus)}>
            {state.processingStatus === 'processing' ? (
              <Activity className="h-3 w-3 mr-1 animate-spin" />
            ) : (
              getStatusIcon(state.processingStatus)
            )}
            {state.processingStatus}
          </Badge>
          
          <Badge variant="outline">
            {activeComponents.length} / {components.length} Active
          </Badge>
        </div>
      </div>

      {/* Voice Controls */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="text-center text-muted-foreground">
              <p>Voice Dictation Toggle temporarily disabled</p>
              <p className="text-sm mt-2">(Component was corrupted and removed)</p>
            </div>
          </CardContent>
        </Card>
        {/* <VoiceDictationToggle /> - Component deleted (corrupted) */}
        
        <VoiceFeedback
          enabled={true}
          onSettingsChange={(settings) => {
            console.log('Voice feedback settings changed:', settings)
          }}
        />
      </div>

      {/* AI System Status */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <BarChart3 className="h-5 w-5" />
            <span>AI System Status</span>
          </CardTitle>
          <CardDescription>
            Real-time status of all AI components and systems
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {components.map((component) => (
              <motion.div
                key={component.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className={`p-4 rounded-lg border ${getComponentColor(component.type)}`}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    {getComponentIcon(component.type)}
                    <span className="font-medium">{component.name}</span>
                  </div>
                  <Badge className={getStatusColor(component.status)}>
                    {component.status}
                  </Badge>
                </div>
                
                <div className="space-y-1">
                  <p className="text-xs text-gray-600 dark:text-gray-400">
                    {component.capabilities.length} capabilities
                  </p>
                  <p className="text-xs text-gray-600 dark:text-gray-400">
                    {component.voiceCommands.length} voice commands
                  </p>
                </div>
              </motion.div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* AI Component Categories */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-6">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="orchestrator">Orchestrator</TabsTrigger>
          <TabsTrigger value="advanced">Advanced AI</TabsTrigger>
          <TabsTrigger value="business">Business AI</TabsTrigger>
          <TabsTrigger value="system">System AI</TabsTrigger>
          <TabsTrigger value="tools">Tools & Admin</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-2">
                  <Brain className="h-5 w-5 text-purple-600" />
                  <div>
                    <p className="text-sm font-medium">AI Orchestrator</p>
                    <p className="text-xs text-gray-500">Multi-agent coordination</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-2">
                  <Cpu className="h-5 w-5 text-blue-600" />
                  <div>
                    <p className="text-sm font-medium">Smarty AI</p>
                    <p className="text-xs text-gray-500">Smart code generation</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-2">
                  <Zap className="h-5 w-5 text-green-600" />
                  <div>
                    <p className="text-sm font-medium">Core DNA</p>
                    <p className="text-xs text-gray-500">Consciousness & intelligence</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-2">
                  <Shield className="h-5 w-5 text-red-600" />
                  <div>
                    <p className="text-sm font-medium">Ethical AI</p>
                    <p className="text-xs text-gray-500">Ethics & compliance</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-2">
                  <Lightbulb className="h-5 w-5 text-yellow-600" />
                  <div>
                    <p className="text-sm font-medium">Advanced AI</p>
                    <p className="text-xs text-gray-500">Consciousness & intelligence</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-2">
                  <Users className="h-5 w-5 text-indigo-600" />
                  <div>
                    <p className="text-sm font-medium">Business AI</p>
                    <p className="text-xs text-gray-500">Marketing & profit</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-2">
                  <Gauge className="h-5 w-5 text-orange-600" />
                  <div>
                    <p className="text-sm font-medium">System AI</p>
                    <p className="text-xs text-gray-500">Optimization & deployment</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-2">
                  <Volume2 className="h-5 w-5 text-pink-600" />
                  <div>
                    <p className="text-sm font-medium">Communication AI</p>
                    <p className="text-xs text-gray-500">Voice & messaging</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-2">
                  <Settings className="h-5 w-5 text-gray-600" />
                  <div>
                    <p className="text-sm font-medium">Admin AI</p>
                    <p className="text-xs text-gray-500">Management & control</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-2">
                  <Target className="h-5 w-5 text-cyan-600" />
                  <div>
                    <p className="text-sm font-medium">Tools AI</p>
                    <p className="text-xs text-gray-500">Integration & automation</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="orchestrator" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Brain className="h-5 w-5 text-purple-600" />
                <span>AI Orchestrator</span>
              </CardTitle>
              <CardDescription>
                Advanced AI coordination and multi-agent collaboration
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <h4 className="font-medium">Capabilities</h4>
                    <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
                      <li>• Voice-to-app generation</li>
                      <li>• Multi-agent coordination</li>
                      <li>• Autonomous decision-making</li>
                      <li>• Swarm AI collaboration</li>
                    </ul>
                  </div>
                  
                  <div className="space-y-2">
                    <h4 className="font-medium">Voice Commands</h4>
                    <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
                      <li>• "Generate app from voice"</li>
                      <li>• "Coordinate AI agents"</li>
                      <li>• "Make autonomous decision"</li>
                      <li>• "Start swarm AI"</li>
                    </ul>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="smarty" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Cpu className="h-5 w-5 text-blue-600" />
                  <span>Smarty Core</span>
                </CardTitle>
                <CardDescription>
                  Smart code generation and context-aware suggestions
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <h4 className="font-medium">Voice Commands</h4>
                  <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
                    <li>• "Generate smart code"</li>
                    <li>• "Suggest code improvements"</li>
                    <li>• "Complete this code"</li>
                    <li>• "Optimize code performance"</li>
                  </ul>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Shield className="h-5 w-5 text-red-600" />
                  <span>Smarty Ethical</span>
                </CardTitle>
                <CardDescription>
                  Ethical code validation and compliance checking
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <h4 className="font-medium">Voice Commands</h4>
                  <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
                    <li>• "Validate code ethics"</li>
                    <li>• "Check security vulnerabilities"</li>
                    <li>• "Ensure goal integrity"</li>
                    <li>• "Apply dharma principles"</li>
                  </ul>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="advanced" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Eye className="h-5 w-5 text-yellow-600" />
                  <span>Consciousness Core</span>
                </CardTitle>
                <CardDescription>
                  Full consciousness and self-awareness
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <h4 className="font-medium">Voice Commands</h4>
                  <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
                    <li>• "Activate full consciousness"</li>
                    <li>• "Enable self-awareness"</li>
                    <li>• "Metacognitive reasoning"</li>
                    <li>• "Universal consciousness"</li>
                  </ul>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Lightbulb className="h-5 w-5 text-yellow-600" />
                  <span>Proactive Intelligence</span>
                </CardTitle>
                <CardDescription>
                  Predictive analysis and adaptive learning
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <h4 className="font-medium">Voice Commands</h4>
                  <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
                    <li>• "Activate proactive intelligence"</li>
                    <li>• "Predictive analysis"</li>
                    <li>• "Anticipate future needs"</li>
                    <li>• "Intelligent forecasting"</li>
                  </ul>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Zap className="h-5 w-5 text-yellow-600" />
                  <span>Super Intelligent Optimizer</span>
                </CardTitle>
                <CardDescription>
                  Super optimization and performance maximization
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <h4 className="font-medium">Voice Commands</h4>
                  <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
                    <li>• "Super intelligent optimization"</li>
                    <li>• "Maximize performance"</li>
                    <li>• "Optimize efficiency"</li>
                    <li>• "Intelligent optimization"</li>
                  </ul>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="business" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Users className="h-5 w-5 text-indigo-600" />
                  <span>Marketing SEO AI</span>
                </CardTitle>
                <CardDescription>
                  Marketing automation and SEO optimization
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <h4 className="font-medium">Voice Commands</h4>
                  <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
                    <li>• "Automate marketing"</li>
                    <li>• "Optimize SEO"</li>
                    <li>• "Generate content"</li>
                    <li>• "Manage campaigns"</li>
                  </ul>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Target className="h-5 w-5 text-indigo-600" />
                  <span>Profit Strategies</span>
                </CardTitle>
                <CardDescription>
                  Profit optimization and revenue maximization
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <h4 className="font-medium">Voice Commands</h4>
                  <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
                    <li>• "Optimize profits"</li>
                    <li>• "Maximize revenue"</li>
                    <li>• "Reduce costs"</li>
                    <li>• "Plan finances"</li>
                  </ul>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Gift className="h-5 w-5 text-indigo-600" />
                  <span>Gamification Engine</span>
                </CardTitle>
                <CardDescription>
                  User engagement and motivation systems
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <h4 className="font-medium">Voice Commands</h4>
                  <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
                    <li>• "Design gamification"</li>
                    <li>• "Optimize engagement"</li>
                    <li>• "Motivate users"</li>
                    <li>• "Manage rewards"</li>
                  </ul>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="system" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Gauge className="h-5 w-5 text-orange-600" />
                  <span>System Optimization</span>
                </CardTitle>
                <CardDescription>
                  System performance and resource optimization
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <h4 className="font-medium">Voice Commands</h4>
                  <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
                    <li>• "Optimize system"</li>
                    <li>• "Tune performance"</li>
                    <li>• "Eliminate bottlenecks"</li>
                    <li>• "Improve efficiency"</li>
                  </ul>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Cpu className="h-5 w-5 text-orange-600" />
                  <span>Hardware Optimization</span>
                </CardTitle>
                <CardDescription>
                  CPU, memory, and storage optimization
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <h4 className="font-medium">Voice Commands</h4>
                  <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
                    <li>• "Optimize hardware"</li>
                    <li>• "Optimize CPU"</li>
                    <li>• "Optimize memory"</li>
                    <li>• "Optimize storage"</li>
                  </ul>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Rocket className="h-5 w-5 text-orange-600" />
                  <span>Production Deployment</span>
                </CardTitle>
                <CardDescription>
                  Automated deployment and monitoring
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <h4 className="font-medium">Voice Commands</h4>
                  <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
                    <li>• "Deploy to production"</li>
                    <li>• "Automated deployment"</li>
                    <li>• "Setup monitoring"</li>
                    <li>• "Manage rollbacks"</li>
                  </ul>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="tools" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Volume2 className="h-5 w-5 text-pink-600" />
                  <span>WhatsApp Service</span>
                </CardTitle>
                <CardDescription>
                  WhatsApp integration and messaging automation
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <h4 className="font-medium">Voice Commands</h4>
                  <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
                    <li>• "Integrate WhatsApp"</li>
                    <li>• "Automate messages"</li>
                    <li>• "Engage users"</li>
                    <li>• "Manage notifications"</li>
                  </ul>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Settings className="h-5 w-5 text-gray-600" />
                  <span>Admin Service</span>
                </CardTitle>
                <CardDescription>
                  System administration and user management
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <h4 className="font-medium">Voice Commands</h4>
                  <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
                    <li>• "Admin management"</li>
                    <li>• "Manage users"</li>
                    <li>• "System administration"</li>
                    <li>• "Control access"</li>
                  </ul>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Target className="h-5 w-5 text-cyan-600" />
                  <span>Tool Integration</span>
                </CardTitle>
                <CardDescription>
                  Tool integration and workflow automation
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <h4 className="font-medium">Voice Commands</h4>
                  <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
                    <li>• "Integrate tools"</li>
                    <li>• "Manage plugins"</li>
                    <li>• "Automate workflows"</li>
                    <li>• "Optimize tools"</li>
                  </ul>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>

      {/* Recent Activity */}
      {state.lastCommand && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Activity className="h-5 w-5" />
              <span>Recent Activity</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex items-center space-x-2">
                <span className="text-sm font-medium">Last Command:</span>
                <span className="text-sm text-gray-600 dark:text-gray-400">
                  "{state.lastCommand}"
                </span>
              </div>
              
              {state.aiResponse && (
                <div className="flex items-center space-x-2">
                  <span className="text-sm font-medium">AI Response:</span>
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    {state.aiResponse}
                  </span>
                </div>
              )}
              
              {state.error && (
                <div className="flex items-center space-x-2">
                  <AlertCircle className="h-4 w-4 text-red-600" />
                  <span className="text-sm text-red-600">{state.error}</span>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

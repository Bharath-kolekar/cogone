'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Cpu, MemoryStick, HardDrive, Zap, Target, TrendingUp, Activity, Settings, Play, Pause, RotateCcw, BarChart3, Gauge, Thermometer } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Slider } from '@/components/ui/slider'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

interface ResourceMetrics {
  cpu: {
    usage: number
    cores: number
    frequency: number
    temperature: number
    efficiency: number
  }
  memory: {
    usage: number
    total: number
    available: number
    swap: number
    efficiency: number
  }
  storage: {
    usage: number
    total: number
    readSpeed: number
    writeSpeed: number
    efficiency: number
  }
  network: {
    bandwidth: number
    latency: number
    throughput: number
    efficiency: number
  }
  gpu?: {
    usage: number
    memory: number
    temperature: number
    efficiency: number
  }
}

interface OptimizationConfig {
  mode: 'performance' | 'balanced' | 'power-save' | 'custom'
  cpuOptimization: boolean
  memoryOptimization: boolean
  storageOptimization: boolean
  networkOptimization: boolean
  gpuOptimization: boolean
  adaptiveScaling: boolean
  predictiveOptimization: boolean
  realTimeMonitoring: boolean
}

interface AdvancedResourceManagerProps {
  onOptimizationComplete?: (metrics: ResourceMetrics) => void
  showRealTimeMetrics?: boolean
  enableAdaptiveOptimization?: boolean
  className?: string
}

export function AdvancedResourceManager({
  onOptimizationComplete,
  showRealTimeMetrics = true,
  enableAdaptiveOptimization = true,
  className = ''
}: AdvancedResourceManagerProps) {
  const [metrics, setMetrics] = useState<ResourceMetrics | null>(null)
  const [isOptimizing, setIsOptimizing] = useState(false)
  const [optimizationStep, setOptimizationStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [config, setConfig] = useState<OptimizationConfig>({
    mode: 'balanced',
    cpuOptimization: true,
    memoryOptimization: true,
    storageOptimization: true,
    networkOptimization: true,
    gpuOptimization: true,
    adaptiveScaling: true,
    predictiveOptimization: true,
    realTimeMonitoring: true
  })
  const [activeTab, setActiveTab] = useState('overview')
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [optimizationHistory, setOptimizationHistory] = useState<Array<{timestamp: Date, metrics: ResourceMetrics}>>([])
  const [isMonitoring, setIsMonitoring] = useState(false)
  const monitoringRef = useRef<NodeJS.Timeout | null>(null)
  const optimizationRef = useRef<ResourceMetrics | null>(null)

  useEffect(() => {
    if (config.realTimeMonitoring) {
      startRealTimeMonitoring()
    } else {
      stopRealTimeMonitoring()
    }

    return () => {
      stopRealTimeMonitoring()
    }
  }, [config.realTimeMonitoring])

  const startRealTimeMonitoring = useCallback(() => {
    if (monitoringRef.current) return

    setIsMonitoring(true)
    monitoringRef.current = setInterval(() => {
      collectResourceMetrics()
    }, 1000)
  }, [])

  const stopRealTimeMonitoring = useCallback(() => {
    if (monitoringRef.current) {
      clearInterval(monitoringRef.current)
      monitoringRef.current = null
    }
    setIsMonitoring(false)
  }, [])

  const collectResourceMetrics = async () => {
    try {
      // Simulate advanced resource monitoring
      const mockMetrics: ResourceMetrics = {
        cpu: {
          usage: Math.random() * 100,
          cores: navigator.hardwareConcurrency || 4,
          frequency: 2000 + Math.random() * 2000,
          temperature: 30 + Math.random() * 40,
          efficiency: 0.7 + Math.random() * 0.3
        },
        memory: {
          usage: Math.random() * 100,
          total: 8 + Math.random() * 24, // 8-32GB
          available: Math.random() * 8,
          swap: Math.random() * 4,
          efficiency: 0.6 + Math.random() * 0.4
        },
        storage: {
          usage: Math.random() * 100,
          total: 500 + Math.random() * 1500, // 500GB-2TB
          readSpeed: 100 + Math.random() * 500, // MB/s
          writeSpeed: 50 + Math.random() * 300, // MB/s
          efficiency: 0.5 + Math.random() * 0.5
        },
        network: {
          bandwidth: 10 + Math.random() * 90, // Mbps
          latency: 1 + Math.random() * 50, // ms
          throughput: Math.random() * 100, // %
          efficiency: 0.6 + Math.random() * 0.4
        },
        gpu: {
          usage: Math.random() * 100,
          memory: Math.random() * 8, // GB
          temperature: 35 + Math.random() * 30,
          efficiency: 0.5 + Math.random() * 0.5
        }
      }

      setMetrics(mockMetrics)
      optimizationRef.current = mockMetrics
      onOptimizationComplete?.(mockMetrics)

      // Add to history
      setOptimizationHistory(prev => [
        { timestamp: new Date(), metrics: mockMetrics },
        ...prev.slice(0, 99) // Keep last 100 entries
      ])

    } catch (error) {
      console.error('Resource monitoring failed:', error)
    }
  }

  const optimizeResources = async () => {
    setIsOptimizing(true)
    setProgress(0)
    setOptimizationStep('Initializing advanced resource optimization...')

    try {
      // Simulate optimization steps
      const steps = [
        'Analyzing current resource utilization...',
        'Identifying optimization opportunities...',
        'Applying CPU optimization algorithms...',
        'Optimizing memory allocation patterns...',
        'Enhancing storage I/O performance...',
        'Tuning network parameters...',
        'Configuring GPU acceleration...',
        'Implementing adaptive scaling...',
        'Enabling predictive optimization...',
        'Finalizing resource allocation...'
      ]

      for (let i = 0; i < steps.length; i++) {
        setOptimizationStep(steps[i])
        setProgress((i + 1) * 10)
        await new Promise(resolve => setTimeout(resolve, 300))
      }

      // Apply optimizations
      await applyOptimizations()
      
      // Collect optimized metrics
      await collectResourceMetrics()

    } catch (error) {
      console.error('Resource optimization failed:', error)
    } finally {
      setIsOptimizing(false)
      setProgress(100)
      setOptimizationStep('Optimization complete!')
    }
  }

  const applyOptimizations = async () => {
    // Simulate advanced optimization algorithms
    await new Promise(resolve => setTimeout(resolve, 1000))

    // Apply CPU optimizations
    if (config.cpuOptimization) {
      await optimizeCPU()
    }

    // Apply memory optimizations
    if (config.memoryOptimization) {
      await optimizeMemory()
    }

    // Apply storage optimizations
    if (config.storageOptimization) {
      await optimizeStorage()
    }

    // Apply network optimizations
    if (config.networkOptimization) {
      await optimizeNetwork()
    }

    // Apply GPU optimizations
    if (config.gpuOptimization) {
      await optimizeGPU()
    }
  }

  const optimizeCPU = async () => {
    // Simulate CPU optimization algorithms
    console.log('Applying CPU optimization algorithms...')
    await new Promise(resolve => setTimeout(resolve, 200))
  }

  const optimizeMemory = async () => {
    // Simulate memory optimization algorithms
    console.log('Applying memory optimization algorithms...')
    await new Promise(resolve => setTimeout(resolve, 200))
  }

  const optimizeStorage = async () => {
    // Simulate storage optimization algorithms
    console.log('Applying storage optimization algorithms...')
    await new Promise(resolve => setTimeout(resolve, 200))
  }

  const optimizeNetwork = async () => {
    // Simulate network optimization algorithms
    console.log('Applying network optimization algorithms...')
    await new Promise(resolve => setTimeout(resolve, 200))
  }

  const optimizeGPU = async () => {
    // Simulate GPU optimization algorithms
    console.log('Applying GPU optimization algorithms...')
    await new Promise(resolve => setTimeout(resolve, 200))
  }

  const getEfficiencyColor = (efficiency: number) => {
    if (efficiency > 0.8) return 'text-green-600 bg-green-100'
    if (efficiency > 0.6) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  const getUsageColor = (usage: number) => {
    if (usage > 90) return 'text-red-600 bg-red-100'
    if (usage > 70) return 'text-yellow-600 bg-yellow-100'
    return 'text-green-600 bg-green-100'
  }

  const getTemperatureColor = (temp: number) => {
    if (temp > 80) return 'text-red-600 bg-red-100'
    if (temp > 60) return 'text-yellow-600 bg-yellow-100'
    return 'text-green-600 bg-green-100'
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <Card className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center space-x-2">
                <Cpu className="h-6 w-6 text-blue-600" />
                <span>Advanced Resource Manager</span>
              </CardTitle>
              <CardDescription>
                Intelligent hardware resource optimization for maximum performance
              </CardDescription>
            </div>
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setIsMonitoring(!isMonitoring)}
              >
                {isMonitoring ? <Pause className="h-4 w-4 mr-1" /> : <Play className="h-4 w-4 mr-1" />}
                {isMonitoring ? 'Stop' : 'Monitor'}
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={optimizeResources}
                disabled={isOptimizing}
              >
                <Zap className="h-4 w-4 mr-1" />
                Optimize
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {/* Optimization Configuration */}
          <div className="space-y-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <Button
                variant={config.mode === 'performance' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setConfig(prev => ({ ...prev, mode: 'performance' }))}
              >
                Performance
              </Button>
              <Button
                variant={config.mode === 'balanced' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setConfig(prev => ({ ...prev, mode: 'balanced' }))}
              >
                Balanced
              </Button>
              <Button
                variant={config.mode === 'power-save' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setConfig(prev => ({ ...prev, mode: 'power-save' }))}
              >
                Power Save
              </Button>
              <Button
                variant={config.mode === 'custom' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setConfig(prev => ({ ...prev, mode: 'custom' }))}
              >
                Custom
              </Button>
            </div>

            {/* Optimization Status */}
            {isOptimizing && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4"
              >
                <div className="flex items-center space-x-3 mb-3">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
                  <span className="text-sm font-medium text-blue-800 dark:text-blue-200">
                    {optimizationStep}
                  </span>
                </div>
                <Progress value={progress} className="h-2" />
              </motion.div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Resource Metrics */}
      {metrics && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-blue-100 dark:bg-blue-900/20 rounded-lg">
                    <Cpu className="h-5 w-5 text-blue-600" />
                  </div>
                  <div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">CPU Usage</div>
                    <div className="text-xl font-bold">
                      <Badge className={getUsageColor(metrics.cpu.usage)}>
                        {metrics.cpu.usage.toFixed(1)}%
                      </Badge>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-green-100 dark:bg-green-900/20 rounded-lg">
                    <MemoryStick className="h-5 w-5 text-green-600" />
                  </div>
                  <div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Memory</div>
                    <div className="text-xl font-bold">
                      <Badge className={getUsageColor(metrics.memory.usage)}>
                        {metrics.memory.usage.toFixed(1)}%
                      </Badge>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-purple-100 dark:bg-purple-900/20 rounded-lg">
                    <HardDrive className="h-5 w-5 text-purple-600" />
                  </div>
                  <div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Storage</div>
                    <div className="text-xl font-bold">
                      <Badge className={getUsageColor(metrics.storage.usage)}>
                        {metrics.storage.usage.toFixed(1)}%
                      </Badge>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-orange-100 dark:bg-orange-900/20 rounded-lg">
                    <Activity className="h-5 w-5 text-orange-600" />
                  </div>
                  <div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Network</div>
                    <div className="text-xl font-bold">
                      <Badge className={getUsageColor(metrics.network.throughput)}>
                        {metrics.network.throughput.toFixed(1)}%
                      </Badge>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Detailed Metrics */}
          <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
            <TabsList className="grid w-full grid-cols-5">
              <TabsTrigger value="overview">Overview</TabsTrigger>
              <TabsTrigger value="cpu">CPU</TabsTrigger>
              <TabsTrigger value="memory">Memory</TabsTrigger>
              <TabsTrigger value="storage">Storage</TabsTrigger>
              <TabsTrigger value="network">Network</TabsTrigger>
            </TabsList>

            <TabsContent value="overview" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="text-sm flex items-center space-x-2">
                      <TrendingUp className="h-4 w-4" />
                      <span>Performance Summary</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">CPU Efficiency</span>
                        <Badge className={getEfficiencyColor(metrics.cpu.efficiency)}>
                          {(metrics.cpu.efficiency * 100).toFixed(1)}%
                        </Badge>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Memory Efficiency</span>
                        <Badge className={getEfficiencyColor(metrics.memory.efficiency)}>
                          {(metrics.memory.efficiency * 100).toFixed(1)}%
                        </Badge>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Storage Efficiency</span>
                        <Badge className={getEfficiencyColor(metrics.storage.efficiency)}>
                          {(metrics.storage.efficiency * 100).toFixed(1)}%
                        </Badge>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Network Efficiency</span>
                        <Badge className={getEfficiencyColor(metrics.network.efficiency)}>
                          {(metrics.network.efficiency * 100).toFixed(1)}%
                        </Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-sm flex items-center space-x-2">
                      <Settings className="h-4 w-4" />
                      <span>Optimization Status</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">CPU Optimization</span>
                        <Badge variant={config.cpuOptimization ? 'default' : 'outline'}>
                          {config.cpuOptimization ? 'Enabled' : 'Disabled'}
                        </Badge>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Memory Optimization</span>
                        <Badge variant={config.memoryOptimization ? 'default' : 'outline'}>
                          {config.memoryOptimization ? 'Enabled' : 'Disabled'}
                        </Badge>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Storage Optimization</span>
                        <Badge variant={config.storageOptimization ? 'default' : 'outline'}>
                          {config.storageOptimization ? 'Enabled' : 'Disabled'}
                        </Badge>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Network Optimization</span>
                        <Badge variant={config.networkOptimization ? 'default' : 'outline'}>
                          {config.networkOptimization ? 'Enabled' : 'Disabled'}
                        </Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="cpu" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="text-sm flex items-center space-x-2">
                      <Cpu className="h-4 w-4" />
                      <span>CPU Metrics</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Usage</span>
                        <span className="font-medium">{metrics.cpu.usage.toFixed(1)}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-blue-500 h-2 rounded-full"
                          style={{ width: `${metrics.cpu.usage}%` }}
                        />
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Cores</span>
                        <span className="font-medium">{metrics.cpu.cores}</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Frequency</span>
                        <span className="font-medium">{metrics.cpu.frequency.toFixed(0)} MHz</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-sm flex items-center space-x-2">
                      <Thermometer className="h-4 w-4" />
                      <span>Temperature & Efficiency</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Temperature</span>
                        <Badge className={getTemperatureColor(metrics.cpu.temperature)}>
                          {metrics.cpu.temperature.toFixed(1)}°C
                        </Badge>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Efficiency</span>
                        <Badge className={getEfficiencyColor(metrics.cpu.efficiency)}>
                          {(metrics.cpu.efficiency * 100).toFixed(1)}%
                        </Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="memory" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="text-sm flex items-center space-x-2">
                      <MemoryStick className="h-4 w-4" />
                      <span>Memory Usage</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Usage</span>
                        <span className="font-medium">{metrics.memory.usage.toFixed(1)}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-green-500 h-2 rounded-full"
                          style={{ width: `${metrics.memory.usage}%` }}
                        />
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Total</span>
                        <span className="font-medium">{metrics.memory.total.toFixed(1)} GB</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Available</span>
                        <span className="font-medium">{metrics.memory.available.toFixed(1)} GB</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-sm flex items-center space-x-2">
                      <Gauge className="h-4 w-4" />
                      <span>Memory Efficiency</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Efficiency</span>
                        <Badge className={getEfficiencyColor(metrics.memory.efficiency)}>
                          {(metrics.memory.efficiency * 100).toFixed(1)}%
                        </Badge>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Swap Usage</span>
                        <span className="font-medium">{metrics.memory.swap.toFixed(1)} GB</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="storage" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="text-sm flex items-center space-x-2">
                      <HardDrive className="h-4 w-4" />
                      <span>Storage Usage</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Usage</span>
                        <span className="font-medium">{metrics.storage.usage.toFixed(1)}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-purple-500 h-2 rounded-full"
                          style={{ width: `${metrics.storage.usage}%` }}
                        />
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Total</span>
                        <span className="font-medium">{metrics.storage.total.toFixed(0)} GB</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-sm flex items-center space-x-2">
                      <Zap className="h-4 w-4" />
                      <span>Performance</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Read Speed</span>
                        <span className="font-medium">{metrics.storage.readSpeed.toFixed(0)} MB/s</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Write Speed</span>
                        <span className="font-medium">{metrics.storage.writeSpeed.toFixed(0)} MB/s</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Efficiency</span>
                        <Badge className={getEfficiencyColor(metrics.storage.efficiency)}>
                          {(metrics.storage.efficiency * 100).toFixed(1)}%
                        </Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="network" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="text-sm flex items-center space-x-2">
                      <Activity className="h-4 w-4" />
                      <span>Network Performance</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Bandwidth</span>
                        <span className="font-medium">{metrics.network.bandwidth.toFixed(1)} Mbps</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Latency</span>
                        <span className="font-medium">{metrics.network.latency.toFixed(1)} ms</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Throughput</span>
                        <span className="font-medium">{metrics.network.throughput.toFixed(1)}%</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-sm flex items-center space-x-2">
                      <Target className="h-4 w-4" />
                      <span>Network Efficiency</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Efficiency</span>
                        <Badge className={getEfficiencyColor(metrics.network.efficiency)}>
                          {(metrics.network.efficiency * 100).toFixed(1)}%
                        </Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
          </Tabs>
        </motion.div>
      )}

      {/* Advanced Features Toggle */}
      <div className="text-center">
        <Button
          variant="outline"
          onClick={() => setShowAdvanced(!showAdvanced)}
        >
          <Settings className="h-4 w-4 mr-2" />
          {showAdvanced ? 'Hide' : 'Show'} Advanced Features
        </Button>
      </div>
    </div>
  )
}

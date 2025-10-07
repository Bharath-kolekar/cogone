'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Brain, Zap, Target, TrendingUp, BarChart3, Activity, Settings, Play, Pause, RotateCcw, Gauge, Thermometer, Cpu, MemoryStick } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Slider } from '@/components/ui/slider'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

interface PerformanceMetrics {
  fps: number
  latency: number
  throughput: number
  cpuUsage: number
  memoryUsage: number
  gpuUsage: number
  temperature: number
  powerConsumption: number
  efficiency: number
  quality: number
}

interface OptimizationAlgorithm {
  id: string
  name: string
  description: string
  category: 'cpu' | 'memory' | 'gpu' | 'network' | 'storage'
  priority: 'high' | 'medium' | 'low'
  enabled: boolean
  effectiveness: number
  resourceImpact: number
}

interface AdaptivePerformanceOptimizerProps {
  onOptimizationComplete?: (metrics: PerformanceMetrics) => void
  showRealTimeMetrics?: boolean
  enablePredictiveOptimization?: boolean
  className?: string
}

const OPTIMIZATION_ALGORITHMS: OptimizationAlgorithm[] = [
  {
    id: 'cpu-frequency-scaling',
    name: 'CPU Frequency Scaling',
    description: 'Dynamically adjusts CPU frequency based on workload',
    category: 'cpu',
    priority: 'high',
    enabled: true,
    effectiveness: 0.85,
    resourceImpact: 0.2
  },
  {
    id: 'memory-compression',
    name: 'Memory Compression',
    description: 'Compresses memory pages to reduce usage',
    category: 'memory',
    priority: 'high',
    enabled: true,
    effectiveness: 0.75,
    resourceImpact: 0.3
  },
  {
    id: 'gpu-optimization',
    name: 'GPU Optimization',
    description: 'Optimizes GPU usage for better performance',
    category: 'gpu',
    priority: 'medium',
    enabled: true,
    effectiveness: 0.8,
    resourceImpact: 0.4
  },
  {
    id: 'network-buffering',
    name: 'Network Buffering',
    description: 'Optimizes network buffer sizes for better throughput',
    category: 'network',
    priority: 'medium',
    enabled: true,
    effectiveness: 0.7,
    resourceImpact: 0.1
  },
  {
    id: 'storage-caching',
    name: 'Storage Caching',
    description: 'Implements intelligent storage caching',
    category: 'storage',
    priority: 'low',
    enabled: true,
    effectiveness: 0.65,
    resourceImpact: 0.2
  },
  {
    id: 'predictive-scaling',
    name: 'Predictive Scaling',
    description: 'Predicts resource needs and scales proactively',
    category: 'cpu',
    priority: 'high',
    enabled: true,
    effectiveness: 0.9,
    resourceImpact: 0.1
  },
  {
    id: 'adaptive-quality',
    name: 'Adaptive Quality',
    description: 'Adjusts quality based on available resources',
    category: 'gpu',
    priority: 'medium',
    enabled: true,
    effectiveness: 0.8,
    resourceImpact: 0.3
  },
  {
    id: 'power-management',
    name: 'Power Management',
    description: 'Optimizes power consumption while maintaining performance',
    category: 'cpu',
    priority: 'medium',
    enabled: true,
    effectiveness: 0.75,
    resourceImpact: 0.2
  }
]

export function AdaptivePerformanceOptimizer({
  onOptimizationComplete,
  showRealTimeMetrics = true,
  enablePredictiveOptimization = true,
  className = ''
}: AdaptivePerformanceOptimizerProps) {
  const [metrics, setMetrics] = useState<PerformanceMetrics | null>(null)
  const [algorithms, setAlgorithms] = useState<OptimizationAlgorithm[]>(OPTIMIZATION_ALGORITHMS)
  const [isOptimizing, setIsOptimizing] = useState(false)
  const [optimizationStep, setOptimizationStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [activeTab, setActiveTab] = useState('overview')
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [isMonitoring, setIsMonitoring] = useState(false)
  const [optimizationHistory, setOptimizationHistory] = useState<Array<{timestamp: Date, metrics: PerformanceMetrics}>>([])
  const [selectedAlgorithm, setSelectedAlgorithm] = useState<string | null>(null)
  const monitoringRef = useRef<NodeJS.Timeout | null>(null)
  const optimizationRef = useRef<PerformanceMetrics | null>(null)

  useEffect(() => {
    if (showRealTimeMetrics) {
      startRealTimeMonitoring()
    } else {
      stopRealTimeMonitoring()
    }

    return () => {
      stopRealTimeMonitoring()
    }
  }, [showRealTimeMetrics])

  const startRealTimeMonitoring = useCallback(() => {
    if (monitoringRef.current) return

    setIsMonitoring(true)
    monitoringRef.current = setInterval(() => {
      collectPerformanceMetrics()
    }, 1000)
  }, [])

  const stopRealTimeMonitoring = useCallback(() => {
    if (monitoringRef.current) {
      clearInterval(monitoringRef.current)
      monitoringRef.current = null
    }
    setIsMonitoring(false)
  }, [])

  const collectPerformanceMetrics = async () => {
    try {
      // Simulate advanced performance monitoring
      const mockMetrics: PerformanceMetrics = {
        fps: 30 + Math.random() * 60,
        latency: 1 + Math.random() * 50,
        throughput: Math.random() * 100,
        cpuUsage: Math.random() * 100,
        memoryUsage: Math.random() * 100,
        gpuUsage: Math.random() * 100,
        temperature: 30 + Math.random() * 40,
        powerConsumption: 20 + Math.random() * 80,
        efficiency: 0.6 + Math.random() * 0.4,
        quality: 0.7 + Math.random() * 0.3
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
      console.error('Performance monitoring failed:', error)
    }
  }

  const optimizePerformance = async () => {
    setIsOptimizing(true)
    setProgress(0)
    setOptimizationStep('Initializing adaptive performance optimization...')

    try {
      // Simulate optimization steps
      const steps = [
        'Analyzing current performance metrics...',
        'Identifying optimization opportunities...',
        'Applying CPU optimization algorithms...',
        'Optimizing memory allocation...',
        'Tuning GPU performance...',
        'Enhancing network efficiency...',
        'Implementing storage optimizations...',
        'Applying predictive scaling...',
        'Enabling adaptive quality...',
        'Finalizing performance tuning...'
      ]

      for (let i = 0; i < steps.length; i++) {
        setOptimizationStep(steps[i])
        setProgress((i + 1) * 10)
        await new Promise(resolve => setTimeout(resolve, 300))
      }

      // Apply optimizations
      await applyOptimizations()
      
      // Collect optimized metrics
      await collectPerformanceMetrics()

    } catch (error) {
      console.error('Performance optimization failed:', error)
    } finally {
      setIsOptimizing(false)
      setProgress(100)
      setOptimizationStep('Optimization complete!')
    }
  }

  const applyOptimizations = async () => {
    // Simulate advanced optimization algorithms
    await new Promise(resolve => setTimeout(resolve, 1000))

    // Apply enabled algorithms
    const enabledAlgorithms = algorithms.filter(alg => alg.enabled)
    
    for (const algorithm of enabledAlgorithms) {
      await applyAlgorithm(algorithm)
    }
  }

  const applyAlgorithm = async (algorithm: OptimizationAlgorithm) => {
    // Simulate algorithm application
    console.log(`Applying ${algorithm.name}...`)
    await new Promise(resolve => setTimeout(resolve, 200))
  }

  const toggleAlgorithm = (algorithmId: string) => {
    setAlgorithms(prev => 
      prev.map(alg => 
        alg.id === algorithmId 
          ? { ...alg, enabled: !alg.enabled }
          : alg
      )
    )
  }

  const getPerformanceColor = (value: number, thresholds: {low: number, medium: number}) => {
    if (value < thresholds.low) return 'text-green-600 bg-green-100'
    if (value < thresholds.medium) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  const getEfficiencyColor = (efficiency: number) => {
    if (efficiency > 0.8) return 'text-green-600 bg-green-100'
    if (efficiency > 0.6) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'text-red-600 bg-red-100'
      case 'medium': return 'text-yellow-600 bg-yellow-100'
      default: return 'text-green-600 bg-green-100'
    }
  }

  const getCategoryIcon = (category: string) => {
    const icons = {
      'cpu': Cpu,
      'memory': MemoryStick,
      'gpu': Zap,
      'network': Activity,
      'storage': BarChart3
    }
    return icons[category as keyof typeof icons] || Brain
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <Card className="bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-900/20 dark:to-blue-900/20">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center space-x-2">
                <Brain className="h-6 w-6 text-green-600" />
                <span>Adaptive Performance Optimizer</span>
              </CardTitle>
              <CardDescription>
                Intelligent performance optimization with adaptive algorithms
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
                onClick={optimizePerformance}
                disabled={isOptimizing}
              >
                <Zap className="h-4 w-4 mr-1" />
                Optimize
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {/* Optimization Status */}
          {isOptimizing && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-green-50 dark:bg-green-900/20 rounded-lg p-4"
            >
              <div className="flex items-center space-x-3 mb-3">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-green-600"></div>
                <span className="text-sm font-medium text-green-800 dark:text-green-200">
                  {optimizationStep}
                </span>
              </div>
              <Progress value={progress} className="h-2" />
            </motion.div>
          )}
        </CardContent>
      </Card>

      {/* Performance Metrics */}
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
                    <Gauge className="h-5 w-5 text-blue-600" />
                  </div>
                  <div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">FPS</div>
                    <div className="text-xl font-bold">
                      <Badge className={getPerformanceColor(metrics.fps, {low: 30, medium: 60})}>
                        {metrics.fps.toFixed(0)}
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
                    <TrendingUp className="h-5 w-5 text-green-600" />
                  </div>
                  <div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Latency</div>
                    <div className="text-xl font-bold">
                      <Badge className={getPerformanceColor(metrics.latency, {low: 10, medium: 30})}>
                        {metrics.latency.toFixed(1)}ms
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
                    <Activity className="h-5 w-5 text-purple-600" />
                  </div>
                  <div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Throughput</div>
                    <div className="text-xl font-bold">
                      <Badge className={getPerformanceColor(metrics.throughput, {low: 50, medium: 80})}>
                        {metrics.throughput.toFixed(1)}%
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
                    <Thermometer className="h-5 w-5 text-orange-600" />
                  </div>
                  <div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Temperature</div>
                    <div className="text-xl font-bold">
                      <Badge className={getPerformanceColor(metrics.temperature, {low: 50, medium: 70})}>
                        {metrics.temperature.toFixed(1)}°C
                      </Badge>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Detailed Metrics */}
          <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="overview">Overview</TabsTrigger>
              <TabsTrigger value="algorithms">Algorithms</TabsTrigger>
              <TabsTrigger value="metrics">Metrics</TabsTrigger>
              <TabsTrigger value="history">History</TabsTrigger>
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
                        <span className="text-sm text-gray-600 dark:text-gray-400">Efficiency</span>
                        <Badge className={getEfficiencyColor(metrics.efficiency)}>
                          {(metrics.efficiency * 100).toFixed(1)}%
                        </Badge>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Quality</span>
                        <Badge className={getEfficiencyColor(metrics.quality)}>
                          {(metrics.quality * 100).toFixed(1)}%
                        </Badge>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Power Consumption</span>
                        <span className="font-medium">{metrics.powerConsumption.toFixed(1)}W</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-sm flex items-center space-x-2">
                      <Settings className="h-4 w-4" />
                      <span>Resource Usage</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">CPU Usage</span>
                        <Badge className={getPerformanceColor(metrics.cpuUsage, {low: 50, medium: 80})}>
                          {metrics.cpuUsage.toFixed(1)}%
                        </Badge>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Memory Usage</span>
                        <Badge className={getPerformanceColor(metrics.memoryUsage, {low: 50, medium: 80})}>
                          {metrics.memoryUsage.toFixed(1)}%
                        </Badge>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">GPU Usage</span>
                        <Badge className={getPerformanceColor(metrics.gpuUsage, {low: 50, medium: 80})}>
                          {metrics.gpuUsage.toFixed(1)}%
                        </Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="algorithms" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {algorithms.map((algorithm) => {
                  const Icon = getCategoryIcon(algorithm.category)
                  return (
                    <Card
                      key={algorithm.id}
                      className={`cursor-pointer transition-all ${
                        selectedAlgorithm === algorithm.id ? 'ring-2 ring-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'hover:bg-gray-50 dark:hover:bg-gray-800'
                      }`}
                      onClick={() => setSelectedAlgorithm(selectedAlgorithm === algorithm.id ? null : algorithm.id)}
                    >
                      <CardContent className="p-4">
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center space-x-2">
                            <Icon className="h-4 w-4" />
                            <h3 className="font-medium">{algorithm.name}</h3>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Badge className={getPriorityColor(algorithm.priority)}>
                              {algorithm.priority}
                            </Badge>
                            <Button
                              variant={algorithm.enabled ? 'default' : 'outline'}
                              size="sm"
                              onClick={(e) => {
                                e.stopPropagation()
                                toggleAlgorithm(algorithm.id)
                              }}
                            >
                              {algorithm.enabled ? 'Enabled' : 'Disabled'}
                            </Button>
                          </div>
                        </div>
                        <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                          {algorithm.description}
                        </p>
                        <div className="flex justify-between items-center">
                          <div className="text-xs text-gray-500">
                            Effectiveness: {(algorithm.effectiveness * 100).toFixed(0)}%
                          </div>
                          <div className="text-xs text-gray-500">
                            Impact: {(algorithm.resourceImpact * 100).toFixed(0)}%
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  )
                })}
              </div>
            </TabsContent>

            <TabsContent value="metrics" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="text-sm flex items-center space-x-2">
                      <Gauge className="h-4 w-4" />
                      <span>Performance Metrics</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">FPS</span>
                        <span className="font-medium">{metrics.fps.toFixed(0)}</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-blue-500 h-2 rounded-full"
                          style={{ width: `${Math.min(metrics.fps / 60 * 100, 100)}%` }}
                        />
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Latency</span>
                        <span className="font-medium">{metrics.latency.toFixed(1)}ms</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-green-500 h-2 rounded-full"
                          style={{ width: `${Math.max(0, 100 - metrics.latency / 50 * 100)}%` }}
                        />
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-sm flex items-center space-x-2">
                      <Activity className="h-4 w-4" />
                      <span>Resource Usage</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">CPU</span>
                        <span className="font-medium">{metrics.cpuUsage.toFixed(1)}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-red-500 h-2 rounded-full"
                          style={{ width: `${metrics.cpuUsage}%` }}
                        />
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Memory</span>
                        <span className="font-medium">{metrics.memoryUsage.toFixed(1)}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-yellow-500 h-2 rounded-full"
                          style={{ width: `${metrics.memoryUsage}%` }}
                        />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="history" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle className="text-sm flex items-center space-x-2">
                    <BarChart3 className="h-4 w-4" />
                    <span>Optimization History</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3 max-h-96 overflow-y-auto">
                    {optimizationHistory.slice(0, 20).map((entry, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                        <div className="flex items-center space-x-3">
                          <div className="text-sm font-medium">
                            {entry.timestamp.toLocaleTimeString()}
                          </div>
                          <div className="text-xs text-gray-500">
                            FPS: {entry.metrics.fps.toFixed(0)} | 
                            Latency: {entry.metrics.latency.toFixed(1)}ms | 
                            Efficiency: {(entry.metrics.efficiency * 100).toFixed(1)}%
                          </div>
                        </div>
                        <Badge className={getEfficiencyColor(entry.metrics.efficiency)}>
                          {(entry.metrics.efficiency * 100).toFixed(1)}%
                        </Badge>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
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

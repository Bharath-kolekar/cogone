'use client'

/**
 * 200 Revolutionary Capabilities Dashboard
 * Browse, search, and track all Smart Coding AI capabilities
 */

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

interface Capability {
  id: number
  name: string
  description: string
  category: string
  implemented: boolean
  priority: string
}

interface CategoryStats {
  total: number
  implemented: number
}

interface CapabilityStats {
  total: number
  implemented: number
  pending: number
  implementation_percentage: number
  by_category: Record<string, CategoryStats>
}

export function CapabilitiesDashboard() {
  const [capabilities, setCapabilities] = useState<Capability[]>([])
  const [stats, setStats] = useState<CapabilityStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [filterImplemented, setFilterImplemented] = useState('all')

  useEffect(() => {
    fetchCapabilities()
    fetchStats()
  }, [])

  const fetchCapabilities = async () => {
    try {
      const response = await fetch('/api/v0/ai-capabilities/all')
      const result = await response.json()
      if (result.success) {
        setCapabilities(result.data)
      }
    } catch (error) {
      console.error('Failed to fetch capabilities:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchStats = async () => {
    try {
      const response = await fetch('/api/v0/ai-capabilities/overview')
      const result = await response.json()
      if (result.success) {
        setStats(result.data)
      }
    } catch (error) {
      console.error('Failed to fetch stats:', error)
    }
  }

  const filteredCapabilities = capabilities.filter(cap => {
    const matchesSearch = cap.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         cap.description.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesCategory = selectedCategory === 'all' || cap.category === selectedCategory
    const matchesImplemented = filterImplemented === 'all' ||
                               (filterImplemented === 'implemented' && cap.implemented) ||
                               (filterImplemented === 'pending' && !cap.implemented)
    
    return matchesSearch && matchesCategory && matchesImplemented
  })

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical': return 'destructive'
      case 'high': return 'default'
      case 'medium': return 'secondary'
      case 'low': return 'outline'
      default: return 'outline'
    }
  }

  const getCategoryProgress = (category: string) => {
    if (!stats) return 0
    const catStats = stats.by_category[category]
    if (!catStats || catStats.total === 0) return 0
    return (catStats.implemented / catStats.total) * 100
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading capabilities...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header Stats */}
      {stats && (
        <div className="grid gap-4 md:grid-cols-4">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium">Total Capabilities</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{stats.total}</div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium">Implemented</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-green-600">{stats.implemented}</div>
              <Progress value={stats.implementation_percentage} className="mt-2" />
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium">Pending</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-orange-600">{stats.pending}</div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium">Progress</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{stats.implementation_percentage.toFixed(1)}%</div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Main Dashboard */}
      <Card>
        <CardHeader>
          <CardTitle>200 Revolutionary Capabilities</CardTitle>
          <CardDescription>
            Comprehensive AI-powered coding assistance across 20 categories
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="all" className="space-y-4">
            <TabsList>
              <TabsTrigger value="all">All Capabilities</TabsTrigger>
              <TabsTrigger value="categories">By Category</TabsTrigger>
              <TabsTrigger value="implemented">Implemented</TabsTrigger>
              <TabsTrigger value="pending">Pending</TabsTrigger>
            </TabsList>

            {/* Filters */}
            <div className="flex gap-4">
              <Input
                placeholder="Search capabilities..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="max-w-sm"
              />
              
              <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                <SelectTrigger className="w-[200px]">
                  <SelectValue placeholder="Category" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Categories</SelectItem>
                  <SelectItem value="code_intelligence">Code Intelligence</SelectItem>
                  <SelectItem value="analysis">Analysis</SelectItem>
                  <SelectItem value="debugging">Debugging</SelectItem>
                  <SelectItem value="testing">Testing</SelectItem>
                  <SelectItem value="architecture">Architecture</SelectItem>
                  <SelectItem value="security">Security</SelectItem>
                  <SelectItem value="documentation">Documentation</SelectItem>
                  <SelectItem value="devops">DevOps</SelectItem>
                  <SelectItem value="collaboration">Collaboration</SelectItem>
                  <SelectItem value="legacy_modernization">Legacy Modernization</SelectItem>
                  <SelectItem value="ai_native">AI-Native</SelectItem>
                  <SelectItem value="requirements">Requirements</SelectItem>
                  <SelectItem value="quality_assurance">Quality Assurance</SelectItem>
                  <SelectItem value="data_analytics">Data & Analytics</SelectItem>
                  <SelectItem value="frontend">Frontend</SelectItem>
                  <SelectItem value="backend">Backend</SelectItem>
                  <SelectItem value="mobile">Mobile</SelectItem>
                  <SelectItem value="emerging_tech">Emerging Tech</SelectItem>
                  <SelectItem value="business">Business</SelectItem>
                  <SelectItem value="future_proofing">Future-Proofing</SelectItem>
                </SelectContent>
              </Select>

              <Select value={filterImplemented} onValueChange={setFilterImplemented}>
                <SelectTrigger className="w-[150px]">
                  <SelectValue placeholder="Status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Status</SelectItem>
                  <SelectItem value="implemented">Implemented</SelectItem>
                  <SelectItem value="pending">Pending</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* All Capabilities Tab */}
            <TabsContent value="all" className="space-y-2">
              <div className="text-sm text-muted-foreground mb-2">
                Showing {filteredCapabilities.length} of {capabilities.length} capabilities
              </div>
              
              <div className="grid gap-2 max-h-[600px] overflow-y-auto">
                {filteredCapabilities.map((cap) => (
                  <Card key={cap.id} className={cap.implemented ? 'bg-green-50 dark:bg-green-950' : ''}>
                    <CardHeader className="pb-3">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-2">
                            <CardTitle className="text-base">
                              {cap.id}. {cap.name}
                            </CardTitle>
                            {cap.implemented && (
                              <Badge variant="default" className="bg-green-600">
                                Implemented
                              </Badge>
                            )}
                          </div>
                          <CardDescription className="mt-1">{cap.description}</CardDescription>
                        </div>
                        <div className="flex gap-2">
                          <Badge variant={getPriorityColor(cap.priority) as any}>
                            {cap.priority}
                          </Badge>
                          <Badge variant="outline">
                            {cap.category.replace(/_/g, ' ')}
                          </Badge>
                        </div>
                      </div>
                    </CardHeader>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Categories Tab */}
            <TabsContent value="categories" className="space-y-4">
              {stats && Object.entries(stats.by_category)
                .filter(([_, catStats]) => catStats.total > 0)
                .map(([category, catStats]) => (
                  <Card key={category}>
                    <CardHeader>
                      <div className="flex items-center justify-between">
                        <CardTitle className="text-base capitalize">
                          {category.replace(/_/g, ' ')}
                        </CardTitle>
                        <Badge variant={catStats.implemented === catStats.total ? 'default' : 'secondary'}>
                          {catStats.implemented}/{catStats.total}
                        </Badge>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <Progress value={getCategoryProgress(category)} className="h-2" />
                      <p className="text-sm text-muted-foreground mt-2">
                        {getCategoryProgress(category).toFixed(0)}% complete
                      </p>
                    </CardContent>
                  </Card>
                ))}
            </TabsContent>

            {/* Implemented Tab */}
            <TabsContent value="implemented">
              <div className="grid gap-2 max-h-[600px] overflow-y-auto">
                {capabilities.filter(c => c.implemented).map((cap) => (
                  <Card key={cap.id} className="bg-green-50 dark:bg-green-950">
                    <CardHeader className="pb-3">
                      <div className="flex items-start justify-between">
                        <div>
                          <CardTitle className="text-base">
                            {cap.id}. {cap.name}
                          </CardTitle>
                          <CardDescription className="mt-1">{cap.description}</CardDescription>
                        </div>
                        <Badge variant="outline">
                          {cap.category.replace(/_/g, ' ')}
                        </Badge>
                      </div>
                    </CardHeader>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Pending Tab */}
            <TabsContent value="pending">
              <div className="grid gap-2 max-h-[600px] overflow-y-auto">
                {capabilities.filter(c => !c.implemented).map((cap) => (
                  <Card key={cap.id}>
                    <CardHeader className="pb-3">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <CardTitle className="text-base">
                            {cap.id}. {cap.name}
                          </CardTitle>
                          <CardDescription className="mt-1">{cap.description}</CardDescription>
                        </div>
                        <div className="flex gap-2">
                          <Badge variant={getPriorityColor(cap.priority) as any}>
                            {cap.priority}
                          </Badge>
                          <Badge variant="outline">
                            {cap.category.replace(/_/g, ' ')}
                          </Badge>
                        </div>
                      </div>
                    </CardHeader>
                  </Card>
                ))}
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  )
}


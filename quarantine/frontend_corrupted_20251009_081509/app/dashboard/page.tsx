/**
 * Dashboard Page
 * Main dashboard for authenticated users
 */

'use client'

import { useEffect, useState } from 'react'
import { useAuthContext } from '@/contexts/AuthContext'
import { Navigation } from '@/components/navigation'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Mic, Plus, Download, Eye, Trash2, Clock, CheckCircle, XCircle } from 'lucide-react'
import { motion } from 'framer-motion'
import { apiService } from '@/lib/api'

interface App {
  id: string
  title: string
  description: string
  status: 'generating' | 'completed' | 'failed'
  created_at: string
  preview_url?: string
  download_url?: string
}

export default function DashboardPage() {
  const { user, isAuthenticated, isLoading } = useAuthContext()
  const [apps, setApps] = useState<App[]>([])
  const [isLoadingApps, setIsLoadingApps] = useState(true)

  useEffect(() => {
    if (isAuthenticated) {
      loadApps()
    }
  }, [isAuthenticated])

  const loadApps = async () => {
    try {
      setIsLoadingApps(true)
      const response = await apiService.getApps()
      if (response.success && response.data) {
        // Transform the data to match the App interface
        const transformedApps: App[] = response.data.map((app: any) => ({
          id: app.id,
          title: app.title,
          description: app.description || 'No description available',
          status: app.status,
          created_at: app.created_at,
          preview_url: app.preview_url,
          download_url: app.download_url,
        }))
        setApps(transformedApps)
      }
    } catch (error) {
      console.error('Failed to load apps:', error)
    } finally {
      setIsLoadingApps(false)
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'failed':
        return <XCircle className="h-4 w-4 text-red-500" />
      case 'generating':
        return <Clock className="h-4 w-4 text-yellow-500" />
      default:
        return <Clock className="h-4 w-4 text-gray-500" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400'
      case 'failed':
        return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400'
      case 'generating':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400'
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400'
    }
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Card className="w-full max-w-md">
          <CardHeader className="text-center">
            <CardTitle>Access Denied</CardTitle>
            <CardDescription>
              Please sign in to access your dashboard
            </CardDescription>
          </CardHeader>
          <CardContent className="text-center">
            <Button asChild>
              <a href="/auth">Sign In</a>
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navigation />
      
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Welcome back, {user?.name || user?.email}!
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Manage your voice-generated applications
          </p>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center space-x-2">
                <Mic className="h-5 w-5 text-blue-600" />
                <span>Create New App</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                Use your voice to generate a new application
              </p>
              <Button className="w-full">
                <Mic className="h-4 w-4 mr-2" />
                Start Recording
              </Button>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center space-x-2">
                <Plus className="h-5 w-5 text-green-600" />
                <span>Quick Start</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                Choose from popular app templates
              </p>
              <Button variant="outline" className="w-full">
                Browse Templates
              </Button>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center space-x-2">
                <Download className="h-5 w-5 text-purple-600" />
                <span>Export Apps</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                Download your completed applications
              </p>
              <Button variant="outline" className="w-full">
                View Downloads
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Apps List */}
        <Card>
          <CardHeader>
            <CardTitle>Your Applications</CardTitle>
            <CardDescription>
              Manage and monitor your voice-generated apps
            </CardDescription>
          </CardHeader>
          <CardContent>
            {isLoadingApps ? (
              <div className="flex items-center justify-center py-8">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
              </div>
            ) : apps.length === 0 ? (
              <div className="text-center py-8">
                <Mic className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                  No apps yet
                </h3>
                <p className="text-gray-600 dark:text-gray-400 mb-4">
                  Create your first app using voice commands
                </p>
                <Button>
                  <Mic className="h-4 w-4 mr-2" />
                  Create Your First App
                </Button>
              </div>
            ) : (
              <div className="space-y-4">
                {apps.map((app, index) => (
                  <motion.div
                    key={app.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:shadow-md transition-shadow"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                            {app.title}
                          </h3>
                          <Badge className={getStatusColor(app.status)}>
                            <div className="flex items-center space-x-1">
                              {getStatusIcon(app.status)}
                              <span className="capitalize">{app.status}</span>
                            </div>
                          </Badge>
                        </div>
                        <p className="text-gray-600 dark:text-gray-400 mb-2">
                          {app.description}
                        </p>
                        <p className="text-sm text-gray-500">
                          Created {new Date(app.created_at).toLocaleDateString()}
                        </p>
                      </div>
                      
                      <div className="flex items-center space-x-2">
                        {app.preview_url && (
                          <Button variant="outline" size="sm" asChild>
                            <a href={app.preview_url} target="_blank" rel="noopener noreferrer">
                              <Eye className="h-4 w-4 mr-1" />
                              Preview
                            </a>
                          </Button>
                        )}
                        
                        {app.download_url && (
                          <Button variant="outline" size="sm" asChild>
                            <a href={app.download_url}>
                              <Download className="h-4 w-4 mr-1" />
                              Download
                            </a>
                          </Button>
                        )}
                        
                        <Button variant="outline" size="sm" className="text-red-600 hover:text-red-700">
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Users, CheckCircle, XCircle, AlertTriangle, Shield, Zap, Code, TrendingUp, Loader2 } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { useCodeReview } from '@/hooks/useSmartCodingAI'
import type { CodeReviewResponse } from '@/lib/api'

interface CodeReviewPanelProps {
  code?: string
  onReviewComplete?: (result: CodeReviewResponse) => void
}

export function CodeReviewPanel({ code: initialCode, onReviewComplete }: CodeReviewPanelProps) {
  const [code, setCode] = useState(initialCode || '')
  const { mutate: reviewCode, data: reviewResult, isPending, error } = useCodeReview()

  const handleReview = () => {
    if (!code.trim()) return
    
    reviewCode(
      { code, context: {} },
      {
        onSuccess: (data) => {
          onReviewComplete?.(data)
        },
      }
    )
  }

  const getIssueCount = () => {
    if (!reviewResult) return 0
    return (
      reviewResult.security_issues.length +
      reviewResult.quality_issues.length +
      reviewResult.performance_issues.length +
      reviewResult.architecture_issues.length
    )
  }

  const getStatusColor = () => {
    if (!reviewResult) return 'gray'
    if (reviewResult.passed) return 'green'
    if (reviewResult.consensus_reached) return 'yellow'
    return 'red'
  }

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center space-x-2">
                <Users className="h-5 w-5 text-blue-600" />
                <span>Multi-Agent Code Review</span>
              </CardTitle>
              <CardDescription>
                Get consensus-based review from specialized AI agents
              </CardDescription>
            </div>
            <Button
              onClick={handleReview}
              disabled={isPending || !code.trim()}
              size="sm"
            >
              {isPending ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  Reviewing...
                </>
              ) : (
                'Start Review'
              )}
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          {error && (
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-4">
              <p className="text-red-600 dark:text-red-400 text-sm">{error.message}</p>
            </div>
          )}

          {reviewResult && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-4"
            >
              {/* Review Status */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <Card>
                  <CardContent className="pt-6">
                    <div className="text-center">
                      <div className={`text-2xl font-bold ${
                        reviewResult.passed ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {reviewResult.passed ? <CheckCircle className="h-8 w-8 mx-auto" /> : <XCircle className="h-8 w-8 mx-auto" />}
                      </div>
                      <div className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                        {reviewResult.passed ? 'Passed' : 'Failed'}
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardContent className="pt-6">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-blue-600">
                        {(reviewResult.consensus_score * 100).toFixed(0)}%
                      </div>
                      <div className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                        Consensus
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardContent className="pt-6">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-orange-600">
                        {getIssueCount()}
                      </div>
                      <div className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                        Issues Found
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardContent className="pt-6">
                    <div className="text-center">
                      <Badge variant={reviewResult.passed ? 'default' : 'destructive'}>
                        {reviewResult.overall_rating}
                      </Badge>
                      <div className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                        Rating
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* Issues Tabs */}
              <Tabs defaultValue="security" className="w-full">
                <TabsList className="grid w-full grid-cols-4">
                  <TabsTrigger value="security">
                    <Shield className="h-4 w-4 mr-1" />
                    Security ({reviewResult.security_issues.length})
                  </TabsTrigger>
                  <TabsTrigger value="quality">
                    <CheckCircle className="h-4 w-4 mr-1" />
                    Quality ({reviewResult.quality_issues.length})
                  </TabsTrigger>
                  <TabsTrigger value="performance">
                    <Zap className="h-4 w-4 mr-1" />
                    Performance ({reviewResult.performance_issues.length})
                  </TabsTrigger>
                  <TabsTrigger value="architecture">
                    <Code className="h-4 w-4 mr-1" />
                    Architecture ({reviewResult.architecture_issues.length})
                  </TabsTrigger>
                </TabsList>

                <TabsContent value="security" className="space-y-2 mt-4">
                  {reviewResult.security_issues.length === 0 ? (
                    <div className="text-center py-8 text-gray-500">
                      No security issues found
                    </div>
                  ) : (
                    reviewResult.security_issues.map((issue, idx) => (
                      <Card key={idx} className="border-red-200 dark:border-red-800">
                        <CardContent className="pt-4">
                          <p className="text-sm">{JSON.stringify(issue)}</p>
                        </CardContent>
                      </Card>
                    ))
                  )}
                </TabsContent>

                <TabsContent value="quality" className="space-y-2 mt-4">
                  {reviewResult.quality_issues.length === 0 ? (
                    <div className="text-center py-8 text-gray-500">
                      No quality issues found
                    </div>
                  ) : (
                    reviewResult.quality_issues.map((issue, idx) => (
                      <Card key={idx}>
                        <CardContent className="pt-4">
                          <p className="text-sm">{JSON.stringify(issue)}</p>
                        </CardContent>
                      </Card>
                    ))
                  )}
                </TabsContent>

                <TabsContent value="performance" className="space-y-2 mt-4">
                  {reviewResult.performance_issues.length === 0 ? (
                    <div className="text-center py-8 text-gray-500">
                      No performance issues found
                    </div>
                  ) : (
                    reviewResult.performance_issues.map((issue, idx) => (
                      <Card key={idx}>
                        <CardContent className="pt-4">
                          <p className="text-sm">{JSON.stringify(issue)}</p>
                        </CardContent>
                      </Card>
                    ))
                  )}
                </TabsContent>

                <TabsContent value="architecture" className="space-y-2 mt-4">
                  {reviewResult.architecture_issues.length === 0 ? (
                    <div className="text-center py-8 text-gray-500">
                      No architecture issues found
                    </div>
                  ) : (
                    reviewResult.architecture_issues.map((issue, idx) => (
                      <Card key={idx}>
                        <CardContent className="pt-4">
                          <p className="text-sm">{JSON.stringify(issue)}</p>
                        </CardContent>
                      </Card>
                    ))
                  )}
                </TabsContent>
              </Tabs>

              {/* Recommendations */}
              {reviewResult.recommendations.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Recommendations</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {reviewResult.recommendations.map((rec, idx) => (
                        <li key={idx} className="flex items-start space-x-2">
                          <TrendingUp className="h-4 w-4 text-blue-600 mt-0.5" />
                          <span className="text-sm">{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              )}
            </motion.div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}


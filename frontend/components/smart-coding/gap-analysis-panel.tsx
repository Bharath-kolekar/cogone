'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Search, Wrench, AlertCircle, CheckCircle2, Loader2 } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { useGapDetection, useGapResolution } from '@/hooks/useSmartCodingAI'
import type { GapDetectionResponse, GapResolutionResponse } from '@/lib/api'

interface GapAnalysisPanelProps {
  code?: string
  onGapsResolved?: (result: GapResolutionResponse) => void
}

export function GapAnalysisPanel({ code: initialCode, onGapsResolved }: GapAnalysisPanelProps) {
  const [code, setCode] = useState(initialCode || '')
  const { mutate: detectGaps, data: gapData, isPending: isDetecting } = useGapDetection()
  const { mutate: resolveGaps, data: resolutionData, isPending: isResolving } = useGapResolution()

  const handleDetect = () => {
    if (!code.trim()) return
    detectGaps({ code, context: {} })
  }

  const handleResolve = () => {
    if (!gapData) return
    resolveGaps(
      { code, gaps: gapData.gaps_detected, context: {} },
      { onSuccess: (data) => onGapsResolved?.(data) }
    )
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'destructive'
      case 'warning': return 'default'
      case 'info': return 'secondary'
      default: return 'outline'
    }
  }

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center space-x-2">
                <Search className="h-5 w-5 text-purple-600" />
                <span>Gap Detection & Resolution</span>
              </CardTitle>
              <CardDescription>
                Find and fix gaps in code automatically
              </CardDescription>
            </div>
            <div className="flex space-x-2">
              <Button onClick={handleDetect} disabled={isDetecting || !code.trim()} size="sm">
                {isDetecting ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Detect Gaps'}
              </Button>
              {gapData && gapData.total_gaps > 0 && (
                <Button onClick={handleResolve} disabled={isResolving} size="sm" variant="default">
                  {isResolving ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Resolve Gaps'}
                </Button>
              )}
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {gapData && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4">
              <div className="grid grid-cols-3 gap-4">
                <Card>
                  <CardContent className="pt-6 text-center">
                    <div className="text-2xl font-bold text-orange-600">{gapData.total_gaps}</div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Total Gaps</div>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="pt-6 text-center">
                    <div className="text-2xl font-bold text-red-600">{gapData.critical_gaps}</div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Critical</div>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="pt-6 text-center">
                    <div className="text-2xl font-bold text-yellow-600">{gapData.warnings}</div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Warnings</div>
                  </CardContent>
                </Card>
              </div>

              <div className="space-y-2">
                {gapData.gaps_detected.map((gap: any, idx: number) => (
                  <Card key={idx}>
                    <CardContent className="pt-4">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-2">
                            <Badge variant={getSeverityColor(gap.severity)}>{gap.severity}</Badge>
                            <Badge variant="outline">{gap.type}</Badge>
                          </div>
                          <p className="text-sm font-medium">{gap.message}</p>
                          {gap.suggestion && (
                            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{gap.suggestion}</p>
                          )}
                        </div>
                        <AlertCircle className="h-5 w-5 text-orange-600" />
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>

              {gapData.recommendations.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Recommendations</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-1">
                      {gapData.recommendations.map((rec, idx) => (
                        <li key={idx} className="text-sm">{rec}</li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              )}
            </motion.div>
          )}

          {resolutionData && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-4">
              <Card className="border-green-200 dark:border-green-800">
                <CardHeader>
                  <CardTitle className="text-lg flex items-center space-x-2">
                    <CheckCircle2 className="h-5 w-5 text-green-600" />
                    <span>Resolution Complete</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <p className="text-sm">
                      Resolved {resolutionData.gaps_resolved.length} of {resolutionData.gaps_resolved.length + resolutionData.gaps_unresolved.length} gaps
                    </p>
                    <p className="text-sm font-medium">Resolution Score: {(resolutionData.resolution_score * 100).toFixed(0)}%</p>
                    <div className="mt-4">
                      <p className="text-sm font-medium mb-2">Fixes Applied:</p>
                      <ul className="space-y-1">
                        {resolutionData.fixes_applied.map((fix, idx) => (
                          <li key={idx} className="text-sm text-gray-600 dark:text-gray-400">• {fix}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}


'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Textarea } from '@/components/ui/textarea'
import { Brain, Shield, Search, TrendingUp, Users } from 'lucide-react'
import { CodeReviewPanel } from './code-review-panel'
import { GapAnalysisPanel } from './gap-analysis-panel'
import { AdvancedFeaturesPanel } from './advanced-features-panel'

interface UnifiedAdvancedDashboardProps {
  initialCode?: string
  className?: string
}

export function UnifiedAdvancedDashboard({ initialCode = '', className = '' }: UnifiedAdvancedDashboardProps) {
  const [code, setCode] = useState(initialCode)

  return (
    <div className={`space-y-6 ${className}`}>
      <Card className="bg-gradient-to-r from-blue-50 via-purple-50 to-pink-50 dark:from-blue-900/20 dark:via-purple-900/20 dark:to-pink-900/20">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Brain className="h-6 w-6 text-blue-600" />
            <span>Advanced AI Features</span>
          </CardTitle>
          <CardDescription>
            Multi-agent review, gap detection, 11-validator system, and consciousness-level AI
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium mb-2 block">Code to Analyze</label>
              <Textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder="Paste your code here for analysis..."
                className="min-h-[150px] font-mono text-sm"
              />
            </div>

            <Tabs defaultValue="review" className="w-full">
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="review">
                  <Users className="h-4 w-4 mr-2" />
                  Multi-Agent Review
                </TabsTrigger>
                <TabsTrigger value="gaps">
                  <Search className="h-4 w-4 mr-2" />
                  Gap Analysis
                </TabsTrigger>
                <TabsTrigger value="validation">
                  <Shield className="h-4 w-4 mr-2" />
                  11 Validators
                </TabsTrigger>
              </TabsList>

              <TabsContent value="review" className="mt-4">
                <CodeReviewPanel code={code} />
              </TabsContent>

              <TabsContent value="gaps" className="mt-4">
                <GapAnalysisPanel code={code} />
              </TabsContent>

              <TabsContent value="validation" className="mt-4">
                <AdvancedFeaturesPanel code={code} />
              </TabsContent>
            </Tabs>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}


'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Shield, Brain, ThumbsUp, ThumbsDown, Loader2, CheckCircle2 } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { useComprehensiveValidation, useLearningFeedback } from '@/hooks/useSmartCodingAI'
import type { ComprehensiveValidationResponse } from '@/lib/api'

interface AdvancedFeaturesPanelProps {
  code?: string
  onValidationComplete?: (result: ComprehensiveValidationResponse) => void
}

export function AdvancedFeaturesPanel({ code: initialCode, onValidationComplete }: AdvancedFeaturesPanelProps) {
  const [code, setCode] = useState(initialCode || '')
  const [consciousnessLevel, setConsciousnessLevel] = useState('6')
  const { mutate: validate, data: validationResult, isPending: isValidating } = useComprehensiveValidation()
  const { mutate: submitFeedback } = useLearningFeedback()

  const handleValidate = () => {
    if (!code.trim()) return
    validate(
      { code, context: { consciousness_level: parseInt(consciousnessLevel) } },
      { onSuccess: (data) => onValidationComplete?.(data) }
    )
  }

  const handleFeedback = (accepted: boolean) => {
    submitFeedback({
      completion_id: 'manual_review',
      feedback: { accepted, code, timestamp: new Date().toISOString() }
    })
  }

  const consciousnessLevels = [
    { value: '1', label: 'Basic', description: 'Simple pattern matching' },
    { value: '2', label: 'Aware', description: 'Context awareness' },
    { value: '3', label: 'Reflective', description: 'Self-reflection' },
    { value: '4', label: 'Metacognitive', description: 'Thinking about thinking' },
    { value: '5', label: 'Self-Aware', description: 'Deep understanding' },
    { value: '6', label: 'Transcendent', description: 'Universal patterns' },
  ]

  return (
    <div className="space-y-4">
      {/* Consciousness Level Selector */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Brain className="h-5 w-5 text-purple-600" />
            <span>Consciousness Level</span>
          </CardTitle>
          <CardDescription>Select AI consciousness level for code generation</CardDescription>
        </CardHeader>
        <CardContent>
          <Select value={consciousnessLevel} onValueChange={setConsciousnessLevel}>
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {consciousnessLevels.map((level) => (
                <SelectItem key={level.value} value={level.value}>
                  Level {level.value}: {level.label} - {level.description}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
            Current: <strong>{consciousnessLevels.find(l => l.value === consciousnessLevel)?.label}</strong>
          </p>
        </CardContent>
      </Card>

      {/* 11-Validator Comprehensive Validation */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center space-x-2">
                <Shield className="h-5 w-5 text-green-600" />
                <span>11-Validator Comprehensive Check</span>
              </CardTitle>
              <CardDescription>Multi-layer validation with all validators</CardDescription>
            </div>
            <Button onClick={handleValidate} disabled={isValidating || !code.trim()} size="sm">
              {isValidating ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Validate'}
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          {validationResult && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4">
              <div className="grid grid-cols-3 gap-4">
                <Card>
                  <CardContent className="pt-6 text-center">
                    <div className={`text-2xl font-bold ${validationResult.overall_valid ? 'text-green-600' : 'text-red-600'}`}>
                      {validationResult.overall_valid ? <CheckCircle2 className="h-8 w-8 mx-auto" /> : 'X'}
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                      {validationResult.overall_valid ? 'Valid' : 'Invalid'}
                    </div>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="pt-6 text-center">
                    <div className="text-2xl font-bold text-blue-600">
                      {(validationResult.validation_score * 100).toFixed(0)}%
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400 mt-2">Score</div>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="pt-6 text-center">
                    <div className="text-2xl font-bold text-purple-600">
                      {validationResult.validators_passed}/{validationResult.validators_used}
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400 mt-2">Passed</div>
                  </CardContent>
                </Card>
              </div>

              {validationResult.issues.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Issues ({validationResult.issues.length})</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-1">
                      {validationResult.issues.slice(0, 5).map((issue, idx) => (
                        <li key={idx} className="text-sm text-red-600 dark:text-red-400">• {issue}</li>
                      ))}
                      {validationResult.issues.length > 5 && (
                        <li className="text-sm text-gray-500">... and {validationResult.issues.length - 5} more</li>
                      )}
                    </ul>
                  </CardContent>
                </Card>
              )}

              {validationResult.recommendations.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Recommendations</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-1">
                      {validationResult.recommendations.map((rec, idx) => (
                        <li key={idx} className="text-sm">• {rec}</li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              )}

              {/* Learning Feedback */}
              <Card className="border-blue-200 dark:border-blue-800">
                <CardHeader>
                  <CardTitle className="text-lg">Was this validation helpful?</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex space-x-2">
                    <Button
                      onClick={() => handleFeedback(true)}
                      variant="outline"
                      size="sm"
                    >
                      <ThumbsUp className="h-4 w-4 mr-2" />
                      Yes
                    </Button>
                    <Button
                      onClick={() => handleFeedback(false)}
                      variant="outline"
                      size="sm"
                    >
                      <ThumbsDown className="h-4 w-4 mr-2" />
                      No
                    </Button>
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


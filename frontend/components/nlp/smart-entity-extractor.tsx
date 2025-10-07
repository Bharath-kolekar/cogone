'use client'

import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Search, MapPin, User, Building, Calendar, Tag, Link, Database, Globe, Phone, Mail } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'

interface Entity {
  text: string
  type: string
  category: string
  confidence: number
  start: number
  end: number
  metadata?: {
    description?: string
    url?: string
    phone?: string
    email?: string
    address?: string
    date?: string
    amount?: string
    organization?: string
    person?: string
  }
}

interface EntityExtractionResult {
  entities: Entity[]
  categories: {
    [key: string]: number
  }
  confidence: number
  coverage: number
  suggestions: Array<{
    type: 'missing' | 'uncertain' | 'enhancement'
    message: string
    priority: 'high' | 'medium' | 'low'
  }>
  relationships: Array<{
    source: string
    target: string
    relation: string
    confidence: number
  }>
}

interface SmartEntityExtractorProps {
  text: string
  onExtractionComplete?: (result: EntityExtractionResult) => void
  showRelationships?: boolean
  showSuggestions?: boolean
  enableRealTime?: boolean
  className?: string
}

const ENTITY_TYPES = {
  PERSON: { icon: User, color: 'text-blue-600 bg-blue-100', category: 'People' },
  ORGANIZATION: { icon: Building, color: 'text-green-600 bg-green-100', category: 'Organizations' },
  LOCATION: { icon: MapPin, color: 'text-red-600 bg-red-100', category: 'Places' },
  DATE: { icon: Calendar, color: 'text-purple-600 bg-purple-100', category: 'Time' },
  MONEY: { icon: Tag, color: 'text-yellow-600 bg-yellow-100', category: 'Financial' },
  EMAIL: { icon: Mail, color: 'text-indigo-600 bg-indigo-100', category: 'Contact' },
  PHONE: { icon: Phone, color: 'text-teal-600 bg-teal-100', category: 'Contact' },
  URL: { icon: Link, color: 'text-orange-600 bg-orange-100', category: 'Web' },
  PRODUCT: { icon: Database, color: 'text-pink-600 bg-pink-100', category: 'Products' },
  EVENT: { icon: Calendar, color: 'text-cyan-600 bg-cyan-100', category: 'Events' },
  TECHNOLOGY: { icon: Globe, color: 'text-gray-600 bg-gray-100', category: 'Technology' }
}

export function SmartEntityExtractor({
  text,
  onExtractionComplete,
  showRelationships = true,
  showSuggestions = true,
  enableRealTime = true,
  className = ''
}: SmartEntityExtractorProps) {
  const [result, setResult] = useState<EntityExtractionResult | null>(null)
  const [isExtracting, setIsExtracting] = useState(false)
  const [extractionStep, setExtractionStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [showDetails, setShowDetails] = useState(false)
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const extractionRef = useRef<EntityExtractionResult | null>(null)

  useEffect(() => {
    if (text && enableRealTime) {
      extractEntities(text)
    }
  }, [text, enableRealTime])

  const extractEntities = async (inputText: string) => {
    setIsExtracting(true)
    setProgress(0)
    setExtractionStep('Initializing entity extraction...')

    try {
      // Simulate real-time extraction steps
      const steps = [
        'Analyzing text structure...',
        'Identifying potential entities...',
        'Classifying entity types...',
        'Calculating confidence scores...',
        'Detecting relationships...',
        'Validating entity boundaries...',
        'Enriching with metadata...',
        'Generating suggestions...',
        'Calculating coverage...',
        'Finalizing extraction...'
      ]

      for (let i = 0; i < steps.length; i++) {
        setExtractionStep(steps[i])
        setProgress((i + 1) * 10)
        await new Promise(resolve => setTimeout(resolve, 200))
      }

      // Perform entity extraction
      const extractionResult = await performEntityExtraction(inputText)
      
      setResult(extractionResult)
      extractionRef.current = extractionResult
      onExtractionComplete?.(extractionResult)
      
    } catch (error) {
      console.error('Entity extraction failed:', error)
    } finally {
      setIsExtracting(false)
      setProgress(100)
      setExtractionStep('Extraction complete!')
    }
  }

  const performEntityExtraction = async (inputText: string): Promise<EntityExtractionResult> => {
    // Simulate advanced entity extraction
    await new Promise(resolve => setTimeout(resolve, 1200))

    const entities: Entity[] = []
    const textLower = inputText.toLowerCase()

    // Extract emails
    const emailRegex = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g
    const emails = inputText.match(emailRegex) || []
    emails.forEach(email => {
      entities.push({
        text: email,
        type: 'EMAIL',
        category: 'Contact',
        confidence: 0.95,
        start: inputText.indexOf(email),
        end: inputText.indexOf(email) + email.length,
        metadata: { email }
      })
    })

    // Extract phone numbers
    const phoneRegex = /(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})/g
    const phones = inputText.match(phoneRegex) || []
    phones.forEach(phone => {
      entities.push({
        text: phone,
        type: 'PHONE',
        category: 'Contact',
        confidence: 0.9,
        start: inputText.indexOf(phone),
        end: inputText.indexOf(phone) + phone.length,
        metadata: { phone }
      })
    })

    // Extract URLs
    const urlRegex = /(https?:\/\/[^\s]+)/g
    const urls = inputText.match(urlRegex) || []
    urls.forEach(url => {
      entities.push({
        text: url,
        type: 'URL',
        category: 'Web',
        confidence: 0.95,
        start: inputText.indexOf(url),
        end: inputText.indexOf(url) + url.length,
        metadata: { url }
      })
    })

    // Extract dates
    const dateRegex = /\b(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}|\d{4}[\/\-]\d{1,2}[\/\-]\d{1,2})\b/g
    const dates = inputText.match(dateRegex) || []
    dates.forEach(date => {
      entities.push({
        text: date,
        type: 'DATE',
        category: 'Time',
        confidence: 0.8,
        start: inputText.indexOf(date),
        end: inputText.indexOf(date) + date.length,
        metadata: { date }
      })
    })

    // Extract money amounts
    const moneyRegex = /\$[\d,]+\.?\d*/g
    const amounts = inputText.match(moneyRegex) || []
    amounts.forEach(amount => {
      entities.push({
        text: amount,
        type: 'MONEY',
        category: 'Financial',
        confidence: 0.9,
        start: inputText.indexOf(amount),
        end: inputText.indexOf(amount) + amount.length,
        metadata: { amount }
      })
    })

    // Extract organizations (simple heuristic)
    const orgKeywords = ['inc', 'corp', 'llc', 'ltd', 'company', 'corporation', 'organization', 'association']
    const words = inputText.split(/\s+/)
    words.forEach((word, index) => {
      if (orgKeywords.some(keyword => word.toLowerCase().includes(keyword))) {
        entities.push({
          text: word,
          type: 'ORGANIZATION',
          category: 'Organizations',
          confidence: 0.7,
          start: inputText.indexOf(word),
          end: inputText.indexOf(word) + word.length
        })
      }
    })

    // Extract people (simple heuristic - names with capital letters)
    const nameRegex = /\b[A-Z][a-z]+ [A-Z][a-z]+\b/g
    const names = inputText.match(nameRegex) || []
    names.forEach(name => {
      entities.push({
        text: name,
        type: 'PERSON',
        category: 'People',
        confidence: 0.6,
        start: inputText.indexOf(name),
        end: inputText.indexOf(name) + name.length,
        metadata: { person: name }
      })
    })

    // Calculate categories
    const categories = entities.reduce((acc, entity) => {
      acc[entity.category] = (acc[entity.category] || 0) + 1
      return acc
    }, {} as { [key: string]: number })

    // Generate suggestions
    const suggestions = []
    if (entities.length === 0) {
      suggestions.push({
        type: 'missing' as const,
        message: 'No entities detected. Consider adding more specific information.',
        priority: 'high' as const
      })
    }
    if (entities.filter(e => e.confidence < 0.7).length > 0) {
      suggestions.push({
        type: 'uncertain' as const,
        message: 'Some entities have low confidence. Review and verify.',
        priority: 'medium' as const
      })
    }
    if (entities.length > 0 && entities.length < 3) {
      suggestions.push({
        type: 'enhancement' as const,
        message: 'Consider adding more descriptive information to improve entity detection.',
        priority: 'low' as const
      })
    }

    // Generate relationships (mock)
    const relationships = []
    if (entities.length >= 2) {
      relationships.push({
        source: entities[0].text,
        target: entities[1].text,
        relation: 'associated_with',
        confidence: 0.7
      })
    }

    // Calculate overall metrics
    const confidence = entities.length > 0 ? 
      entities.reduce((sum, e) => sum + e.confidence, 0) / entities.length : 0
    const coverage = entities.length > 0 ? 
      entities.reduce((sum, e) => sum + (e.end - e.start), 0) / inputText.length : 0

    return {
      entities,
      categories,
      confidence,
      coverage,
      suggestions,
      relationships
    }
  }

  const getEntityIcon = (type: string) => {
    const entityType = ENTITY_TYPES[type as keyof typeof ENTITY_TYPES]
    return entityType?.icon || Search
  }

  const getEntityColor = (type: string) => {
    const entityType = ENTITY_TYPES[type as keyof typeof ENTITY_TYPES]
    return entityType?.color || 'text-gray-600 bg-gray-100'
  }

  const getConfidenceColor = (confidence: number) => {
    if (confidence > 0.8) return 'text-green-600 bg-green-100'
    if (confidence > 0.6) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'text-red-600 bg-red-100'
      case 'medium': return 'text-yellow-600 bg-yellow-100'
      default: return 'text-green-600 bg-green-100'
    }
  }

  const filteredEntities = selectedCategory ? 
    result?.entities.filter(e => e.category === selectedCategory) || [] :
    result?.entities || []

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Extraction Status */}
      {isExtracting && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-green-50 dark:bg-green-900/20 rounded-lg p-4"
        >
          <div className="flex items-center space-x-3 mb-3">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-green-600"></div>
            <span className="text-sm font-medium text-green-800 dark:text-green-200">
              {extractionStep}
            </span>
          </div>
          <Progress value={progress} className="h-2" />
        </motion.div>
      )}

      {/* Extraction Results */}
      {result && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Summary */}
          <Card className="bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-900/20 dark:to-blue-900/20">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Search className="h-5 w-5 text-green-600" />
                <span>Entity Extraction Summary</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">{result.entities.length}</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Entities Found</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">{(result.confidence * 100).toFixed(1)}%</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Confidence</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">{(result.coverage * 100).toFixed(1)}%</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Coverage</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-orange-600">{Object.keys(result.categories).length}</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Categories</div>
                </div>
              </div>

              <div className="flex flex-wrap gap-2">
                {Object.entries(result.categories).map(([category, count]) => (
                  <Button
                    key={category}
                    variant={selectedCategory === category ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setSelectedCategory(selectedCategory === category ? null : category)}
                  >
                    {category} ({count})
                  </Button>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Entities List */}
          <Card>
            <CardHeader>
              <CardTitle className="text-sm flex items-center space-x-2">
                <Database className="h-4 w-4" />
                <span>Extracted Entities</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              {filteredEntities.length > 0 ? (
                <div className="space-y-3">
                  {filteredEntities.map((entity, index) => {
                    const Icon = getEntityIcon(entity.type)
                    return (
                      <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                        <div className="flex items-center space-x-3">
                          <Icon className="h-5 w-5 text-gray-500" />
                          <div>
                            <div className="font-medium">{entity.text}</div>
                            <div className="flex items-center space-x-2">
                              <Badge className={getEntityColor(entity.type)}>
                                {entity.type}
                              </Badge>
                              <Badge variant="outline">
                                {entity.category}
                              </Badge>
                            </div>
                          </div>
                        </div>
                        <div className="text-right">
                          <Badge className={getConfidenceColor(entity.confidence)}>
                            {(entity.confidence * 100).toFixed(0)}%
                          </Badge>
                          <div className="text-xs text-gray-500 mt-1">
                            {entity.start}-{entity.end}
                          </div>
                        </div>
                      </div>
                    )
                  })}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-500">
                  No entities found in the selected category.
                </div>
              )}
            </CardContent>
          </Card>

          {/* Relationships */}
          {showRelationships && result.relationships.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Link className="h-4 w-4" />
                  <span>Entity Relationships</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {result.relationships.map((rel, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <div className="font-medium">{rel.source}</div>
                        <div className="text-gray-500">→</div>
                        <div className="font-medium">{rel.target}</div>
                      </div>
                      <div className="text-right">
                        <Badge variant="outline">{rel.relation}</Badge>
                        <div className="text-xs text-gray-500 mt-1">
                          {(rel.confidence * 100).toFixed(0)}% confidence
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Suggestions */}
          {showSuggestions && result.suggestions.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Tag className="h-4 w-4" />
                  <span>Suggestions</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {result.suggestions.map((suggestion, index) => (
                    <div key={index} className="flex items-start space-x-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                      <Badge className={getPriorityColor(suggestion.priority)}>
                        {suggestion.priority}
                      </Badge>
                      <div className="flex-1">
                        <div className="font-medium capitalize">{suggestion.type}</div>
                        <div className="text-sm text-gray-600 dark:text-gray-400">{suggestion.message}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Toggle Details */}
          <div className="text-center">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowDetails(!showDetails)}
            >
              {showDetails ? 'Hide' : 'Show'} Detailed Analysis
            </Button>
          </div>
        </motion.div>
      )}
    </div>
  )
}

/**
 * React Hooks for Smart Coding AI Advanced Features
 */

import { useMutation, useQuery } from '@tanstack/react-query'
import { apiService } from '@/lib/api'
import type {
  CodeReviewRequest,
  CodeReviewResponse,
  LearningFeedbackRequest,
  LearningFeedbackResponse,
  MetaAnalysisRequest,
  MetaAnalysisResponse,
  GapDetectionRequest,
  GapDetectionResponse,
  GapResolutionRequest,
  GapResolutionResponse,
  ComprehensiveValidationRequest,
  ComprehensiveValidationResponse,
} from '@/lib/api'

/**
 * Hook for multi-agent code review
 */
export function useCodeReview() {
  return useMutation<
    CodeReviewResponse,
    Error,
    CodeReviewRequest
  >({
    mutationFn: async (request) => {
      const response = await apiService.reviewCode(request)
      if (!response.success || !response.data) {
        throw new Error(response.error || 'Code review failed')
      }
      return response.data
    },
  })
}

/**
 * Hook for submitting learning feedback
 */
export function useLearningFeedback() {
  return useMutation<
    LearningFeedbackResponse,
    Error,
    LearningFeedbackRequest
  >({
    mutationFn: async (request) => {
      const response = await apiService.submitLearningFeedback(request)
      if (!response.success || !response.data) {
        throw new Error(response.error || 'Learning feedback submission failed')
      }
      return response.data
    },
  })
}

/**
 * Hook for meta-analysis (Layer 3)
 */
export function useMetaAnalysis() {
  return useMutation<
    MetaAnalysisResponse,
    Error,
    MetaAnalysisRequest
  >({
    mutationFn: async (request) => {
      const response = await apiService.getMetaAnalysis(request)
      if (!response.success || !response.data) {
        throw new Error(response.error || 'Meta-analysis failed')
      }
      return response.data
    },
  })
}

/**
 * Hook for gap detection
 */
export function useGapDetection() {
  return useMutation<
    GapDetectionResponse,
    Error,
    GapDetectionRequest
  >({
    mutationFn: async (request) => {
      const response = await apiService.detectGaps(request)
      if (!response.success || !response.data) {
        throw new Error(response.error || 'Gap detection failed')
      }
      return response.data
    },
  })
}

/**
 * Hook for gap resolution
 */
export function useGapResolution() {
  return useMutation<
    GapResolutionResponse,
    Error,
    GapResolutionRequest
  >({
    mutationFn: async (request) => {
      const response = await apiService.resolveGaps(request)
      if (!response.success || !response.data) {
        throw new Error(response.error || 'Gap resolution failed')
      }
      return response.data
    },
  })
}

/**
 * Hook for comprehensive validation (11 validators)
 */
export function useComprehensiveValidation() {
  return useMutation<
    ComprehensiveValidationResponse,
    Error,
    ComprehensiveValidationRequest
  >({
    mutationFn: async (request) => {
      const response = await apiService.validateCodeComprehensive(request)
      if (!response.success || !response.data) {
        throw new Error(response.error || 'Comprehensive validation failed')
      }
      return response.data
    },
  })
}

/**
 * Hook for learning metrics
 */
export function useLearningMetrics() {
  return useQuery({
    queryKey: ['learning-metrics'],
    queryFn: async () => {
      const response = await apiService.getLearningMetrics()
      if (!response.success || !response.data) {
        throw new Error(response.error || 'Failed to fetch learning metrics')
      }
      return response.data
    },
    refetchInterval: 30000, // Refetch every 30 seconds
  })
}

/**
 * Hook for review metrics
 */
export function useReviewMetrics() {
  return useQuery({
    queryKey: ['review-metrics'],
    queryFn: async () => {
      const response = await apiService.getReviewMetrics()
      if (!response.success || !response.data) {
        throw new Error(response.error || 'Failed to fetch review metrics')
      }
      return response.data
    },
    refetchInterval: 30000,
  })
}

/**
 * Hook for gap metrics
 */
export function useGapMetrics() {
  return useQuery({
    queryKey: ['gap-metrics'],
    queryFn: async () => {
      const response = await apiService.getGapMetrics()
      if (!response.success || !response.data) {
        throw new Error(response.error || 'Failed to fetch gap metrics')
      }
      return response.data
    },
    refetchInterval: 30000,
  })
}

/**
 * Hook for metacognition metrics
 */
export function useMetacognitionMetrics() {
  return useQuery({
    queryKey: ['metacognition-metrics'],
    queryFn: async () => {
      const response = await apiService.getMetacognitionMetrics()
      if (!response.success || !response.data) {
        throw new Error(response.error || 'Failed to fetch metacognition metrics')
      }
      return response.data
    },
    refetchInterval: 30000,
  })
}

/**
 * Combined hook for all advanced features
 */
export function useSmartCodingAdvanced() {
  const codeReview = useCodeReview()
  const learningFeedback = useLearningFeedback()
  const metaAnalysis = useMetaAnalysis()
  const gapDetection = useGapDetection()
  const gapResolution = useGapResolution()
  const comprehensiveValidation = useComprehensiveValidation()

  return {
    codeReview,
    learningFeedback,
    metaAnalysis,
    gapDetection,
    gapResolution,
    comprehensiveValidation,
  }
}

/**
 * Combined hook for all metrics
 */
export function useAllMetrics() {
  const learningMetrics = useLearningMetrics()
  const reviewMetrics = useReviewMetrics()
  const gapMetrics = useGapMetrics()
  const metacognitionMetrics = useMetacognitionMetrics()

  return {
    learning: learningMetrics,
    review: reviewMetrics,
    gap: gapMetrics,
    metacognition: metacognitionMetrics,
  }
}


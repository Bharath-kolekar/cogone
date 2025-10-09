/**
 * Seamless Edit Hook
 * Manages the Ctrl+L edit workflow and code change processing
 */

import { useState, useCallback, useRef } from 'react'
import { apiService, CodeChangeRequest, CodeChangeResponse } from '@/lib/api'

interface SeamlessEditState {
  isProcessing: boolean
  selectedText: string
  selectionStart: number
  selectionEnd: number
  changes: Array<{
    id: string
    originalCode: string
    modifiedCode: string
    description: string
    timestamp: Date
    status: 'pending' | 'applied' | 'rejected'
  }>
  error: string | null
  success: string | null
}

interface SeamlessEditActions {
  processEdit: (code: string, description?: string) => Promise<void>
  applyChange: (changeId: string) => void
  rejectChange: (changeId: string) => void
  clearError: () => void
  clearSuccess: () => void
  setSelection: (start: number, end: number, text: string) => void
}

export function useSeamlessEdit(): SeamlessEditState & SeamlessEditActions {
  const [state, setState] = useState<SeamlessEditState>({
    isProcessing: false,
    selectedText: '',
    selectionStart: 0,
    selectionEnd: 0,
    changes: [],
    error: null,
    success: null,
  })

  const processEdit = useCallback(async (code: string, description?: string): Promise<void> => {
    if (!code.trim()) {
      setState(prev => ({ ...prev, error: 'Please select some code to edit' }))
      return
    }

    setState(prev => ({ ...prev, isProcessing: true, error: null, success: null }))

    try {
      const response = await apiService.processCodeChange({
        code,
        language: 'javascript', // Default language, can be made configurable
        description: description || 'User requested edit via Ctrl+L'
      })

      if (response.success && response.data) {
        const change = {
          id: Date.now().toString(),
          originalCode: code,
          modifiedCode: response.data.modifiedCode,
          description: response.data.description,
          timestamp: new Date(),
          status: 'pending' as const
        }

        setState(prev => ({
          ...prev,
          changes: [change, ...prev.changes],
          isProcessing: false,
          success: 'Code modification ready! Review and apply if satisfied.'
        }))
      } else {
        throw new Error(response.error || 'Failed to process code change')
      }
    } catch (error) {
      setState(prev => ({
        ...prev,
        isProcessing: false,
        error: error instanceof Error ? error.message : 'Failed to process code change'
      }))
    }
  }, [])

  const applyChange = useCallback((changeId: string) => {
    setState(prev => ({
      ...prev,
      changes: prev.changes.map(change => 
        change.id === changeId 
          ? { ...change, status: 'applied' as const }
          : change
      ),
      success: 'Code change applied successfully!'
    }))
  }, [])

  const rejectChange = useCallback((changeId: string) => {
    setState(prev => ({
      ...prev,
      changes: prev.changes.map(change => 
        change.id === changeId 
          ? { ...change, status: 'rejected' as const }
          : change
      )
    }))
  }, [])

  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }))
  }, [])

  const clearSuccess = useCallback(() => {
    setState(prev => ({ ...prev, success: null }))
  }, [])

  const setSelection = useCallback((start: number, end: number, text: string) => {
    setState(prev => ({
      ...prev,
      selectionStart: start,
      selectionEnd: end,
      selectedText: text
    }))
  }, [])

  return {
    ...state,
    processEdit,
    applyChange,
    rejectChange,
    clearError,
    clearSuccess,
    setSelection,
  }
}

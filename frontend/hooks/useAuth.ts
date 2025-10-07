/**
 * Authentication Hook
 * Manages user authentication state and operations
 */

import { useState, useEffect, useCallback } from 'react'
import { apiService, UserProfile } from '@/lib/api'

interface AuthState {
  user: UserProfile | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
}

interface AuthActions {
  login: (email: string, password: string) => Promise<boolean>
  register: (email: string, password: string, name?: string) => Promise<boolean>
  logout: () => void
  updateProfile: (updates: Partial<UserProfile>) => Promise<boolean>
  refreshProfile: () => Promise<void>
}

export function useAuth(): AuthState & AuthActions {
  const [state, setState] = useState<AuthState>({
    user: null,
    isAuthenticated: false,
    isLoading: true,
    error: null,
  })

  // Initialize auth state on mount
  useEffect(() => {
    const initAuth = async () => {
      if (apiService.isAuthenticated()) {
        try {
          const response = await apiService.getProfile()
          if (response.success && response.data) {
            setState({
              user: response.data,
              isAuthenticated: true,
              isLoading: false,
              error: null,
            })
          } else {
            // Token is invalid, clear it
            apiService.setToken(null)
            setState({
              user: null,
              isAuthenticated: false,
              isLoading: false,
              error: null,
            })
          }
        } catch (error) {
          apiService.setToken(null)
          setState({
            user: null,
            isAuthenticated: false,
            isLoading: false,
            error: null,
          })
        }
      } else {
        setState({
          user: null,
          isAuthenticated: false,
          isLoading: false,
          error: null,
        })
      }
    }

    initAuth()
  }, [])

  const login = useCallback(async (email: string, password: string): Promise<boolean> => {
    setState(prev => ({ ...prev, isLoading: true, error: null }))

    try {
      const response = await apiService.login(email, password)
      
      if (response.success && response.data) {
        apiService.setToken(response.data.access_token)
        setState({
          user: response.data.user,
          isAuthenticated: true,
          isLoading: false,
          error: null,
        })
        return true
      } else {
        setState(prev => ({
          ...prev,
          isLoading: false,
          error: response.error || 'Login failed',
        }))
        return false
      }
    } catch (error) {
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Login failed',
      }))
      return false
    }
  }, [])

  const register = useCallback(async (email: string, password: string, name?: string): Promise<boolean> => {
    setState(prev => ({ ...prev, isLoading: true, error: null }))

    try {
      const response = await apiService.register(email, password, name)
      
      if (response.success && response.data) {
        apiService.setToken(response.data.access_token)
        setState({
          user: response.data.user,
          isAuthenticated: true,
          isLoading: false,
          error: null,
        })
        return true
      } else {
        setState(prev => ({
          ...prev,
          isLoading: false,
          error: response.error || 'Registration failed',
        }))
        return false
      }
    } catch (error) {
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Registration failed',
      }))
      return false
    }
  }, [])

  const logout = useCallback(() => {
    apiService.setToken(null)
    setState({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,
    })
  }, [])

  const updateProfile = useCallback(async (updates: Partial<UserProfile>): Promise<boolean> => {
    setState(prev => ({ ...prev, isLoading: true, error: null }))

    try {
      const response = await apiService.updateProfile(updates)
      
      if (response.success && response.data) {
        setState(prev => ({
          ...prev,
          user: response.data || null,
          isLoading: false,
          error: null,
        }))
        return true
      } else {
        setState(prev => ({
          ...prev,
          isLoading: false,
          error: response.error || 'Profile update failed',
        }))
        return false
      }
    } catch (error) {
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Profile update failed',
      }))
      return false
    }
  }, [])

  const refreshProfile = useCallback(async (): Promise<void> => {
    if (!apiService.isAuthenticated()) return

    try {
      const response = await apiService.getProfile()
      if (response.success && response.data) {
        setState(prev => ({
          ...prev,
          user: response.data || null,
          error: null,
        }))
      } else {
        // Token is invalid, logout
        logout()
      }
    } catch (error) {
      // Network error, keep current state
      console.warn('Failed to refresh profile:', error)
    }
  }, [logout])

  return {
    ...state,
    login,
    register,
    logout,
    updateProfile,
    refreshProfile,
  }
}

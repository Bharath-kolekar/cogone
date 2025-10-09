'use client'

import { useEffect, useRef, useState } from 'react'

interface PerformanceOptimizerProps {
  children: React.ReactNode
  enableParticles?: boolean
  enableNeural?: boolean
  enableAnimations?: boolean
  maxFPS?: number
  quality?: 'low' | 'medium' | 'high'
}

export function PerformanceOptimizer({
  children,
  enableParticles = true,
  enableNeural = true,
  enableAnimations = true,
  maxFPS = 60,
  quality = 'medium'
}: PerformanceOptimizerProps) {
  const [isLowPerformance, setIsLowPerformance] = useState(false)
  const [fps, setFps] = useState(60)
  const frameCountRef = useRef(0)
  const lastTimeRef = useRef(performance.now())
  const animationRef = useRef<number>()

  useEffect(() => {
    const measureFPS = () => {
      const now = performance.now()
      frameCountRef.current++

      if (now - lastTimeRef.current >= 1000) {
        const currentFPS = Math.round((frameCountRef.current * 1000) / (now - lastTimeRef.current))
        setFps(currentFPS)
        
        // Adjust performance based on FPS
        if (currentFPS < 30) {
          setIsLowPerformance(true)
        } else if (currentFPS > 50) {
          setIsLowPerformance(false)
        }

        frameCountRef.current = 0
        lastTimeRef.current = now
      }

      animationRef.current = requestAnimationFrame(measureFPS)
    }

    animationRef.current = requestAnimationFrame(measureFPS)

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current)
      }
    }
  }, [])

  // Adjust quality based on performance
  const adjustedQuality = isLowPerformance ? 'low' : quality
  const shouldEnableParticles = enableParticles && !isLowPerformance
  const shouldEnableNeural = enableNeural && adjustedQuality !== 'low'
  const shouldEnableAnimations = enableAnimations && fps > 30

  return (
    <div 
      className="performance-optimizer"
      data-fps={fps}
      data-quality={adjustedQuality}
      data-particles={shouldEnableParticles}
      data-neural={shouldEnableNeural}
      data-animations={shouldEnableAnimations}
    >
      {children}
    </div>
  )
}

// Hook for performance-aware animations
export function usePerformanceAwareAnimation() {
  const [shouldAnimate, setShouldAnimate] = useState(true)
  const [fps, setFps] = useState(60)

  useEffect(() => {
    let frameCount = 0
    let lastTime = performance.now()

    const measureFPS = () => {
      const now = performance.now()
      frameCount++

      if (now - lastTime >= 1000) {
        const currentFPS = Math.round((frameCount * 1000) / (now - lastTime))
        setFps(currentFPS)
        
        // Disable animations if FPS is too low
        setShouldAnimate(currentFPS > 30)
        
        frameCount = 0
        lastTime = now
      }

      requestAnimationFrame(measureFPS)
    }

    requestAnimationFrame(measureFPS)
  }, [])

  return { shouldAnimate, fps }
}

// Lazy loading component for heavy VFX
export function LazyVFX({ 
  children, 
  threshold = 0.1,
  rootMargin = '50px'
}: {
  children: React.ReactNode
  threshold?: number
  rootMargin?: string
}) {
  const [isVisible, setIsVisible] = useState(false)
  const [hasLoaded, setHasLoaded] = useState(false)
  const elementRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !hasLoaded) {
          setIsVisible(true)
          setHasLoaded(true)
        }
      },
      { threshold, rootMargin }
    )

    if (elementRef.current) {
      observer.observe(elementRef.current)
    }

    return () => observer.disconnect()
  }, [threshold, rootMargin, hasLoaded])

  return (
    <div ref={elementRef} className="lazy-vfx">
      {isVisible ? children : (
        <div className="w-full h-full bg-gray-100 dark:bg-gray-800 animate-pulse rounded" />
      )}
    </div>
  )
}

// Memory management for VFX components
export function useVFXMemoryManager() {
  const [memoryUsage, setMemoryUsage] = useState(0)
  const [isLowMemory, setIsLowMemory] = useState(false)

  useEffect(() => {
    const checkMemory = () => {
      if ('memory' in performance) {
        const memory = (performance as any).memory
        const usedMB = memory.usedJSHeapSize / 1024 / 1024
        setMemoryUsage(usedMB)
        
        // Consider low memory if usage is over 100MB
        setIsLowMemory(usedMB > 100)
      }
    }

    const interval = setInterval(checkMemory, 5000)
    checkMemory()

    return () => clearInterval(interval)
  }, [])

  return { memoryUsage, isLowMemory }
}

// Adaptive quality based on device capabilities
export function useAdaptiveQuality() {
  const [quality, setQuality] = useState<'low' | 'medium' | 'high'>('medium')

  useEffect(() => {
    const checkDeviceCapabilities = () => {
      // Check for high DPI displays
      const isHighDPI = window.devicePixelRatio > 2
      
      // Check for hardware acceleration
      const canvas = document.createElement('canvas')
      const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl')
      const hasWebGL = !!gl
      
      // Check for reduced motion preference
      const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
      
      if (prefersReducedMotion) {
        setQuality('low')
      } else if (isHighDPI && hasWebGL) {
        setQuality('high')
      } else if (hasWebGL) {
        setQuality('medium')
      } else {
        setQuality('low')
      }
    }

    checkDeviceCapabilities()
    
    // Listen for changes in reduced motion preference
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)')
    const handleChange = () => checkDeviceCapabilities()
    mediaQuery.addEventListener('change', handleChange)

    return () => mediaQuery.removeEventListener('change', handleChange)
  }, [])

  return quality
}

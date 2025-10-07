'use client'

import { useEffect, useRef, useState } from 'react'
import { motion } from 'framer-motion'

interface VoiceVisualizerProps {
  isRecording: boolean
  audioLevel?: number
  className?: string
}

export function VoiceVisualizer({ 
  isRecording, 
  audioLevel = 0,
  className = ''
}: VoiceVisualizerProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const animationRef = useRef<number>()

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const resizeCanvas = () => {
      const rect = canvas.getBoundingClientRect()
      canvas.width = rect.width
      canvas.height = rect.height
    }

    resizeCanvas()
    window.addEventListener('resize', resizeCanvas)

    const bars = 32
    const barWidth = canvas.width / bars
    const barHeights = new Array(bars).fill(0)

    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      if (isRecording) {
        // Update bar heights based on audio level
        for (let i = 0; i < bars; i++) {
          const targetHeight = (Math.random() * audioLevel + 0.1) * canvas.height
          barHeights[i] += (targetHeight - barHeights[i]) * 0.1
        }

        // Draw bars
        for (let i = 0; i < bars; i++) {
          const x = i * barWidth
          const height = barHeights[i]
          const y = canvas.height - height

          // Create gradient
          const gradient = ctx.createLinearGradient(0, y, 0, canvas.height)
          gradient.addColorStop(0, '#3b82f6')
          gradient.addColorStop(0.5, '#8b5cf6')
          gradient.addColorStop(1, '#06b6d4')

          ctx.fillStyle = gradient
          ctx.fillRect(x, y, barWidth - 2, height)
        }
      } else {
        // Fade out bars when not recording
        for (let i = 0; i < bars; i++) {
          barHeights[i] *= 0.9
          if (barHeights[i] > 1) {
            const x = i * barWidth
            const height = barHeights[i]
            const y = canvas.height - height

            ctx.fillStyle = `rgba(59, 130, 246, ${barHeights[i] / canvas.height})`
            ctx.fillRect(x, y, barWidth - 2, height)
          }
        }
      }

      animationRef.current = requestAnimationFrame(draw)
    }

    draw()

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current)
      }
      window.removeEventListener('resize', resizeCanvas)
    }
  }, [isRecording, audioLevel])

  return (
    <canvas
      ref={canvasRef}
      className={`w-full h-full ${className}`}
    />
  )
}

// Circular Voice Visualizer
export function CircularVoiceVisualizer({ 
  isRecording, 
  audioLevel = 0,
  size = 200,
  className = ''
}: VoiceVisualizerProps & { size?: number }) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const animationRef = useRef<number>()

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    canvas.width = size
    canvas.height = size

    const centerX = size / 2
    const centerY = size / 2
    const radius = size / 3
    const bars = 64

    const draw = () => {
      ctx.clearRect(0, 0, size, size)

      if (isRecording) {
        for (let i = 0; i < bars; i++) {
          const angle = (i / bars) * Math.PI * 2
          const barHeight = (Math.random() * audioLevel + 0.1) * radius * 0.8
          
          const x1 = centerX + Math.cos(angle) * radius
          const y1 = centerY + Math.sin(angle) * radius
          const x2 = centerX + Math.cos(angle) * (radius + barHeight)
          const y2 = centerY + Math.sin(angle) * (radius + barHeight)

          // Create gradient
          const gradient = ctx.createLinearGradient(x1, y1, x2, y2)
          gradient.addColorStop(0, '#3b82f6')
          gradient.addColorStop(1, '#8b5cf6')

          ctx.strokeStyle = gradient
          ctx.lineWidth = 3
          ctx.beginPath()
          ctx.moveTo(x1, y1)
          ctx.lineTo(x2, y2)
          ctx.stroke()
        }
      }

      animationRef.current = requestAnimationFrame(draw)
    }

    draw()

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current)
      }
    }
  }, [isRecording, audioLevel, size])

  return (
    <canvas
      ref={canvasRef}
      className={`${className}`}
    />
  )
}

// Waveform Visualizer
export function WaveformVisualizer({ 
  isRecording, 
  audioLevel = 0,
  className = ''
}: VoiceVisualizerProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const animationRef = useRef<number>()

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const resizeCanvas = () => {
      const rect = canvas.getBoundingClientRect()
      canvas.width = rect.width
      canvas.height = rect.height
    }

    resizeCanvas()
    window.addEventListener('resize', resizeCanvas)

    const points: number[] = []
    const maxPoints = 200

    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      if (isRecording) {
        // Add new point
        const newPoint = (Math.random() - 0.5) * audioLevel * canvas.height * 0.5
        points.push(newPoint)

        if (points.length > maxPoints) {
          points.shift()
        }

        // Draw waveform
        ctx.strokeStyle = '#3b82f6'
        ctx.lineWidth = 2
        ctx.beginPath()

        for (let i = 0; i < points.length; i++) {
          const x = (i / (maxPoints - 1)) * canvas.width
          const y = canvas.height / 2 + points[i]

          if (i === 0) {
            ctx.moveTo(x, y)
          } else {
            ctx.lineTo(x, y)
          }
        }

        ctx.stroke()

        // Draw mirror waveform
        ctx.strokeStyle = '#8b5cf6'
        ctx.lineWidth = 1
        ctx.beginPath()

        for (let i = 0; i < points.length; i++) {
          const x = (i / (maxPoints - 1)) * canvas.width
          const y = canvas.height / 2 - points[i]

          if (i === 0) {
            ctx.moveTo(x, y)
          } else {
            ctx.lineTo(x, y)
          }
        }

        ctx.stroke()
      } else {
        // Fade out points
        for (let i = 0; i < points.length; i++) {
          points[i] *= 0.95
        }

        if (points.length > 0 && Math.abs(points[points.length - 1]) < 0.1) {
          points.shift()
        }

        if (points.length > 0) {
          ctx.strokeStyle = '#3b82f6'
          ctx.lineWidth = 2
          ctx.beginPath()

          for (let i = 0; i < points.length; i++) {
            const x = (i / (maxPoints - 1)) * canvas.width
            const y = canvas.height / 2 + points[i]

            if (i === 0) {
              ctx.moveTo(x, y)
            } else {
              ctx.lineTo(x, y)
            }
          }

          ctx.stroke()
        }
      }

      animationRef.current = requestAnimationFrame(draw)
    }

    draw()

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current)
      }
      window.removeEventListener('resize', resizeCanvas)
    }
  }, [isRecording, audioLevel])

  return (
    <canvas
      ref={canvasRef}
      className={`w-full h-full ${className}`}
    />
  )
}

// Voice Pulse Effect
export function VoicePulse({ 
  isRecording, 
  audioLevel = 0,
  className = ''
}: VoiceVisualizerProps) {
  return (
    <motion.div
      className={`relative ${className}`}
      animate={isRecording ? {
        scale: [1, 1 + audioLevel * 0.2, 1],
        opacity: [0.8, 1, 0.8]
      } : {}}
      transition={{
        duration: 0.1,
        repeat: Infinity,
        ease: 'easeInOut'
      }}
    >
      <motion.div
        className="absolute inset-0 rounded-full border-2 border-blue-500"
        animate={isRecording ? {
          scale: [1, 1.5, 1],
          opacity: [1, 0, 1]
        } : {}}
        transition={{
          duration: 0.5,
          repeat: Infinity,
          ease: 'easeOut'
        }}
      />
      <motion.div
        className="absolute inset-0 rounded-full border border-blue-400"
        animate={isRecording ? {
          scale: [1, 1.2, 1],
          opacity: [1, 0, 1]
        } : {}}
        transition={{
          duration: 0.3,
          repeat: Infinity,
          ease: 'easeOut',
          delay: 0.1
        }}
      />
    </motion.div>
  )
}

'use client'

import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence, useAnimation } from 'framer-motion'

// Holographic Effect Component
export function HolographicEffect({ 
  children, 
  intensity = 1,
  className = ''
}: {
  children: React.ReactNode
  intensity?: number
  className?: string
}) {
  return (
    <motion.div
      className={`relative ${className}`}
      style={{
        background: `
          linear-gradient(45deg, 
            transparent 30%, 
            rgba(59, 130, 246, 0.1) 50%, 
            transparent 70%
          ),
          linear-gradient(-45deg, 
            transparent 30%, 
            rgba(139, 92, 246, 0.1) 50%, 
            transparent 70%
          )
        `,
        backgroundSize: '20px 20px',
        animation: 'holographic 3s linear infinite'
      }}
    >
      <style jsx>{`
        @keyframes holographic {
          0% { background-position: 0 0, 0 0; }
          100% { background-position: 20px 20px, -20px 20px; }
        }
      `}</style>
      {children}
    </motion.div>
  )
}

// Morphing Shape Component
export function MorphingShape({ 
  shapes = ['circle', 'square', 'triangle'],
  duration = 3,
  size = 100,
  color = '#3b82f6',
  className = ''
}: {
  shapes?: string[]
  duration?: number
  size?: number
  color?: string
  className?: string
}) {
  const [currentShape, setCurrentShape] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentShape(prev => (prev + 1) % shapes.length)
    }, duration * 1000)

    return () => clearInterval(interval)
  }, [shapes.length, duration])

  const getShapePath = (shape: string) => {
    const halfSize = size / 2
    switch (shape) {
      case 'circle':
        return `M ${halfSize} 0 A ${halfSize} ${halfSize} 0 1 1 ${halfSize - 0.1} 0`
      case 'square':
        return `M 0 0 L ${size} 0 L ${size} ${size} L 0 ${size} Z`
      case 'triangle':
        return `M ${halfSize} 0 L ${size} ${size} L 0 ${size} Z`
      default:
        return `M ${halfSize} 0 A ${halfSize} ${halfSize} 0 1 1 ${halfSize - 0.1} 0`
    }
  }

  return (
    <div className={`relative ${className}`} style={{ width: size, height: size }}>
      <motion.svg
        width={size}
        height={size}
        viewBox={`0 0 ${size} ${size}`}
        className="absolute inset-0"
      >
        <motion.path
          d={getShapePath(shapes[currentShape])}
          fill={color}
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 0.5 }}
        />
      </motion.svg>
    </div>
  )
}

// Liquid Blob Animation
export function LiquidBlob({ 
  size = 200,
  color = '#3b82f6',
  className = ''
}: {
  size?: number
  color?: string
  className?: string
}) {
  const [path, setPath] = useState('')

  useEffect(() => {
    const generateBlobPath = () => {
      const points = 8
      const radius = size / 2
      const centerX = size / 2
      const centerY = size / 2
      
      let path = 'M'
      
      for (let i = 0; i < points; i++) {
        const angle = (i / points) * Math.PI * 2
        const variation = 0.3 + Math.random() * 0.4
        const x = centerX + Math.cos(angle) * radius * variation
        const y = centerY + Math.sin(angle) * radius * variation
        
        if (i === 0) {
          path += ` ${x} ${y}`
        } else {
          path += ` L ${x} ${y}`
        }
      }
      
      path += ' Z'
      return path
    }

    const updatePath = () => {
      setPath(generateBlobPath())
    }

    updatePath()
    const interval = setInterval(updatePath, 2000)

    return () => clearInterval(interval)
  }, [size])

  return (
    <div className={`relative ${className}`} style={{ width: size, height: size }}>
      <motion.svg
        width={size}
        height={size}
        viewBox={`0 0 ${size} ${size}`}
        className="absolute inset-0"
      >
        <motion.path
          d={path}
          fill={color}
          animate={{
            d: path
          }}
          transition={{
            duration: 2,
            ease: 'easeInOut',
            repeat: Infinity,
            repeatType: 'reverse'
          }}
        />
      </motion.svg>
    </div>
  )
}

// Matrix Rain Effect
export function MatrixRain({ 
  characters = '01',
  speed = 50,
  className = ''
}: {
  characters?: string
  speed?: number
  className?: string
}) {
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

    const columns = Math.floor(canvas.width / 20)
    const drops: number[] = new Array(columns).fill(0)

    const draw = () => {
      ctx.fillStyle = 'rgba(0, 0, 0, 0.05)'
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      ctx.fillStyle = '#0f0'
      ctx.font = '15px monospace'

      for (let i = 0; i < drops.length; i++) {
        const char = characters[Math.floor(Math.random() * characters.length)]
        ctx.fillText(char, i * 20, drops[i] * 20)

        if (drops[i] * 20 > canvas.height && Math.random() > 0.975) {
          drops[i] = 0
        }
        drops[i]++
      }
    }

    const animate = () => {
      draw()
      animationRef.current = requestAnimationFrame(animate)
    }

    animate()

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current)
      }
      window.removeEventListener('resize', resizeCanvas)
    }
  }, [characters])

  return (
    <canvas
      ref={canvasRef}
      className={`absolute inset-0 pointer-events-none ${className}`}
      style={{ zIndex: 1 }}
    />
  )
}

// Glitch Effect
export function GlitchEffect({ 
  children, 
  intensity = 1,
  className = ''
}: {
  children: React.ReactNode
  intensity?: number
  className?: string
}) {
  const [isGlitching, setIsGlitching] = useState(false)

  useEffect(() => {
    const interval = setInterval(() => {
      if (Math.random() < 0.1 * intensity) {
        setIsGlitching(true)
        setTimeout(() => setIsGlitching(false), 100)
      }
    }, 1000)

    return () => clearInterval(interval)
  }, [intensity])

  return (
    <motion.div
      className={`relative ${className}`}
      animate={isGlitching ? {
        x: [0, -2, 2, -1, 1, 0],
        y: [0, 1, -1, 0.5, -0.5, 0],
        filter: [
          'hue-rotate(0deg)',
          'hue-rotate(90deg)',
          'hue-rotate(180deg)',
          'hue-rotate(270deg)',
          'hue-rotate(360deg)'
        ]
      } : {}}
      transition={{ duration: 0.1 }}
    >
      {children}
    </motion.div>
  )
}

// Floating Elements
export function FloatingElements({ 
  count = 10,
  className = ''
}: {
  count?: number
  className?: string
}) {
  const elements = Array.from({ length: count }, (_, i) => ({
    id: i,
    x: Math.random() * 100,
    y: Math.random() * 100,
    size: Math.random() * 20 + 10,
    color: `hsl(${Math.random() * 360}, 70%, 60%)`,
    delay: Math.random() * 2
  }))

  return (
    <div className={`absolute inset-0 pointer-events-none ${className}`}>
      {elements.map((element) => (
        <motion.div
          key={element.id}
          className="absolute rounded-full opacity-60"
          style={{
            left: `${element.x}%`,
            top: `${element.y}%`,
            width: element.size,
            height: element.size,
            backgroundColor: element.color
          }}
          animate={{
            y: [0, -20, 0],
            x: [0, 10, 0],
            scale: [1, 1.1, 1],
            opacity: [0.6, 1, 0.6]
          }}
          transition={{
            duration: 3,
            delay: element.delay,
            repeat: Infinity,
            ease: 'easeInOut'
          }}
        />
      ))}
    </div>
  )
}

// Energy Field
export function EnergyField({ 
  intensity = 1,
  color = '#3b82f6',
  className = ''
}: {
  intensity?: number
  color?: string
  className?: string
}) {
  return (
    <div className={`relative ${className}`}>
      <motion.div
        className="absolute inset-0 rounded-full"
        style={{
          background: `radial-gradient(circle, ${color}20 0%, transparent 70%)`,
          filter: 'blur(20px)'
        }}
        animate={{
          scale: [1, 1.2, 1],
          opacity: [0.3, 0.8, 0.3]
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
          ease: 'easeInOut'
        }}
      />
      <motion.div
        className="absolute inset-0 rounded-full border"
        style={{
          borderColor: color,
          borderWidth: '1px'
        }}
        animate={{
          scale: [1, 1.1, 1],
          opacity: [0.5, 1, 0.5]
        }}
        transition={{
          duration: 1.5,
          repeat: Infinity,
          ease: 'easeInOut',
          delay: 0.5
        }}
      />
    </div>
  )
}

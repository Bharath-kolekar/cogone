'use client'

import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Brain, Zap, Cpu, Network } from 'lucide-react'

interface NeuralNodeProps {
  x: number
  y: number
  size: number
  intensity: number
  color: string
  delay?: number
}

function NeuralNode({ x, y, size, intensity, color, delay = 0 }: NeuralNodeProps) {
  return (
    <motion.div
      initial={{ scale: 0, opacity: 0 }}
      animate={{ 
        scale: [0, 1, 1.2, 1],
        opacity: [0, 1, 0.8, 1]
      }}
      transition={{
        duration: 2,
        delay,
        repeat: Infinity,
        repeatType: 'reverse'
      }}
      className="absolute rounded-full"
      style={{
        left: x,
        top: y,
        width: size,
        height: size,
        background: `radial-gradient(circle, ${color} 0%, transparent 70%)`,
        boxShadow: `0 0 ${size * 2}px ${color}`,
        filter: `brightness(${intensity})`
      }}
    />
  )
}

interface NeuralConnectionProps {
  from: { x: number; y: number }
  to: { x: number; y: number }
  intensity: number
  delay?: number
}

function NeuralConnection({ from, to, intensity, delay = 0 }: NeuralConnectionProps) {
  const [isActive, setIsActive] = useState(false)

  useEffect(() => {
    const interval = setInterval(() => {
      setIsActive(prev => !prev)
    }, 2000 + delay * 100)

    return () => clearInterval(interval)
  }, [delay])

  const length = Math.sqrt((to.x - from.x) ** 2 + (to.y - from.y) ** 2)
  const angle = Math.atan2(to.y - from.y, to.x - from.x) * (180 / Math.PI)

  return (
    <motion.div
      className="absolute origin-left"
      style={{
        left: from.x,
        top: from.y,
        width: length,
        height: 2,
        transform: `rotate(${angle}deg)`,
        background: isActive 
          ? `linear-gradient(90deg, transparent 0%, #3b82f6 50%, transparent 100%)`
          : 'transparent',
        boxShadow: isActive ? '0 0 10px #3b82f6' : 'none'
      }}
      initial={{ opacity: 0 }}
      animate={{ opacity: isActive ? 1 : 0.3 }}
      transition={{ duration: 0.5 }}
    />
  )
}

export function NeuralBackground({ 
  nodeCount = 15,
  connectionCount = 20,
  className = ''
}: {
  nodeCount?: number
  connectionCount?: number
  className?: string
}) {
  const [nodes, setNodes] = useState<Array<{
    x: number
    y: number
    size: number
    intensity: number
    color: string
  }>>([])
  const [connections, setConnections] = useState<Array<{
    from: { x: number; y: number }
    to: { x: number; y: number }
    intensity: number
  }>>([])

  useEffect(() => {
    // Generate nodes
    const newNodes = Array.from({ length: nodeCount }, (_, i) => ({
      x: Math.random() * 100,
      y: Math.random() * 100,
      size: Math.random() * 20 + 10,
      intensity: Math.random() * 0.5 + 0.5,
      color: `hsl(${Math.random() * 60 + 200}, 70%, 60%)`
    }))

    // Generate connections
    const newConnections = Array.from({ length: connectionCount }, () => {
      const fromNode = newNodes[Math.floor(Math.random() * newNodes.length)]
      const toNode = newNodes[Math.floor(Math.random() * newNodes.length)]
      return {
        from: { x: fromNode.x, y: fromNode.y },
        to: { x: toNode.x, y: toNode.y },
        intensity: Math.random()
      }
    })

    setNodes(newNodes)
    setConnections(newConnections)
  }, [nodeCount, connectionCount])

  return (
    <div className={`absolute inset-0 overflow-hidden ${className}`}>
      {connections.map((connection, index) => (
        <NeuralConnection
          key={index}
          from={connection.from}
          to={connection.to}
          intensity={connection.intensity}
          delay={index * 0.1}
        />
      ))}
      {nodes.map((node, index) => (
        <NeuralNode
          key={index}
          x={node.x}
          y={node.y}
          size={node.size}
          intensity={node.intensity}
          color={node.color}
          delay={index * 0.2}
        />
      ))}
    </div>
  )
}

export function NeuralPulse({ 
  children, 
  intensity = 1,
  color = '#3b82f6',
  className = ''
}: {
  children: React.ReactNode
  intensity?: number
  color?: string
  className?: string
}) {
  return (
    <motion.div
      className={`relative ${className}`}
      animate={{
        boxShadow: [
          `0 0 0px ${color}`,
          `0 0 ${20 * intensity}px ${color}`,
          `0 0 0px ${color}`
        ]
      }}
      transition={{
        duration: 2,
        repeat: Infinity,
        ease: 'easeInOut'
      }}
    >
      {children}
    </motion.div>
  )
}

export function NeuralGrid({ 
  rows = 10, 
  cols = 15,
  className = ''
}: {
  rows?: number
  cols?: number
  className?: string
}) {
  const [activeCells, setActiveCells] = useState<Set<string>>(new Set())

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveCells(prev => {
        const newActive = new Set<string>()
        const totalCells = rows * cols
        
        // Activate random cells
        for (let i = 0; i < Math.floor(totalCells * 0.1); i++) {
          const row = Math.floor(Math.random() * rows)
          const col = Math.floor(Math.random() * cols)
          newActive.add(`${row}-${col}`)
        }
        
        return newActive
      })
    }, 100)

    return () => clearInterval(interval)
  }, [rows, cols])

  return (
    <div className={`absolute inset-0 grid ${className}`} style={{
      gridTemplateRows: `repeat(${rows}, 1fr)`,
      gridTemplateColumns: `repeat(${cols}, 1fr)`
    }}>
      {Array.from({ length: rows * cols }, (_, i) => {
        const row = Math.floor(i / cols)
        const col = i % cols
        const isActive = activeCells.has(`${row}-${col}`)
        
        return (
          <motion.div
            key={i}
            className="border border-blue-500/20"
            animate={{
              backgroundColor: isActive ? '#3b82f6' : 'transparent',
              boxShadow: isActive ? '0 0 10px #3b82f6' : 'none'
            }}
            transition={{ duration: 0.3 }}
          />
        )
      })}
    </div>
  )
}

export function NeuralWave({ 
  amplitude = 20,
  frequency = 0.02,
  speed = 0.01,
  color = '#3b82f6',
  className = ''
}: {
  amplitude?: number
  frequency?: number
  speed?: number
  color?: string
  className?: string
}) {
  const [offset, setOffset] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setOffset(prev => prev + speed)
    }, 16)

    return () => clearInterval(interval)
  }, [speed])

  return (
    <div className={`relative overflow-hidden ${className}`}>
      <svg
        className="absolute inset-0 w-full h-full"
        viewBox="0 0 100 20"
        preserveAspectRatio="none"
      >
        <motion.path
          d={`M 0,10 Q 25,${10 - amplitude * Math.sin(offset * frequency)} 50,10 T 100,10`}
          stroke={color}
          strokeWidth="0.5"
          fill="none"
          animate={{
            d: [
              `M 0,10 Q 25,${10 - amplitude * Math.sin(offset * frequency)} 50,10 T 100,10`,
              `M 0,10 Q 25,${10 + amplitude * Math.sin(offset * frequency)} 50,10 T 100,10`,
              `M 0,10 Q 25,${10 - amplitude * Math.sin(offset * frequency)} 50,10 T 100,10`
            ]
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: 'easeInOut'
          }}
        />
      </svg>
    </div>
  )
}

export function NeuralLoading({ 
  size = 40,
  color = '#3b82f6',
  className = ''
}: {
  size?: number
  color?: string
  className?: string
}) {
  return (
    <div className={`flex items-center justify-center ${className}`}>
      <motion.div
        className="relative"
        style={{ width: size, height: size }}
        animate={{ rotate: 360 }}
        transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
      >
        <motion.div
          className="absolute inset-0 rounded-full border-2 border-transparent"
          style={{
            borderTopColor: color,
            borderRightColor: color
          }}
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
        />
        <motion.div
          className="absolute inset-2 rounded-full border-2 border-transparent"
          style={{
            borderBottomColor: color,
            borderLeftColor: color
          }}
          animate={{ rotate: -360 }}
          transition={{ duration: 1.5, repeat: Infinity, ease: 'linear' }}
        />
        <motion.div
          className="absolute inset-4 rounded-full"
          style={{ backgroundColor: color }}
          animate={{ scale: [1, 1.2, 1] }}
          transition={{ duration: 1, repeat: Infinity }}
        />
      </motion.div>
    </div>
  )
}

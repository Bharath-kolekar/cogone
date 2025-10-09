'use client'

import { useEffect, useRef, useState } from 'react'
import { motion } from 'framer-motion'

interface Particle {
  id: number
  x: number
  y: number
  vx: number
  vy: number
  size: number
  opacity: number
  color: string
  life: number
  maxLife: number
}

interface ParticleSystemProps {
  particleCount?: number
  colors?: string[]
  speed?: number
  size?: { min: number; max: number }
  className?: string
}

export function ParticleSystem({
  particleCount = 50,
  colors = ['#3b82f6', '#8b5cf6', '#06b6d4', '#10b981'],
  speed = 1,
  size = { min: 1, max: 4 },
  className = ''
}: ParticleSystemProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const animationRef = useRef<number>()
  const [particles, setParticles] = useState<Particle[]>([])
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 })

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const resizeCanvas = () => {
      const rect = canvas.getBoundingClientRect()
      canvas.width = rect.width
      canvas.height = rect.height
      setDimensions({ width: rect.width, height: rect.height })
    }

    resizeCanvas()
    window.addEventListener('resize', resizeCanvas)

    return () => window.removeEventListener('resize', resizeCanvas)
  }, [])

  useEffect(() => {
    if (dimensions.width === 0 || dimensions.height === 0) return

    // Initialize particles
    const newParticles: Particle[] = []
    for (let i = 0; i < particleCount; i++) {
      newParticles.push({
        id: i,
        x: Math.random() * dimensions.width,
        y: Math.random() * dimensions.height,
        vx: (Math.random() - 0.5) * speed * 2,
        vy: (Math.random() - 0.5) * speed * 2,
        size: Math.random() * (size.max - size.min) + size.min,
        opacity: Math.random() * 0.8 + 0.2,
        color: colors[Math.floor(Math.random() * colors.length)],
        life: Math.random() * 100,
        maxLife: 100
      })
    }
    setParticles(newParticles)
  }, [particleCount, dimensions, colors, speed, size])

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas || particles.length === 0) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      setParticles(prevParticles => {
        return prevParticles.map(particle => {
          // Update position
          let newX = particle.x + particle.vx
          let newY = particle.y + particle.vy

          // Bounce off edges
          if (newX <= 0 || newX >= canvas.width) {
            particle.vx *= -1
            newX = particle.x
          }
          if (newY <= 0 || newY >= canvas.height) {
            particle.vy *= -1
            newY = particle.y
          }

          // Update life
          const newLife = particle.life - 0.5
          const opacity = (newLife / particle.maxLife) * particle.opacity

          // Draw particle
          ctx.save()
          ctx.globalAlpha = opacity
          ctx.fillStyle = particle.color
          ctx.beginPath()
          ctx.arc(newX, newY, particle.size, 0, Math.PI * 2)
          ctx.fill()
          ctx.restore()

          // Reset particle if life is over
          if (newLife <= 0) {
            return {
              ...particle,
              x: Math.random() * canvas.width,
              y: Math.random() * canvas.height,
              life: particle.maxLife,
              opacity: Math.random() * 0.8 + 0.2
            }
          }

          return {
            ...particle,
            x: newX,
            y: newY,
            life: newLife
          }
        })
      })

      animationRef.current = requestAnimationFrame(animate)
    }

    animate()

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current)
      }
    }
  }, [particles.length])

  return (
    <canvas
      ref={canvasRef}
      className={`absolute inset-0 pointer-events-none ${className}`}
      style={{ zIndex: 1 }}
    />
  )
}

// Neural Network Visualization Component
export function NeuralNetworkViz({ 
  nodes = 20, 
  connections = 30,
  className = '' 
}: { 
  nodes?: number
  connections?: number
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

    // Create nodes
    const nodeList = Array.from({ length: nodes }, (_, i) => ({
      id: i,
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.5,
      vy: (Math.random() - 0.5) * 0.5,
      size: Math.random() * 3 + 2,
      color: `hsl(${Math.random() * 60 + 200}, 70%, 60%)`
    }))

    // Create connections
    const connectionList = Array.from({ length: connections }, () => ({
      from: Math.floor(Math.random() * nodes),
      to: Math.floor(Math.random() * nodes),
      strength: Math.random()
    }))

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      // Update and draw connections
      ctx.strokeStyle = 'rgba(59, 130, 246, 0.3)'
      ctx.lineWidth = 1
      connectionList.forEach(conn => {
        const fromNode = nodeList[conn.from]
        const toNode = nodeList[conn.to]
        
        ctx.beginPath()
        ctx.moveTo(fromNode.x, fromNode.y)
        ctx.lineTo(toNode.x, toNode.y)
        ctx.stroke()
      })

      // Update and draw nodes
      nodeList.forEach(node => {
        // Update position
        node.x += node.vx
        node.y += node.vy

        // Bounce off edges
        if (node.x <= 0 || node.x >= canvas.width) node.vx *= -1
        if (node.y <= 0 || node.y >= canvas.height) node.vy *= -1

        // Draw node
        ctx.fillStyle = node.color
        ctx.beginPath()
        ctx.arc(node.x, node.y, node.size, 0, Math.PI * 2)
        ctx.fill()

        // Add glow effect
        ctx.shadowColor = node.color
        ctx.shadowBlur = 10
        ctx.beginPath()
        ctx.arc(node.x, node.y, node.size * 0.5, 0, Math.PI * 2)
        ctx.fill()
        ctx.shadowBlur = 0
      })

      animationRef.current = requestAnimationFrame(animate)
    }

    animate()

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current)
      }
      window.removeEventListener('resize', resizeCanvas)
    }
  }, [nodes, connections])

  return (
    <canvas
      ref={canvasRef}
      className={`absolute inset-0 pointer-events-none ${className}`}
      style={{ zIndex: 1 }}
    />
  )
}

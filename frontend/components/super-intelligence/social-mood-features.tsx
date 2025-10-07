'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Users, Heart, Share2, MessageCircle, TrendingUp, Award, Globe, Lock, Eye, Settings } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'

interface MoodShare {
  id: string
  userId: string
  userName: string
  userAvatar: string
  mood: string
  intensity: number
  message: string
  timestamp: number
  likes: number
  comments: number
  isLiked: boolean
  isPublic: boolean
}

interface MoodChallenge {
  id: string
  name: string
  description: string
  goal: string
  participants: number
  duration: number
  rewards: string[]
  isActive: boolean
  progress: number
}

interface SocialMoodFeaturesProps {
  enableMoodSharing?: boolean
  enableMoodChallenges?: boolean
  enableMoodLeaderboards?: boolean
  enableMoodCollaboration?: boolean
  onMoodShare?: (share: MoodShare) => void
  onMoodChallenge?: (challenge: MoodChallenge) => void
  className?: string
}

export function SocialMoodFeatures({
  enableMoodSharing = true,
  enableMoodChallenges = true,
  enableMoodLeaderboards = true,
  enableMoodCollaboration = true,
  onMoodShare,
  onMoodChallenge,
  className = ''
}: SocialMoodFeaturesProps) {
  const [moodShares, setMoodShares] = useState<MoodShare[]>([])
  const [moodChallenges, setMoodChallenges] = useState<MoodChallenge[]>([])
  const [leaderboard, setLeaderboard] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [selectedTab, setSelectedTab] = useState('shares')
  const [showShareModal, setShowShareModal] = useState(false)
  const [shareMessage, setShareMessage] = useState('')
  const [shareMood, setShareMood] = useState('happy')
  const [shareIntensity, setShareIntensity] = useState(0.8)

  const socialData = useRef<{
    totalShares: number
    totalLikes: number
    totalComments: number
    activeChallenges: number
    completedChallenges: number
  }>({
    totalShares: 0,
    totalLikes: 0,
    totalComments: 0,
    activeChallenges: 0,
    completedChallenges: 0
  })

  useEffect(() => {
    loadSocialData()
  }, [])

  const loadSocialData = useCallback(async () => {
    setIsLoading(true)
    
    try {
      // Simulate loading social data
      await new Promise(resolve => setTimeout(resolve, 1000))

      // Generate mock mood shares
      const shares: MoodShare[] = [
        {
          id: '1',
          userId: 'user1',
          userName: 'Alex Johnson',
          userAvatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Alex',
          mood: 'happy',
          intensity: 0.9,
          message: 'Just completed a major project! Feeling amazing! 🎉',
          timestamp: Date.now() - 3600000,
          likes: 12,
          comments: 3,
          isLiked: false,
          isPublic: true
        },
        {
          id: '2',
          userId: 'user2',
          userName: 'Sarah Chen',
          userAvatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Sarah',
          mood: 'focused',
          intensity: 0.8,
          message: 'Deep work session going great! Productivity mode activated 💪',
          timestamp: Date.now() - 7200000,
          likes: 8,
          comments: 2,
          isLiked: true,
          isPublic: true
        },
        {
          id: '3',
          userId: 'user3',
          userName: 'Mike Rodriguez',
          userAvatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Mike',
          mood: 'motivated',
          intensity: 0.95,
          message: 'New goals set, ready to crush them! Let\'s go! 🚀',
          timestamp: Date.now() - 10800000,
          likes: 15,
          comments: 5,
          isLiked: false,
          isPublic: true
        }
      ]

      // Generate mock challenges
      const challenges: MoodChallenge[] = [
        {
          id: '1',
          name: '7-Day Positivity Challenge',
          description: 'Share a positive mood every day for a week',
          goal: 'Maintain positive mood for 7 consecutive days',
          participants: 45,
          duration: 7,
          rewards: ['Positivity Badge', '100 Points', 'Special Avatar'],
          isActive: true,
          progress: 0.6
        },
        {
          id: '2',
          name: 'Focus Master Challenge',
          description: 'Achieve 5 hours of focused work in a day',
          goal: 'Complete 5 hours of deep focus work',
          participants: 23,
          duration: 1,
          rewards: ['Focus Master Badge', '50 Points'],
          isActive: true,
          progress: 0.8
        },
        {
          id: '3',
          name: 'Mood Sharing Champion',
          description: 'Share your mood with the community',
          goal: 'Share 10 mood updates',
          participants: 67,
          duration: 30,
          rewards: ['Social Butterfly Badge', '200 Points', 'Community Recognition'],
          isActive: true,
          progress: 0.3
        }
      ]

      // Generate mock leaderboard
      const leaderboardData = [
        { rank: 1, name: 'Alex Johnson', points: 1250, mood: 'happy', streak: 7 },
        { rank: 2, name: 'Sarah Chen', points: 1180, mood: 'focused', streak: 5 },
        { rank: 3, name: 'Mike Rodriguez', points: 1100, mood: 'motivated', streak: 3 },
        { rank: 4, name: 'Emma Wilson', points: 980, mood: 'excited', streak: 4 },
        { rank: 5, name: 'David Kim', points: 920, mood: 'calm', streak: 2 }
      ]

      setMoodShares(shares)
      setMoodChallenges(challenges)
      setLeaderboard(leaderboardData)

      // Update social data
      socialData.current = {
        totalShares: shares.length,
        totalLikes: shares.reduce((sum, share) => sum + share.likes, 0),
        totalComments: shares.reduce((sum, share) => sum + share.comments, 0),
        activeChallenges: challenges.filter(c => c.isActive).length,
        completedChallenges: challenges.filter(c => c.progress === 1).length
      }

    } catch (error) {
      console.error('Failed to load social data:', error)
    } finally {
      setIsLoading(false)
    }
  }, [])

  const handleMoodShare = useCallback(() => {
    const newShare: MoodShare = {
      id: Date.now().toString(),
      userId: 'current_user',
      userName: 'You',
      userAvatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=You',
      mood: shareMood,
      intensity: shareIntensity,
      message: shareMessage,
      timestamp: Date.now(),
      likes: 0,
      comments: 0,
      isLiked: false,
      isPublic: true
    }

    setMoodShares(prev => [newShare, ...prev])
    onMoodShare?.(newShare)
    setShowShareModal(false)
    setShareMessage('')
  }, [shareMood, shareIntensity, shareMessage, onMoodShare])

  const handleLike = useCallback((shareId: string) => {
    setMoodShares(prev => prev.map(share => 
      share.id === shareId 
        ? { 
            ...share, 
            isLiked: !share.isLiked,
            likes: share.isLiked ? share.likes - 1 : share.likes + 1
          }
        : share
    ))
  }, [])

  const handleJoinChallenge = useCallback((challengeId: string) => {
    setMoodChallenges(prev => prev.map(challenge =>
      challenge.id === challengeId
        ? { ...challenge, participants: challenge.participants + 1 }
        : challenge
    ))
    onMoodChallenge?.(moodChallenges.find(c => c.id === challengeId)!)
  }, [moodChallenges, onMoodChallenge])

  const getMoodIcon = (mood: string) => {
    const icons = {
      'happy': '😊',
      'sad': '😢',
      'excited': '🤩',
      'focused': '🎯',
      'motivated': '💪',
      'stressed': '😰',
      'calm': '😌',
      'confused': '😕'
    }
    return icons[mood as keyof typeof icons] || '😐'
  }

  const getMoodColor = (mood: string) => {
    const colors = {
      'happy': 'text-yellow-600 bg-yellow-100',
      'sad': 'text-blue-600 bg-blue-100',
      'excited': 'text-orange-600 bg-orange-100',
      'focused': 'text-green-600 bg-green-100',
      'motivated': 'text-red-600 bg-red-100',
      'stressed': 'text-red-600 bg-red-100',
      'calm': 'text-purple-600 bg-purple-100',
      'confused': 'text-gray-600 bg-gray-100'
    }
    return colors[mood as keyof typeof colors] || 'text-gray-600 bg-gray-100'
  }

  const tabs = [
    { id: 'shares', name: 'Mood Shares', icon: Share2 },
    { id: 'challenges', name: 'Challenges', icon: Award },
    { id: 'leaderboard', name: 'Leaderboard', icon: TrendingUp },
    { id: 'collaboration', name: 'Collaboration', icon: Users }
  ]

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Loading State */}
      {isLoading && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-lg p-4"
        >
          <div className="flex items-center space-x-3 mb-3">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
            <span className="text-sm font-medium text-blue-800 dark:text-blue-200">
              Loading social features...
            </span>
          </div>
          <Progress value={50} className="h-2" />
        </motion.div>
      )}

      {/* Social Stats */}
      {!isLoading && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          <Card className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Users className="h-5 w-5 text-blue-600" />
                <span>Social Mood Community</span>
              </CardTitle>
              <CardDescription>
                Connect with others through shared emotional experiences
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">
                    {socialData.current.totalShares}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Total Shares</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">
                    {socialData.current.totalLikes}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Total Likes</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">
                    {socialData.current.totalComments}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Comments</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-orange-600">
                    {socialData.current.activeChallenges}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Active Challenges</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-red-600">
                    {socialData.current.completedChallenges}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Completed</div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Tab Navigation */}
          <div className="flex flex-wrap gap-2">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <Button
                  key={tab.id}
                  variant={selectedTab === tab.id ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setSelectedTab(tab.id)}
                  className="flex items-center space-x-2"
                >
                  <Icon className="h-4 w-4" />
                  <span>{tab.name}</span>
                </Button>
              )
            })}
          </div>

          {/* Tab Content */}
          <AnimatePresence mode="wait">
            {selectedTab === 'shares' && enableMoodSharing && (
              <motion.div
                key="shares"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="space-y-4"
              >
                <div className="flex justify-between items-center">
                  <h3 className="text-lg font-semibold">Mood Shares</h3>
                  <Button onClick={() => setShowShareModal(true)}>
                    Share Your Mood
                  </Button>
                </div>

                <div className="space-y-4">
                  {moodShares.map((share) => (
                    <Card key={share.id}>
                      <CardContent className="p-4">
                        <div className="flex items-start space-x-3">
                          <img
                            src={share.userAvatar}
                            alt={share.userName}
                            className="w-10 h-10 rounded-full"
                          />
                          <div className="flex-1">
                            <div className="flex items-center space-x-2 mb-2">
                              <span className="font-medium">{share.userName}</span>
                              <Badge className={getMoodColor(share.mood)}>
                                {getMoodIcon(share.mood)} {share.mood}
                              </Badge>
                              <span className="text-sm text-gray-500">
                                {(share.intensity * 100).toFixed(0)}% intensity
                              </span>
                            </div>
                            <p className="text-gray-700 dark:text-gray-300 mb-3">
                              {share.message}
                            </p>
                            <div className="flex items-center space-x-4">
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => handleLike(share.id)}
                                className={share.isLiked ? 'text-red-600' : ''}
                              >
                                <Heart className="h-4 w-4 mr-1" />
                                {share.likes}
                              </Button>
                              <Button variant="ghost" size="sm">
                                <MessageCircle className="h-4 w-4 mr-1" />
                                {share.comments}
                              </Button>
                              <Button variant="ghost" size="sm">
                                <Share2 className="h-4 w-4 mr-1" />
                                Share
                              </Button>
                            </div>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </motion.div>
            )}

            {selectedTab === 'challenges' && enableMoodChallenges && (
              <motion.div
                key="challenges"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="space-y-4"
              >
                <h3 className="text-lg font-semibold">Mood Challenges</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {moodChallenges.map((challenge) => (
                    <Card key={challenge.id}>
                      <CardHeader>
                        <CardTitle className="text-sm">{challenge.name}</CardTitle>
                        <CardDescription>{challenge.description}</CardDescription>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-3">
                          <div className="flex justify-between items-center">
                            <span className="text-sm font-medium">Progress</span>
                            <span className="text-sm">{(challenge.progress * 100).toFixed(0)}%</span>
                          </div>
                          <Progress value={challenge.progress * 100} className="h-2" />
                          <div className="flex justify-between items-center">
                            <span className="text-sm text-gray-600 dark:text-gray-400">
                              {challenge.participants} participants
                            </span>
                            <Button
                              size="sm"
                              onClick={() => handleJoinChallenge(challenge.id)}
                            >
                              Join Challenge
                            </Button>
                          </div>
                          <div className="flex flex-wrap gap-1">
                            {challenge.rewards.map((reward, index) => (
                              <Badge key={index} variant="outline" className="text-xs">
                                {reward}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </motion.div>
            )}

            {selectedTab === 'leaderboard' && enableMoodLeaderboards && (
              <motion.div
                key="leaderboard"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="space-y-4"
              >
                <h3 className="text-lg font-semibold">Mood Leaderboard</h3>
                <Card>
                  <CardContent className="p-0">
                    <div className="space-y-2">
                      {leaderboard.map((user, index) => (
                        <div key={user.rank} className="flex items-center justify-between p-4 border-b last:border-b-0">
                          <div className="flex items-center space-x-3">
                            <div className="w-8 h-8 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full flex items-center justify-center text-white font-bold">
                              {user.rank}
                            </div>
                            <div>
                              <div className="font-medium">{user.name}</div>
                              <div className="text-sm text-gray-600 dark:text-gray-400">
                                {user.points} points • {user.streak} day streak
                              </div>
                            </div>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Badge className={getMoodColor(user.mood)}>
                              {getMoodIcon(user.mood)} {user.mood}
                            </Badge>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            )}

            {selectedTab === 'collaboration' && enableMoodCollaboration && (
              <motion.div
                key="collaboration"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="space-y-4"
              >
                <h3 className="text-lg font-semibold">Mood Collaboration</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-sm">Team Mood Sync</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                        Sync your mood with team members for better collaboration
                      </p>
                      <Button className="w-full">
                        <Users className="h-4 w-4 mr-2" />
                        Join Team Sync
                      </Button>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="text-sm">Mood Matching</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                        Find users with similar moods for better connections
                      </p>
                      <Button className="w-full">
                        <Heart className="h-4 w-4 mr-2" />
                        Find Mood Matches
                      </Button>
                    </CardContent>
                  </Card>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Share Modal */}
          {showShareModal && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
              onClick={() => setShowShareModal(false)}
            >
              <motion.div
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                className="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-md mx-4"
                onClick={(e) => e.stopPropagation()}
              >
                <h3 className="text-lg font-semibold mb-4">Share Your Mood</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">Mood</label>
                    <select
                      value={shareMood}
                      onChange={(e) => setShareMood(e.target.value)}
                      className="w-full p-2 border rounded-lg"
                    >
                      <option value="happy">Happy</option>
                      <option value="excited">Excited</option>
                      <option value="focused">Focused</option>
                      <option value="motivated">Motivated</option>
                      <option value="calm">Calm</option>
                      <option value="stressed">Stressed</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Intensity: {(shareIntensity * 100).toFixed(0)}%
                    </label>
                    <input
                      type="range"
                      min="0"
                      max="1"
                      step="0.1"
                      value={shareIntensity}
                      onChange={(e) => setShareIntensity(parseFloat(e.target.value))}
                      className="w-full"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">Message</label>
                    <textarea
                      value={shareMessage}
                      onChange={(e) => setShareMessage(e.target.value)}
                      placeholder="How are you feeling today?"
                      className="w-full p-2 border rounded-lg h-20"
                    />
                  </div>
                  <div className="flex space-x-2">
                    <Button onClick={handleMoodShare} className="flex-1">
                      Share Mood
                    </Button>
                    <Button variant="outline" onClick={() => setShowShareModal(false)}>
                      Cancel
                    </Button>
                  </div>
                </div>
              </motion.div>
            </motion.div>
          )}
        </motion.div>
      )}
    </div>
  )
}

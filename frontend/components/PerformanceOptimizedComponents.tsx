"use client";

import React, { useState, useEffect, useMemo, useCallback, memo } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import { toast } from '../hooks/use-toast';
import { 
  Bot, 
  Plus, 
  Play, 
  Pause, 
  Settings, 
  BarChart3, 
  MessageSquare, 
  Zap,
  Cpu,
  DollarSign,
  Activity,
  Users,
  Clock,
  CheckCircle,
  AlertCircle,
  Brain,
  Sparkles,
  TrendingUp,
  Database,
  Code,
  FileText,
  Lightbulb,
  BookOpen,
  Terminal,
  GitBranch,
  Search,
  Filter
} from 'lucide-react';

// Memoized components to prevent unnecessary re-renders
const AgentCard = memo(({ 
  agent, 
  onToggleStatus, 
  onDelete, 
  onViewAnalytics 
}: {
  agent: any;
  onToggleStatus: (id: string) => void;
  onDelete: (id: string) => void;
  onViewAnalytics: (id: string) => void;
}) => {
  const handleToggleStatus = useCallback(() => {
    onToggleStatus(agent.id);
  }, [agent.id, onToggleStatus]);

  const handleDelete = useCallback(() => {
    onDelete(agent.id);
  }, [agent.id, onDelete]);

  const handleViewAnalytics = useCallback(() => {
    onViewAnalytics(agent.id);
  }, [agent.id, onViewAnalytics]);

  return (
    <Card className="hover:shadow-lg transition-shadow duration-200">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg">
              <Bot className="h-5 w-5 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <CardTitle className="text-lg">{agent.name}</CardTitle>
              <CardDescription className="text-sm">{agent.description}</CardDescription>
            </div>
          </div>
          <Badge 
            variant={agent.status === 'active' ? 'default' : 'secondary'}
            className="capitalize"
          >
            {agent.status}
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          <div className="flex flex-wrap gap-2">
            {agent.capabilities?.slice(0, 3).map((capability: string, index: number) => (
              <Badge key={index} variant="outline" className="text-xs">
                {capability.replace('_', ' ')}
              </Badge>
            ))}
            {agent.capabilities?.length > 3 && (
              <Badge variant="outline" className="text-xs">
                +{agent.capabilities.length - 3} more
              </Badge>
            )}
          </div>
          
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <p className="text-gray-600 dark:text-gray-400">Interactions</p>
              <p className="font-semibold">{agent.metrics?.total_interactions || 0}</p>
            </div>
            <div>
              <p className="text-gray-600 dark:text-gray-400">Response Time</p>
              <p className="font-semibold">
                {(agent.metrics?.average_response_time || 0).toFixed(2)}s
              </p>
            </div>
          </div>
          
          <div className="flex space-x-2">
            <Button
              size="sm"
              variant="outline"
              onClick={handleToggleStatus}
              className="flex-1"
            >
              {agent.status === 'active' ? (
                <>
                  <Pause className="h-4 w-4 mr-1" />
                  Pause
                </>
              ) : (
                <>
                  <Play className="h-4 w-4 mr-1" />
                  Start
                </>
              )}
            </Button>
            <Button
              size="sm"
              variant="outline"
              onClick={handleViewAnalytics}
              className="flex-1"
            >
              <BarChart3 className="h-4 w-4 mr-1" />
              Analytics
            </Button>
            <Button
              size="sm"
              variant="outline"
              onClick={handleDelete}
              className="text-red-600 hover:text-red-700"
            >
              <Settings className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
});

AgentCard.displayName = 'AgentCard';

// Memoized analytics component
const AnalyticsCard = memo(({ 
  title, 
  value, 
  icon: Icon, 
  color, 
  trend 
}: {
  title: string;
  value: string | number;
  icon: React.ComponentType<any>;
  color: string;
  trend?: number;
}) => (
  <Card>
    <CardContent className="p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600 dark:text-gray-400">{title}</p>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">{value}</p>
          {trend !== undefined && (
            <div className="flex items-center mt-1">
              <TrendingUp className={`h-4 w-4 mr-1 ${trend > 0 ? 'text-green-500' : 'text-red-500'}`} />
              <span className={`text-sm ${trend > 0 ? 'text-green-500' : 'text-red-500'}`}>
                {trend > 0 ? '+' : ''}{trend}%
              </span>
            </div>
          )}
        </div>
        <div className={`p-3 rounded-lg ${color}`}>
          <Icon className="h-6 w-6 text-white" />
        </div>
      </div>
    </CardContent>
  </Card>
));

AnalyticsCard.displayName = 'AnalyticsCard';

// Performance-optimized AI Agent Dashboard
export function PerformanceOptimizedAIAgentDashboard() {
  const [agents, setAgents] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('agents');
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [performanceMetrics, setPerformanceMetrics] = useState<any>(null);

  // Memoized filtered agents to prevent unnecessary recalculations
  const filteredAgents = useMemo(() => {
    return agents.filter(agent => {
      const matchesSearch = agent.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           agent.description.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesStatus = filterStatus === 'all' || agent.status === filterStatus;
      return matchesSearch && matchesStatus;
    });
  }, [agents, searchTerm, filterStatus]);

  // Memoized analytics calculations
  const analyticsData = useMemo(() => {
    if (!agents.length) return null;

    const totalInteractions = agents.reduce((sum, agent) => sum + (agent.metrics?.total_interactions || 0), 0);
    const avgResponseTime = agents.reduce((sum, agent) => sum + (agent.metrics?.average_response_time || 0), 0) / agents.length;
    const totalCost = agents.reduce((sum, agent) => sum + (agent.metrics?.total_cost || 0), 0);
    const avgSatisfaction = agents.reduce((sum, agent) => sum + (agent.metrics?.user_satisfaction || 0), 0) / agents.length;

    return {
      totalInteractions,
      avgResponseTime: avgResponseTime.toFixed(2),
      totalCost: totalCost.toFixed(2),
      avgSatisfaction: avgSatisfaction.toFixed(1)
    };
  }, [agents]);

  // Debounced search to prevent excessive API calls
  const [debouncedSearchTerm, setDebouncedSearchTerm] = useState('');
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearchTerm(searchTerm);
    }, 300);
    return () => clearTimeout(timer);
  }, [searchTerm]);

  // Optimized fetch function with caching
  const fetchAgents = useCallback(async () => {
    if (loading) return; // Prevent multiple simultaneous requests

    try {
      setLoading(true);
      const cacheKey = `agents_${debouncedSearchTerm}_${filterStatus}`;
      const cachedData = localStorage.getItem(cacheKey);
      
      if (cachedData) {
        const { data, timestamp } = JSON.parse(cachedData);
        // Use cached data if less than 5 minutes old
        if (Date.now() - timestamp < 300000) {
          setAgents(data);
          return;
        }
      }

      const response = await fetch(`/api/ai-agents?search=${debouncedSearchTerm}&status=${filterStatus}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        const agentsData = data.agents || [];
        setAgents(agentsData);
        
        // Cache the data
        localStorage.setItem(cacheKey, JSON.stringify({
          data: agentsData,
          timestamp: Date.now()
        }));
      } else {
        toast({
          title: "Error",
          description: "Failed to fetch agents",
          variant: "destructive"
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to fetch agents",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  }, [debouncedSearchTerm, filterStatus, loading]);

  // Fetch performance metrics
  const fetchPerformanceMetrics = useCallback(async () => {
    try {
      const response = await fetch('/api/ai-agents/performance-metrics', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setPerformanceMetrics(data);
      }
    } catch (error) {
      console.error('Failed to fetch performance metrics:', error);
    }
  }, []);

  // Load data on mount and when dependencies change
  useEffect(() => {
    fetchAgents();
  }, [fetchAgents]);

  useEffect(() => {
    fetchPerformanceMetrics();
  }, [fetchPerformanceMetrics]);

  // Memoized event handlers
  const handleToggleStatus = useCallback(async (agentId: string) => {
    try {
      const agent = agents.find(a => a.id === agentId);
      const newStatus = agent?.status === 'active' ? 'inactive' : 'active';
      
      const response = await fetch(`/api/ai-agents/${agentId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({ status: newStatus })
      });
      
      if (response.ok) {
        setAgents(prev => prev.map(a => 
          a.id === agentId ? { ...a, status: newStatus } : a
        ));
        
        // Clear cache to force refresh
        localStorage.removeItem(`agents_${debouncedSearchTerm}_${filterStatus}`);
        
        toast({
          title: "Success",
          description: `Agent ${newStatus === 'active' ? 'started' : 'paused'}`,
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to update agent status",
        variant: "destructive"
      });
    }
  }, [agents, debouncedSearchTerm, filterStatus]);

  const handleDelete = useCallback(async (agentId: string) => {
    if (!confirm('Are you sure you want to delete this agent?')) return;
    
    try {
      const response = await fetch(`/api/ai-agents/${agentId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      
      if (response.ok) {
        setAgents(prev => prev.filter(a => a.id !== agentId));
        
        // Clear cache to force refresh
        localStorage.removeItem(`agents_${debouncedSearchTerm}_${filterStatus}`);
        
        toast({
          title: "Success",
          description: "Agent deleted successfully",
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to delete agent",
        variant: "destructive"
      });
    }
  }, [debouncedSearchTerm, filterStatus]);

  const handleViewAnalytics = useCallback((agentId: string) => {
    // Navigate to analytics page or open modal
    window.open(`/analytics/agent/${agentId}`, '_blank');
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">AI Agents</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Manage your AI agents with optimized performance
          </p>
        </div>
        <Button className="bg-blue-600 hover:bg-blue-700">
          <Plus className="h-4 w-4 mr-2" />
          Create Agent
        </Button>
      </div>

      {/* Performance Metrics */}
      {performanceMetrics && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <AnalyticsCard
            title="Response Time"
            value={`${performanceMetrics.average_response_time || '0.000'}s`}
            icon={Clock}
            color="bg-blue-500"
            trend={performanceMetrics.response_time_improvement}
          />
          <AnalyticsCard
            title="Memory Usage"
            value={`${performanceMetrics.memory_usage || 0}MB`}
            icon={Database}
            color="bg-green-500"
            trend={performanceMetrics.memory_reduction}
          />
          <AnalyticsCard
            title="Cache Hit Rate"
            value={`${performanceMetrics.cache_stats?.hit_rate || '0%'}`}
            icon={Activity}
            color="bg-purple-500"
          />
          <AnalyticsCard
            title="Active Agents"
            value={performanceMetrics.active_agents || 0}
            icon={Bot}
            color="bg-orange-500"
          />
        </div>
      )}

      {/* Tabs */}
      <div className="border-b border-gray-200 dark:border-gray-700">
        <nav className="-mb-px flex space-x-8">
          {[
            { id: 'agents', label: 'Agents', icon: Bot },
            { id: 'smart-coding', label: 'Smart Coding AI', icon: Code },
            { id: 'analytics', label: 'Analytics', icon: BarChart3 },
            { id: 'performance', label: 'Performance', icon: TrendingUp }
          ].map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              onClick={() => setActiveTab(id)}
              className={`flex items-center space-x-2 py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === id
                  ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                  : 'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
              }`}
            >
              <Icon className="h-4 w-4" />
              <span>{label}</span>
            </button>
          ))}
        </nav>
      </div>

      {/* Agents Tab */}
      {activeTab === 'agents' && (
        <div className="space-y-6">
          {/* Filters */}
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <Input
                placeholder="Search agents..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full"
              />
            </div>
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
            >
              <option value="all">All Status</option>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
              <option value="training">Training</option>
              <option value="error">Error</option>
            </select>
          </div>

          {/* Agents Grid */}
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredAgents.map((agent) => (
                <AgentCard
                  key={agent.id}
                  agent={agent}
                  onToggleStatus={handleToggleStatus}
                  onDelete={handleDelete}
                  onViewAnalytics={handleViewAnalytics}
                />
              ))}
            </div>
          )}

          {!loading && filteredAgents.length === 0 && (
            <div className="text-center py-12">
              <Bot className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                No agents found
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                {searchTerm || filterStatus !== 'all' 
                  ? 'Try adjusting your search or filter criteria.'
                  : 'Create your first AI agent to get started.'
                }
              </p>
            </div>
          )}
        </div>
      )}

      {/* Smart Coding AI Tab */}
      {activeTab === 'smart-coding' && (
        <div className="space-y-6">
          {/* Smart Coding AI Overview */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Code Completions</CardTitle>
                <Code className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">1,234</div>
                <p className="text-xs text-muted-foreground">
                  +12% from last month
                </p>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Suggestions</CardTitle>
                <Lightbulb className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">567</div>
                <p className="text-xs text-muted-foreground">
                  +8% from last month
                </p>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Snippets</CardTitle>
                <FileText className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">89</div>
                <p className="text-xs text-muted-foreground">
                  +15% from last month
                </p>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Documentation</CardTitle>
                <BookOpen className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">45</div>
                <p className="text-xs text-muted-foreground">
                  +5% from last month
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Code Editor Interface */}
          <Card>
            <CardHeader>
              <CardTitle>Smart Code Assistant</CardTitle>
              <CardDescription>
                Get intelligent code completions, suggestions, and documentation
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {/* Language Selection */}
                <div className="flex items-center space-x-4">
                  <label className="text-sm font-medium">Language:</label>
                  <select className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <option value="python">Python</option>
                    <option value="javascript">JavaScript</option>
                    <option value="typescript">TypeScript</option>
                    <option value="java">Java</option>
                    <option value="csharp">C#</option>
                    <option value="cpp">C++</option>
                    <option value="go">Go</option>
                    <option value="rust">Rust</option>
                  </select>
                </div>

                {/* Code Editor */}
                <div className="border border-gray-300 rounded-lg">
                  <div className="bg-gray-50 dark:bg-gray-800 px-4 py-2 border-b border-gray-300">
                    <div className="flex items-center space-x-2">
                      <Terminal className="h-4 w-4" />
                      <span className="text-sm font-medium">main.py</span>
                    </div>
                  </div>
                  <textarea
                    className="w-full h-64 p-4 font-mono text-sm focus:outline-none resize-none"
                    placeholder="def hello_world():
    # Type your code here...
    # Get intelligent completions as you type"
                    defaultValue="def hello_world():
    # Type your code here...
    # Get intelligent completions as you type"
                  />
                </div>

                {/* Action Buttons */}
                <div className="flex space-x-2">
                  <Button className="flex items-center space-x-2">
                    <Code className="h-4 w-4" />
                    <span>Get Completions</span>
                  </Button>
                  <Button variant="outline" className="flex items-center space-x-2">
                    <Lightbulb className="h-4 w-4" />
                    <span>Get Suggestions</span>
                  </Button>
                  <Button variant="outline" className="flex items-center space-x-2">
                    <FileText className="h-4 w-4" />
                    <span>Get Snippets</span>
                  </Button>
                  <Button variant="outline" className="flex items-center space-x-2">
                    <BookOpen className="h-4 w-4" />
                    <span>Get Documentation</span>
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Recent Completions */}
          <Card>
            <CardHeader>
              <CardTitle>Recent Completions</CardTitle>
              <CardDescription>
                Your recent code completions and suggestions
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {[
                  {
                    id: 1,
                    text: "async def fetch_data():",
                    type: "function",
                    language: "python",
                    confidence: 0.95,
                    timestamp: "2 minutes ago"
                  },
                  {
                    id: 2,
                    text: "try:\n    # Your code here\nexcept Exception as e:",
                    type: "snippet",
                    language: "python",
                    confidence: 0.92,
                    timestamp: "5 minutes ago"
                  },
                  {
                    id: 3,
                    text: "from typing import List, Dict",
                    type: "import",
                    language: "python",
                    confidence: 0.98,
                    timestamp: "10 minutes ago"
                  }
                ].map((completion) => (
                  <div key={completion.id} className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg">
                        <Code className="h-4 w-4 text-blue-600 dark:text-blue-400" />
                      </div>
                      <div>
                        <p className="font-medium text-sm">{completion.text}</p>
                        <div className="flex items-center space-x-2 text-xs text-gray-500">
                          <Badge variant="outline" className="text-xs">
                            {completion.type}
                          </Badge>
                          <Badge variant="outline" className="text-xs">
                            {completion.language}
                          </Badge>
                          <span>{completion.timestamp}</span>
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium">
                        {(completion.confidence * 100).toFixed(0)}%
                      </p>
                      <p className="text-xs text-gray-500">confidence</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Analytics Tab */}
      {activeTab === 'analytics' && analyticsData && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <AnalyticsCard
            title="Total Interactions"
            value={analyticsData.totalInteractions}
            icon={MessageSquare}
            color="bg-blue-500"
          />
          <AnalyticsCard
            title="Avg Response Time"
            value={`${analyticsData.avgResponseTime}s`}
            icon={Clock}
            color="bg-green-500"
          />
          <AnalyticsCard
            title="Total Cost"
            value={`$${analyticsData.totalCost}`}
            icon={DollarSign}
            color="bg-purple-500"
          />
          <AnalyticsCard
            title="Avg Satisfaction"
            value={`${analyticsData.avgSatisfaction}/5`}
            icon={CheckCircle}
            color="bg-orange-500"
          />
        </div>
      )}
    </div>
  );
}

export default PerformanceOptimizedAIAgentDashboard;

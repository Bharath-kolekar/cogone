/**
 * Code Editor Page
 * Seamless Edit & Fix Workflow with Ctrl+L integration
 */

'use client'

import { useState, useEffect } from 'react'
import { useAuthContext } from '@/contexts/AuthContext'
import { Navigation } from '@/components/navigation'
import { CodeEditor } from '@/components/code-editor'
import { SmartCodeEditor } from '@/components/smart-code-editor'
import { NLPSmartCodeEditor } from '@/components/nlp-smart-code-editor'
import { VoiceDictationToggle } from '@/components/voice-dictation-toggle'
import { VoiceFeedback } from '@/components/voice-feedback'
import { VoiceAIDashboard } from '@/components/voice-ai-dashboard'
import { useVoiceDictation } from '@/hooks/useVoiceDictation'
import { initializeVoiceCommandMapper } from '@/services/voice-command-mapper'
import { initializeVoiceAIIntegration } from '@/services/voice-ai-integration'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  Code, 
  FileText, 
  Download, 
  Upload, 
  Save, 
  Play,
  Settings,
  Lightbulb,
  CheckCircle,
  AlertTriangle
} from 'lucide-react'
import { motion } from 'framer-motion'
import { apiService } from '@/lib/api'

interface CodeTemplate {
  name: string
  description: string
  code: string
}

export default function EditorPage() {
  const { user, isAuthenticated, isLoading } = useAuthContext()
  const [code, setCode] = useState('')
  const [language, setLanguage] = useState('javascript')
  const [templates, setTemplates] = useState<CodeTemplate[]>([])
  const [isLoadingTemplates, setIsLoadingTemplates] = useState(false)
  const [savedFiles, setSavedFiles] = useState<Array<{ id: string; name: string; language: string; lastModified: string }>>([])
  const [activeTab, setActiveTab] = useState('editor')
  const [showVoiceControls, setShowVoiceControls] = useState(false)
  const [useSmartEditor, setUseSmartEditor] = useState(true)
  const [useNLPEditor, setUseNLPEditor] = useState(false)

  // Initialize voice dictation
  const voiceDictation = useVoiceDictation()

  useEffect(() => {
    // Initialize voice command mapper and AI integration
    if (voiceDictation.isSupported) {
      const commandMapper = initializeVoiceCommandMapper(voiceDictation)
      initializeVoiceAIIntegration(voiceDictation, commandMapper)
    }
  }, [voiceDictation.isSupported])

  const supportedLanguages = [
    { name: 'JavaScript', value: 'javascript' },
    { name: 'TypeScript', value: 'typescript' },
    { name: 'Python', value: 'python' },
    { name: 'Java', value: 'java' },
    { name: 'C++', value: 'cpp' },
    { name: 'C#', value: 'csharp' },
    { name: 'Go', value: 'go' },
    { name: 'Rust', value: 'rust' },
    { name: 'PHP', value: 'php' },
    { name: 'Ruby', value: 'ruby' },
    { name: 'Swift', value: 'swift' },
    { name: 'Kotlin', value: 'kotlin' },
    { name: 'HTML', value: 'html' },
    { name: 'CSS', value: 'css' },
    { name: 'SQL', value: 'sql' },
    { name: 'JSON', value: 'json' },
    { name: 'YAML', value: 'yaml' },
    { name: 'Markdown', value: 'markdown' },
  ]

  useEffect(() => {
    if (isAuthenticated) {
      loadTemplates()
      loadSavedFiles()
    }
  }, [isAuthenticated, language])

  const loadTemplates = async () => {
    try {
      setIsLoadingTemplates(true)
      const response = await apiService.getCodeTemplates(language)
      if (response.success && response.data) {
        setTemplates(response.data.templates || [])
      }
    } catch (error) {
      console.error('Failed to load templates:', error)
    } finally {
      setIsLoadingTemplates(false)
    }
  }

  const loadSavedFiles = async () => {
    // In a real implementation, this would load from the backend
    setSavedFiles([
      { id: '1', name: 'app.js', language: 'javascript', lastModified: '2024-01-15' },
      { id: '2', name: 'component.tsx', language: 'typescript', lastModified: '2024-01-14' },
      { id: '3', name: 'api.py', language: 'python', lastModified: '2024-01-13' },
    ])
  }

  const handleCodeChange = (newCode: string) => {
    setCode(newCode)
  }

  const handleSave = async (codeToSave: string) => {
    try {
      // In a real implementation, this would save to the backend
      console.log('Saving code:', codeToSave)
      // await apiService.saveCode({ code: codeToSave, language, name: 'untitled' })
    } catch (error) {
      console.error('Failed to save code:', error)
    }
  }

  const handleLoadTemplate = (template: CodeTemplate) => {
    setCode(template.code)
  }

  const handleDownload = () => {
    const blob = new Blob([code], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `code.${language}`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const handleUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (e) => {
        setCode(e.target?.result as string)
      }
      reader.readAsText(file)
    }
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Card className="w-full max-w-md">
          <CardHeader className="text-center">
            <CardTitle>Access Denied</CardTitle>
            <CardDescription>
              Please sign in to access the code editor
            </CardDescription>
          </CardHeader>
          <CardContent className="text-center">
            <Button asChild>
              <a href="/auth">Sign In</a>
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navigation />
      
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Code Editor
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Seamless edit & fix workflow with AI-powered code assistance
          </p>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <Card className="hover:shadow-lg transition-shadow">
            <CardContent className="p-4">
              <div className="flex items-center space-x-3">
                <Lightbulb className="h-5 w-5 text-yellow-500" />
                <div>
                  <p className="text-sm font-medium">Quick Edit</p>
                  <p className="text-xs text-gray-500">Select + Ctrl+L</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card 
            className="hover:shadow-lg transition-shadow cursor-pointer"
            onClick={() => setShowVoiceControls(!showVoiceControls)}
          >
            <CardContent className="p-4">
              <div className="flex items-center space-x-3">
                <div className={`w-5 h-5 rounded-full ${voiceDictation.isListening ? 'bg-green-500 animate-pulse' : 'bg-gray-400'}`}></div>
                <div>
                  <p className="text-sm font-medium">Voice Control</p>
                  <p className="text-xs text-gray-500">
                    {voiceDictation.isListening ? 'Listening...' : 'Click to enable'}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardContent className="p-4">
              <div className="flex items-center space-x-3">
                <CheckCircle className="h-5 w-5 text-green-500" />
                <div>
                  <p className="text-sm font-medium">AI Validation</p>
                  <p className="text-xs text-gray-500">Auto-check code</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardContent className="p-4">
              <div className="flex items-center space-x-3">
                <Settings className="h-5 w-5 text-blue-500" />
                <div>
                  <p className="text-sm font-medium">Smart Suggestions</p>
                  <p className="text-xs text-gray-500">AI-powered tips</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardContent className="p-4">
              <div className="flex items-center space-x-3">
                <Play className="h-5 w-5 text-purple-500" />
                <div>
                  <p className="text-sm font-medium">Run Code</p>
                  <p className="text-xs text-gray-500">Execute & test</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Editor Interface */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="editor">Editor</TabsTrigger>
            <TabsTrigger value="templates">Templates</TabsTrigger>
            <TabsTrigger value="files">Files</TabsTrigger>
            <TabsTrigger value="settings">Settings</TabsTrigger>
          </TabsList>

          <TabsContent value="editor" className="space-y-6">
            {/* Language Selection */}
            <Card>
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <CardTitle className="flex items-center space-x-2">
                    <Code className="h-5 w-5" />
                    <span>Code Editor</span>
                  </CardTitle>
                  
                  <div className="flex items-center space-x-4">
                    <Select value={language} onValueChange={setLanguage}>
                      <SelectTrigger className="w-40">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {supportedLanguages.map((lang) => (
                          <SelectItem key={lang.value} value={lang.value}>
                            {lang.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    
                    <Badge variant="outline">{language}</Badge>
                  </div>
                </div>
              </CardHeader>
              
              <CardContent>
                {useNLPEditor ? (
                  <NLPSmartCodeEditor
                    initialCode={code}
                    language={language}
                    onCodeChange={handleCodeChange}
                    onSave={handleSave}
                    onSmartAnalysis={(analysis) => {
                      console.log('NLP Smart analysis result:', analysis)
                    }}
                    onIntegrationResult={(result) => {
                      console.log('NLP Integration result:', result)
                    }}
                    onNLPInsight={(insight) => {
                      console.log('NLP Insight:', insight)
                    }}
                  />
                ) : useSmartEditor ? (
                  <SmartCodeEditor
                    initialCode={code}
                    language={language}
                    onCodeChange={handleCodeChange}
                    onSave={handleSave}
                    onSmartAnalysis={(analysis) => {
                      console.log('Smart analysis result:', analysis)
                    }}
                    onIntegrationResult={(result) => {
                      console.log('Integration result:', result)
                    }}
                  />
                ) : (
                  <CodeEditor
                    initialCode={code}
                    language={language}
                    onCodeChange={handleCodeChange}
                    onSave={handleSave}
                  />
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="templates" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <FileText className="h-5 w-5" />
                  <span>Code Templates</span>
                </CardTitle>
                <CardDescription>
                  Choose from pre-built templates for {language}
                </CardDescription>
              </CardHeader>
              
              <CardContent>
                {isLoadingTemplates ? (
                  <div className="flex items-center justify-center py-8">
                    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                  </div>
                ) : templates.length === 0 ? (
                  <div className="text-center py-8">
                    <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                      No templates available
                    </h3>
                    <p className="text-gray-600 dark:text-gray-400">
                      No templates found for {language}
                    </p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {templates.map((template, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.1 }}
                      >
                        <Card className="hover:shadow-md transition-shadow cursor-pointer"
                              onClick={() => handleLoadTemplate(template)}>
                          <CardHeader className="pb-3">
                            <CardTitle className="text-sm">{template.name}</CardTitle>
                            <CardDescription className="text-xs">
                              {template.description}
                            </CardDescription>
                          </CardHeader>
                          <CardContent>
                            <pre className="text-xs bg-gray-100 dark:bg-gray-800 p-2 rounded overflow-x-auto">
                              {template.code.substring(0, 100)}...
                            </pre>
                          </CardContent>
                        </Card>
                      </motion.div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="files" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <FileText className="h-5 w-5" />
                  <span>Saved Files</span>
                </CardTitle>
                <CardDescription>
                  Manage your saved code files
                </CardDescription>
              </CardHeader>
              
              <CardContent>
                <div className="space-y-4">
                  {savedFiles.map((file) => (
                    <div key={file.id} className="flex items-center justify-between p-3 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800">
                      <div className="flex items-center space-x-3">
                        <FileText className="h-4 w-4 text-gray-500" />
                        <div>
                          <p className="text-sm font-medium">{file.name}</p>
                          <p className="text-xs text-gray-500">
                            {file.language} • {file.lastModified}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Button variant="outline" size="sm">
                          Open
                        </Button>
                        <Button variant="outline" size="sm">
                          <Download className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="settings" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Settings className="h-5 w-5" />
                  <span>Editor Settings</span>
                </CardTitle>
                <CardDescription>
                  Configure your coding environment
                </CardDescription>
              </CardHeader>
              
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <label className="text-sm font-medium">Smart Code Editor</label>
                      <p className="text-xs text-gray-500">Enable Smart Coding AI integration</p>
                    </div>
                    <Button 
                      variant={useSmartEditor ? "default" : "outline"} 
                      size="sm"
                      onClick={() => setUseSmartEditor(!useSmartEditor)}
                    >
                      {useSmartEditor ? 'Enabled' : 'Disabled'}
                    </Button>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div>
                      <label className="text-sm font-medium">NLP Smart Editor</label>
                      <p className="text-xs text-gray-500">Enable NLP-enhanced Smart Coding AI</p>
                    </div>
                    <Button 
                      variant={useNLPEditor ? "default" : "outline"} 
                      size="sm"
                      onClick={() => setUseNLPEditor(!useNLPEditor)}
                    >
                      {useNLPEditor ? 'Enabled' : 'Disabled'}
                    </Button>
                  </div>
                  <div>
                    <label className="text-sm font-medium">Auto-save</label>
                    <p className="text-xs text-gray-500">Automatically save changes</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium">AI Suggestions</label>
                    <p className="text-xs text-gray-500">Enable AI-powered code suggestions</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium">Syntax Highlighting</label>
                    <p className="text-xs text-gray-500">Color-code your syntax</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Voice Controls */}
            {showVoiceControls && voiceDictation.isSupported && (
              <div className="space-y-4">
                <VoiceAIDashboard />
              </div>
            )}
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

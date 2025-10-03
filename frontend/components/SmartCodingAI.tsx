"use client";

import React, { useState, useEffect, useCallback, useRef } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import { 
  Code, 
  Lightbulb, 
  Zap, 
  BookOpen, 
  Settings, 
  Play, 
  Square, 
  RefreshCw,
  CheckCircle,
  AlertCircle,
  Info,
  Sparkles
} from 'lucide-react';

interface CodeCompletion {
  completion_id: string;
  text: string;
  completion_type: string;
  language: string;
  confidence: number;
  start_line: number;
  end_line: number;
  start_column: number;
  end_column: number;
  description: string;
  documentation?: string;
  parameters?: any[];
  return_type?: string;
  created_at: string;
}

interface CodeSuggestion {
  suggestion_id: string;
  suggestion_type: string;
  text: string;
  language: string;
  confidence: number;
  start_line: number;
  end_line: number;
  start_column: number;
  end_column: number;
  description: string;
  priority: number;
  auto_apply: boolean;
  created_at: string;
}

interface SmartCodingAIProps {
  className?: string;
}

const SmartCodingAI: React.FC<SmartCodingAIProps> = ({ className }) => {
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [completions, setCompletions] = useState<CodeCompletion[]>([]);
  const [suggestions, setSuggestions] = useState<CodeSuggestion[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [cursorPosition, setCursorPosition] = useState({ line: 1, column: 1 });
  const [selectedCompletion, setSelectedCompletion] = useState<CodeCompletion | null>(null);
  const [selectedSuggestion, setSelectedSuggestion] = useState<CodeSuggestion | null>(null);
  const [isActive, setIsActive] = useState(false);
  const [serviceStatus, setServiceStatus] = useState<any>(null);
  
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const debounceRef = useRef<NodeJS.Timeout>();

  const languages = [
    { value: 'python', label: 'Python', extensions: ['.py', '.pyw'] },
    { value: 'javascript', label: 'JavaScript', extensions: ['.js', '.mjs'] },
    { value: 'typescript', label: 'TypeScript', extensions: ['.ts', '.tsx'] },
    { value: 'java', label: 'Java', extensions: ['.java'] },
    { value: 'csharp', label: 'C#', extensions: ['.cs'] },
    { value: 'cpp', label: 'C++', extensions: ['.cpp', '.cc', '.cxx'] },
    { value: 'go', label: 'Go', extensions: ['.go'] },
    { value: 'rust', label: 'Rust', extensions: ['.rs'] },
    { value: 'php', label: 'PHP', extensions: ['.php'] },
    { value: 'ruby', label: 'Ruby', extensions: ['.rb'] },
    { value: 'swift', label: 'Swift', extensions: ['.swift'] },
    { value: 'kotlin', label: 'Kotlin', extensions: ['.kt', '.kts'] },
    { value: 'html', label: 'HTML', extensions: ['.html', '.htm'] },
    { value: 'css', label: 'CSS', extensions: ['.css'] },
    { value: 'sql', label: 'SQL', extensions: ['.sql'] },
    { value: 'yaml', label: 'YAML', extensions: ['.yml', '.yaml'] },
    { value: 'json', label: 'JSON', extensions: ['.json'] },
    { value: 'markdown', label: 'Markdown', extensions: ['.md', '.markdown'] },
  ];

  const completionTypes = [
    { value: 'function', label: 'Function', description: 'Function definitions and calls' },
    { value: 'variable', label: 'Variable', description: 'Variable declarations and references' },
    { value: 'class', label: 'Class', description: 'Class definitions and instantiations' },
    { value: 'import', label: 'Import', description: 'Import statements and modules' },
    { value: 'parameter', label: 'Parameter', description: 'Function parameters and arguments' },
    { value: 'method', label: 'Method', description: 'Method definitions and calls' },
    { value: 'property', label: 'Property', description: 'Property definitions and access' },
    { value: 'type', label: 'Type', description: 'Type definitions and annotations' },
    { value: 'keyword', label: 'Keyword', description: 'Language keywords and reserved words' },
    { value: 'snippet', label: 'Snippet', description: 'Code snippets and templates' },
  ];

  const suggestionTypes = [
    { value: 'completion', label: 'Completion', description: 'Code completion suggestions' },
    { value: 'hint', label: 'Hint', description: 'Helpful hints and tips' },
    { value: 'error_fix', label: 'Error Fix', description: 'Error fixes and corrections' },
    { value: 'refactor', label: 'Refactor', description: 'Code refactoring suggestions' },
    { value: 'optimization', label: 'Optimization', description: 'Performance optimization suggestions' },
    { value: 'documentation', label: 'Documentation', description: 'Documentation improvements' },
  ];

  // Get cursor position from textarea
  const getCursorPosition = useCallback(() => {
    if (!textareaRef.current) return { line: 1, column: 1 };
    
    const textarea = textareaRef.current;
    const text = textarea.value;
    const cursorPos = textarea.selectionStart;
    
    const lines = text.substring(0, cursorPos).split('\n');
    const line = lines.length;
    const column = lines[lines.length - 1].length + 1;
    
    return { line, column };
  }, []);

  // Get code completions
  const getCompletions = useCallback(async () => {
    if (!code.trim()) return;
    
    setIsLoading(true);
    try {
      const position = getCursorPosition();
      const response = await fetch('/api/smart-coding-ai/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          file_path: `temp.${language}`,
          language,
          content: code,
          cursor_line: position.line,
          cursor_column: position.column,
          max_completions: 10,
        }),
      });
      
      if (response.ok) {
        const data = await response.json();
        setCompletions(data.completions || []);
      }
    } catch (error) {
      console.error('Failed to get completions:', error);
    } finally {
      setIsLoading(false);
    }
  }, [code, language, getCursorPosition]);

  // Get code suggestions
  const getSuggestions = useCallback(async () => {
    if (!code.trim()) return;
    
    setIsLoading(true);
    try {
      const position = getCursorPosition();
      const response = await fetch('/api/smart-coding-ai/suggestions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          file_path: `temp.${language}`,
          language,
          content: code,
          cursor_line: position.line,
          cursor_column: position.column,
          max_suggestions: 5,
        }),
      });
      
      if (response.ok) {
        const data = await response.json();
        setSuggestions(data.suggestions || []);
      }
    } catch (error) {
      console.error('Failed to get suggestions:', error);
    } finally {
      setIsLoading(false);
    }
  }, [code, language, getCursorPosition]);

  // Get service status
  const getServiceStatus = useCallback(async () => {
    try {
      const response = await fetch('/api/smart-coding-ai/status');
      if (response.ok) {
        const data = await response.json();
        setServiceStatus(data);
        setIsActive(data.service_active);
      }
    } catch (error) {
      console.error('Failed to get service status:', error);
    }
  }, []);

  // Debounced code analysis
  useEffect(() => {
    if (debounceRef.current) {
      clearTimeout(debounceRef.current);
    }
    
    debounceRef.current = setTimeout(() => {
      if (code.trim()) {
        getCompletions();
        getSuggestions();
      }
    }, 500);
    
    return () => {
      if (debounceRef.current) {
        clearTimeout(debounceRef.current);
      }
    };
  }, [code, getCompletions, getSuggestions]);

  // Get service status on mount
  useEffect(() => {
    getServiceStatus();
  }, [getServiceStatus]);

  // Apply completion
  const applyCompletion = useCallback((completion: CodeCompletion) => {
    if (!textareaRef.current) return;
    
    const textarea = textareaRef.current;
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const newCode = code.substring(0, start) + completion.text + code.substring(end);
    setCode(newCode);
    setSelectedCompletion(completion);
  }, [code]);

  // Apply suggestion
  const applySuggestion = useCallback((suggestion: CodeSuggestion) => {
    if (!textareaRef.current) return;
    
    const textarea = textareaRef.current;
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const newCode = code.substring(0, start) + suggestion.text + code.substring(end);
    setCode(newCode);
    setSelectedSuggestion(suggestion);
  }, [code]);

  // Clear cache
  const clearCache = useCallback(async () => {
    try {
      await fetch('/api/smart-coding-ai/cache/clear', { method: 'POST' });
      setCompletions([]);
      setSuggestions([]);
    } catch (error) {
      console.error('Failed to clear cache:', error);
    }
  }, []);

  const getCompletionIcon = (type: string) => {
    switch (type) {
      case 'function': return <Code className="h-4 w-4" />;
      case 'variable': return <Settings className="h-4 w-4" />;
      case 'class': return <BookOpen className="h-4 w-4" />;
      case 'import': return <Zap className="h-4 w-4" />;
      default: return <Sparkles className="h-4 w-4" />;
    }
  };

  const getSuggestionIcon = (type: string) => {
    switch (type) {
      case 'completion': return <CheckCircle className="h-4 w-4" />;
      case 'hint': return <Lightbulb className="h-4 w-4" />;
      case 'error_fix': return <AlertCircle className="h-4 w-4" />;
      case 'refactor': return <RefreshCw className="h-4 w-4" />;
      case 'optimization': return <Zap className="h-4 w-4" />;
      case 'documentation': return <BookOpen className="h-4 w-4" />;
      default: return <Info className="h-4 w-4" />;
    }
  };

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold flex items-center gap-2">
            <Code className="h-6 w-6" />
            Smart Coding AI
          </h2>
          <p className="text-muted-foreground">
            In-editor code completion and intelligent assistance
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant={isActive ? "default" : "secondary"}>
            {isActive ? "Active" : "Inactive"}
          </Badge>
          <Button variant="outline" size="sm" onClick={clearCache}>
            <RefreshCw className="h-4 w-4 mr-2" />
            Clear Cache
          </Button>
        </div>
      </div>

      {/* Service Status */}
      {serviceStatus && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Service Status</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold">{serviceStatus.supported_languages}</div>
                <div className="text-sm text-muted-foreground">Languages</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold">{serviceStatus.completion_cache_size}</div>
                <div className="text-sm text-muted-foreground">Completions</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold">{serviceStatus.suggestion_cache_size}</div>
                <div className="text-sm text-muted-foreground">Suggestions</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold">{serviceStatus.models_loaded ? "✓" : "✗"}</div>
                <div className="text-sm text-muted-foreground">Models</div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Main Interface */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Code Editor */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Code Editor</CardTitle>
            <CardDescription>
              Write code and get intelligent completions and suggestions
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-2">
              <Select value={language} onValueChange={setLanguage}>
                <SelectTrigger className="w-48">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {languages.map((lang) => (
                    <SelectItem key={lang.value} value={lang.value}>
                      {lang.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <Badge variant="outline">
                Line {cursorPosition.line}, Col {cursorPosition.column}
              </Badge>
            </div>
            
            <Textarea
              ref={textareaRef}
              value={code}
              onChange={(e) => {
                setCode(e.target.value);
                setCursorPosition(getCursorPosition());
              }}
              placeholder={`Enter your ${language} code here...`}
              className="min-h-[400px] font-mono text-sm"
              onKeyDown={(e) => {
                if (e.key === 'Tab' && completions.length > 0) {
                  e.preventDefault();
                  applyCompletion(completions[0]);
                }
              }}
            />
            
            {isLoading && (
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <RefreshCw className="h-4 w-4 animate-spin" />
                Analyzing code...
              </div>
            )}
          </CardContent>
        </Card>

        {/* Completions and Suggestions */}
        <Tabs defaultValue="completions" className="space-y-4">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="completions">
              Completions ({completions.length})
            </TabsTrigger>
            <TabsTrigger value="suggestions">
              Suggestions ({suggestions.length})
            </TabsTrigger>
          </TabsList>
          
          <TabsContent value="completions" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Code Completions</CardTitle>
                <CardDescription>
                  AI-powered code completions for your current context
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ScrollArea className="h-96">
                  {completions.length === 0 ? (
                    <div className="text-center text-muted-foreground py-8">
                      No completions available. Start typing to get suggestions.
                    </div>
                  ) : (
                    <div className="space-y-2">
                      {completions.map((completion) => (
                        <div
                          key={completion.completion_id}
                          className={`p-3 rounded-lg border cursor-pointer transition-colors ${
                            selectedCompletion?.completion_id === completion.completion_id
                              ? 'bg-primary/10 border-primary'
                              : 'hover:bg-muted'
                          }`}
                          onClick={() => applyCompletion(completion)}
                        >
                          <div className="flex items-start gap-3">
                            {getCompletionIcon(completion.completion_type)}
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center gap-2 mb-1">
                                <code className="text-sm font-mono bg-muted px-2 py-1 rounded">
                                  {completion.text}
                                </code>
                                <Badge variant="outline" className="text-xs">
                                  {completion.completion_type}
                                </Badge>
                                <Badge variant="secondary" className="text-xs">
                                  {Math.round(completion.confidence * 100)}%
                                </Badge>
                              </div>
                              <p className="text-sm text-muted-foreground">
                                {completion.description}
                              </p>
                              {completion.documentation && (
                                <p className="text-xs text-muted-foreground mt-1">
                                  {completion.documentation}
                                </p>
                              )}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </ScrollArea>
              </CardContent>
            </Card>
          </TabsContent>
          
          <TabsContent value="suggestions" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Code Suggestions</CardTitle>
                <CardDescription>
                  Intelligent suggestions for code improvements and fixes
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ScrollArea className="h-96">
                  {suggestions.length === 0 ? (
                    <div className="text-center text-muted-foreground py-8">
                      No suggestions available. Write some code to get suggestions.
                    </div>
                  ) : (
                    <div className="space-y-2">
                      {suggestions.map((suggestion) => (
                        <div
                          key={suggestion.suggestion_id}
                          className={`p-3 rounded-lg border cursor-pointer transition-colors ${
                            selectedSuggestion?.suggestion_id === suggestion.suggestion_id
                              ? 'bg-primary/10 border-primary'
                              : 'hover:bg-muted'
                          }`}
                          onClick={() => applySuggestion(suggestion)}
                        >
                          <div className="flex items-start gap-3">
                            {getSuggestionIcon(suggestion.suggestion_type)}
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center gap-2 mb-1">
                                <span className="text-sm font-medium">
                                  {suggestion.text}
                                </span>
                                <Badge variant="outline" className="text-xs">
                                  {suggestion.suggestion_type}
                                </Badge>
                                <Badge variant="secondary" className="text-xs">
                                  Priority {suggestion.priority}
                                </Badge>
                                <Badge variant="secondary" className="text-xs">
                                  {Math.round(suggestion.confidence * 100)}%
                                </Badge>
                              </div>
                              <p className="text-sm text-muted-foreground">
                                {suggestion.description}
                              </p>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </ScrollArea>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default SmartCodingAI;

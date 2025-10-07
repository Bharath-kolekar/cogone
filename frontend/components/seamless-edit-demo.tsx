/**
 * Seamless Edit Demo Component
 * Showcases the Ctrl+L edit workflow with examples
 */

'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  Code, 
  Wand2, 
  Check, 
  X, 
  Copy, 
  Play,
  Lightbulb,
  ArrowRight,
  Zap
} from 'lucide-react'
import { motion } from 'framer-motion'

interface DemoExample {
  id: string
  title: string
  description: string
  originalCode: string
  modifiedCode: string
  instruction: string
  language: string
}

const demoExamples: DemoExample[] = [
  {
    id: '1',
    title: 'Optimize Database Query',
    description: 'Improve performance of a slow database query',
    originalCode: `SELECT * FROM users WHERE age > 18 AND status = 'active'`,
    modifiedCode: `SELECT id, name, email FROM users 
WHERE age > 18 AND status = 'active' 
AND created_at > '2023-01-01'
ORDER BY created_at DESC
LIMIT 100`,
    instruction: 'Add indexing and limit results for better performance',
    language: 'sql'
  },
  {
    id: '2',
    title: 'Add Error Handling',
    description: 'Add proper error handling to an API call',
    originalCode: `async function fetchUser(id) {
  const response = await fetch(\`/api/users/\${id}\`);
  const user = await response.json();
  return user;
}`,
    modifiedCode: `async function fetchUser(id) {
  try {
    const response = await fetch(\`/api/users/\${id}\`);
    
    if (!response.ok) {
      throw new Error(\`HTTP error! status: \${response.status}\`);
    }
    
    const user = await response.json();
    return user;
  } catch (error) {
    console.error('Failed to fetch user:', error);
    throw new Error(\`Unable to fetch user with id \${id}\`);
  }
}`,
    instruction: 'Add try-catch block and proper error handling',
    language: 'javascript'
  },
  {
    id: '3',
    title: 'Convert to TypeScript',
    description: 'Add TypeScript types to JavaScript code',
    originalCode: `function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}`,
    modifiedCode: `interface Item {
  price: number;
  name: string;
  id: string;
}

function calculateTotal(items: Item[]): number {
  return items.reduce((sum: number, item: Item) => sum + item.price, 0);
}`,
    instruction: 'Add TypeScript interfaces and type annotations',
    language: 'typescript'
  },
  {
    id: '4',
    title: 'Add Input Validation',
    description: 'Add validation to a form handler',
    originalCode: `function handleSubmit(formData) {
  const user = {
    name: formData.name,
    email: formData.email
  };
  saveUser(user);
}`,
    modifiedCode: `function handleSubmit(formData) {
  // Validate required fields
  if (!formData.name || !formData.email) {
    throw new Error('Name and email are required');
  }
  
  // Validate email format
  const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
  if (!emailRegex.test(formData.email)) {
    throw new Error('Invalid email format');
  }
  
  const user = {
    name: formData.name.trim(),
    email: formData.email.toLowerCase()
  };
  
  saveUser(user);
}`,
    instruction: 'Add input validation and sanitization',
    language: 'javascript'
  }
]

export function SeamlessEditDemo() {
  const [selectedExample, setSelectedExample] = useState<DemoExample | null>(null)
  const [showModified, setShowModified] = useState(false)

  const handleExampleSelect = (example: DemoExample) => {
    setSelectedExample(example)
    setShowModified(false)
  }

  const handleEditRequest = () => {
    if (selectedExample) {
      setShowModified(true)
    }
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
          Seamless Edit & Fix Workflow
        </h2>
        <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
          Select any code and press <kbd className="px-3 py-1 bg-blue-100 dark:bg-blue-900 rounded text-sm font-mono">Ctrl+L</kbd> to describe changes. 
          Watch AI transform your code instantly.
        </p>
      </div>

      {/* Quick Demo */}
      <Card className="border-blue-200 dark:border-blue-800">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Zap className="h-5 w-5 text-blue-600" />
            <span>Try It Now</span>
          </CardTitle>
          <CardDescription>
            Select code below and press Ctrl+L to see the magic happen
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <pre className="text-sm font-mono text-gray-800 dark:text-gray-200">
{`// Select this code and press Ctrl+L
function getUserData(id) {
  return fetch('/api/users/' + id)
    .then(response => response.json());
}`}
              </pre>
            </div>
            
            <div className="flex items-center space-x-4">
              <Button onClick={handleEditRequest} className="bg-blue-600 hover:bg-blue-700">
                <Wand2 className="h-4 w-4 mr-2" />
                Simulate Ctrl+L
              </Button>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                In the real editor, just select code and press Ctrl+L
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Examples Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {demoExamples.map((example, index) => (
          <motion.div
            key={example.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <Card 
              className={`cursor-pointer transition-all duration-200 hover:shadow-lg ${
                selectedExample?.id === example.id 
                  ? 'ring-2 ring-blue-500 bg-blue-50 dark:bg-blue-900/20' 
                  : 'hover:shadow-md'
              }`}
              onClick={() => handleExampleSelect(example)}
            >
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg">{example.title}</CardTitle>
                  <Badge variant="outline">{example.language}</Badge>
                </div>
                <CardDescription>{example.description}</CardDescription>
              </CardHeader>
              
              <CardContent>
                <div className="space-y-3">
                  <div>
                    <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Original Code:
                    </h4>
                    <pre className="text-xs bg-gray-100 dark:bg-gray-800 p-3 rounded overflow-x-auto">
                      {example.originalCode}
                    </pre>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <ArrowRight className="h-4 w-4 text-gray-400" />
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                      {example.instruction}
                    </span>
                  </div>
                  
                  {selectedExample?.id === example.id && showModified && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      className="space-y-2"
                    >
                      <h4 className="text-sm font-medium text-green-700 dark:text-green-300">
                        Modified Code:
                      </h4>
                      <pre className="text-xs bg-green-50 dark:bg-green-900/20 p-3 rounded overflow-x-auto border border-green-200 dark:border-green-800">
                        {example.modifiedCode}
                      </pre>
                    </motion.div>
                  )}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Features */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Lightbulb className="h-5 w-5 text-yellow-500" />
            <span>Key Features</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center mx-auto mb-3">
                <Wand2 className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="font-medium mb-2">AI-Powered Changes</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Describe what you want and AI will modify your code intelligently
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-green-100 dark:bg-green-900/20 rounded-lg flex items-center justify-center mx-auto mb-3">
                <Check className="h-6 w-6 text-green-600" />
              </div>
              <h3 className="font-medium mb-2">Instant Preview</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                See changes before applying them with side-by-side comparison
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/20 rounded-lg flex items-center justify-center mx-auto mb-3">
                <Code className="h-6 w-6 text-purple-600" />
              </div>
              <h3 className="font-medium mb-2">Multi-Language Support</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Works with JavaScript, Python, TypeScript, and 15+ languages
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Usage Instructions */}
      <Card className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Play className="h-5 w-5 text-blue-600" />
            <span>How to Use</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-start space-x-3">
              <div className="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium">
                1
              </div>
              <div>
                <h4 className="font-medium">Select Code</h4>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Highlight the code you want to modify
                </p>
              </div>
            </div>
            
            <div className="flex items-start space-x-3">
              <div className="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium">
                2
              </div>
              <div>
                <h4 className="font-medium">Press Ctrl+L</h4>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Use the keyboard shortcut to activate edit mode
                </p>
              </div>
            </div>
            
            <div className="flex items-start space-x-3">
              <div className="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium">
                3
              </div>
              <div>
                <h4 className="font-medium">Describe Changes</h4>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Tell AI what you want to change (e.g., "Add error handling")
                </p>
              </div>
            </div>
            
            <div className="flex items-start space-x-3">
              <div className="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium">
                4
              </div>
              <div>
                <h4 className="font-medium">Review & Apply</h4>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Preview the changes and apply them if satisfied
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

/**
 * Type Definitions
 * Extracted from large file for better organization
 */

interface RefactoringRequest {
  id: string
  originalCode: string
  refactoredCode: string
  improvements: RefactoringImprovement[]
  type: 'performance' | 'readability' | 'maintainability' | 'structure' | 'types'
  complexity: 'simple' | 'medium' | 'complex'
  confidence: number
  description: string
  timestamp: Date
}



interface RefactoringImprovement {
  id: string
  type: 'custom-hooks' | 'typescript' | 'performance' | 'structure' | 'readability'
  title: string
  description: string
  code: string
  explanation: string
  impact: 'low' | 'medium' | 'high'
  confidence: number
}



interface RefactoringAIProps {
  onCodeRefactored?: (result: RefactoringRequest) => void
  showRealTimeRefactoring?: boolean
  enableAutoOptimization?: boolean
  className?: string
}



interface ComponentProps {
  userId: string;
  onUserUpdate: (user: any) => void;
}



interface User {
  id: string;
  name: string;
  email: string;
  bio?: string;
  createdAt: string;
  lastLogin: string;
  posts: Post[];
}



interface Post {
  id: string;
  title: string;
  content: string;
  publishedAt: string;
  authorId: string;
}



interface UserStats {
  totalPosts: number;
  joinDate: string;
  isActive: boolean;
}



interface ComponentProps {
  userId: string;
  onUserUpdate: (user: User) => void;
  className?: string;
}



interface FormValues {
  name: string;
  email: string;
  bio: string;
}



interface FormErrors {
  name?: string;
  email?: string;
  bio?: string;
}



interface ComponentProps {
  userId: string;
  onUserUpdate: (user: any) => void;
}



interface User {\n  id: string;\n  name: string;\n  email: string;\n}',
        explanation: 'TypeScript types provide better type safety and IDE support',
        impact: 'high',
        confidence: 0.95
      })
    }
    
    improvements.push({
      id: 'readability',
      type: 'readability',
      title: 'Improve Code Readability',
      description: 'Add comments and improve code structure',
      code: '/**\n * Component description\n * @param props - Component props\n */',
      explanation: 'Better documentation and structure improve maintainability',
      impact: 'medium',
      confidence: 0.85
    })
    
    return improvements
  }



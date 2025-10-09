/**
 * Voice Command Mapper Service
 * Maps voice commands to UI actions and provides command registration
 */

import { useVoiceDictation } from '@/hooks/useVoiceDictation'

export interface VoiceCommandAction {
  id: string
  pattern: RegExp
  action: (params: string[]) => void
  description: string
  category: 'navigation' | 'editor' | 'recording' | 'general' | 'ai' | 'business' | 'system' | 'communication' | 'admin' | 'tools'
  keywords: string[]
}

export class VoiceCommandMapper {
  private commands: Map<string, VoiceCommandAction> = new Map()
  private voiceDictation: ReturnType<typeof useVoiceDictation> | null = null

  constructor(voiceDictation: ReturnType<typeof useVoiceDictation>) {
    this.voiceDictation = voiceDictation
    this.initializeDefaultCommands()
  }

  private initializeDefaultCommands() {
    // Navigation Commands
    this.registerCommand({
      id: 'navigate-dashboard',
      pattern: /go to dashboard|open dashboard|show dashboard/i,
      action: () => this.navigateTo('/dashboard'),
      description: 'Navigate to dashboard',
      category: 'navigation',
      keywords: ['dashboard', 'go', 'open', 'show']
    })

    this.registerCommand({
      id: 'navigate-editor',
      pattern: /go to editor|open editor|show editor|code editor/i,
      action: () => this.navigateTo('/editor'),
      description: 'Navigate to code editor',
      category: 'navigation',
      keywords: ['editor', 'code', 'go', 'open', 'show']
    })

    this.registerCommand({
      id: 'navigate-settings',
      pattern: /go to settings|open settings|show settings/i,
      action: () => this.navigateTo('/settings'),
      description: 'Navigate to settings',
      category: 'navigation',
      keywords: ['settings', 'go', 'open', 'show']
    })

    this.registerCommand({
      id: 'navigate-back',
      pattern: /go back|back|previous|return/i,
      action: () => window.history.back(),
      description: 'Go back to previous page',
      category: 'navigation',
      keywords: ['back', 'previous', 'return']
    })

    // Editor Commands
    this.registerCommand({
      id: 'editor-save',
      pattern: /save file|save|save code/i,
      action: () => this.triggerAction('save-file'),
      description: 'Save current file',
      category: 'editor',
      keywords: ['save', 'file', 'code']
    })

    this.registerCommand({
      id: 'editor-new',
      pattern: /new file|create file|new code/i,
      action: () => this.triggerAction('new-file'),
      description: 'Create new file',
      category: 'editor',
      keywords: ['new', 'create', 'file', 'code']
    })

    this.registerCommand({
      id: 'editor-copy',
      pattern: /copy code|copy|copy all/i,
      action: () => this.triggerAction('copy-code'),
      description: 'Copy code to clipboard',
      category: 'editor',
      keywords: ['copy', 'code', 'all']
    })

    this.registerCommand({
      id: 'editor-undo',
      pattern: /undo|undo changes|revert/i,
      action: () => this.triggerAction('undo'),
      description: 'Undo last change',
      category: 'editor',
      keywords: ['undo', 'revert', 'changes']
    })

    this.registerCommand({
      id: 'editor-redo',
      pattern: /redo|redo changes/i,
      action: () => this.triggerAction('redo'),
      description: 'Redo last undone change',
      category: 'editor',
      keywords: ['redo', 'changes']
    })

    this.registerCommand({
      id: 'editor-format',
      pattern: /format code|format|beautify/i,
      action: () => this.triggerAction('format-code'),
      description: 'Format code',
      category: 'editor',
      keywords: ['format', 'beautify', 'code']
    })

    // Voice Recording Commands
    this.registerCommand({
      id: 'recording-start',
      pattern: /start recording|begin recording|record/i,
      action: () => this.triggerAction('start-recording'),
      description: 'Start voice recording',
      category: 'recording',
      keywords: ['start', 'begin', 'recording', 'record']
    })

    this.registerCommand({
      id: 'recording-stop',
      pattern: /stop recording|end recording|stop/i,
      action: () => this.triggerAction('stop-recording'),
      description: 'Stop voice recording',
      category: 'recording',
      keywords: ['stop', 'end', 'recording']
    })

    this.registerCommand({
      id: 'recording-process',
      pattern: /process audio|process recording|generate app/i,
      action: () => this.triggerAction('process-audio'),
      description: 'Process recorded audio',
      category: 'recording',
      keywords: ['process', 'audio', 'recording', 'generate', 'app']
    })

    // General Commands
    this.registerCommand({
      id: 'general-help',
      pattern: /help|show help|commands/i,
      action: () => this.triggerAction('show-help'),
      description: 'Show help and available commands',
      category: 'general',
      keywords: ['help', 'show', 'commands']
    })

    this.registerCommand({
      id: 'general-clear',
      pattern: /clear|clear all|reset/i,
      action: () => this.triggerAction('clear-all'),
      description: 'Clear current content',
      category: 'general',
      keywords: ['clear', 'all', 'reset']
    })

    this.registerCommand({
      id: 'general-refresh',
      pattern: /refresh|reload|update/i,
      action: () => window.location.reload(),
      description: 'Refresh the page',
      category: 'general',
      keywords: ['refresh', 'reload', 'update']
    })

    this.registerCommand({
      id: 'general-close',
      pattern: /close|exit|quit/i,
      action: () => this.triggerAction('close-modal'),
      description: 'Close current modal or dialog',
      category: 'general',
      keywords: ['close', 'exit', 'quit']
    })

    // Search Commands
    this.registerCommand({
      id: 'search-find',
      pattern: /find (.*)|search for (.*)|look for (.*)/i,
      action: (params) => this.triggerAction('search', params[0]),
      description: 'Search for text',
      category: 'general',
      keywords: ['find', 'search', 'look']
    })

    // Language Commands
    this.registerCommand({
      id: 'language-change',
      pattern: /change language to (.*)|set language to (.*)|switch to (.*)/i,
      action: (params) => this.triggerAction('change-language', params[0]),
      description: 'Change programming language',
      category: 'editor',
      keywords: ['change', 'set', 'switch', 'language']
    })
  }

  public registerCommand(command: VoiceCommandAction) {
    this.commands.set(command.id, command)
    
    if (this.voiceDictation) {
      this.voiceDictation.registerCommand({
        pattern: command.pattern,
        action: command.action,
        description: command.description
      })
    }
  }

  public unregisterCommand(commandId: string) {
    const command = this.commands.get(commandId)
    if (command && this.voiceDictation) {
      this.voiceDictation.unregisterCommand(command.pattern)
      this.commands.delete(commandId)
    }
  }

  public getCommandsByCategory(category: string): VoiceCommandAction[] {
    return Array.from(this.commands.values()).filter(cmd => cmd.category === category)
  }

  public getAllCommands(): VoiceCommandAction[] {
    return Array.from(this.commands.values())
  }

  public searchCommands(query: string): VoiceCommandAction[] {
    const normalizedQuery = query.toLowerCase()
    return Array.from(this.commands.values()).filter(cmd => 
      cmd.description.toLowerCase().includes(normalizedQuery) ||
      cmd.keywords.some(keyword => keyword.toLowerCase().includes(normalizedQuery))
    )
  }

  private navigateTo(path: string) {
    window.location.href = path
  }

  private triggerAction(action: string, params?: string) {
    // Dispatch custom event for components to listen to
    const event = new CustomEvent('voice-command', {
      detail: { action, params }
    })
    window.dispatchEvent(event)
  }

  // Voice feedback methods
  public speak(text: string) {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.rate = 0.9
      utterance.pitch = 1
      speechSynthesis.speak(utterance)
    }
  }

  public speakCommandConfirmation(command: string) {
    this.speak(`Executed: ${command}`)
  }

  public speakError(error: string) {
    this.speak(`Error: ${error}`)
  }
}

// Global voice command mapper instance
let globalVoiceCommandMapper: VoiceCommandMapper | null = null

export function initializeVoiceCommandMapper(voiceDictation: ReturnType<typeof useVoiceDictation>) {
  globalVoiceCommandMapper = new VoiceCommandMapper(voiceDictation)
  return globalVoiceCommandMapper
}

export function getVoiceCommandMapper(): VoiceCommandMapper | null {
  return globalVoiceCommandMapper
}

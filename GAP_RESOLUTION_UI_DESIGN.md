# 🎨 **GAP RESOLUTION UI DESIGN SYSTEM**
## **Comprehensive UI Component Design & Implementation**

---

## **🎯 UI DESIGN PRINCIPLES**

### **Core Design Principles**
- **Proactive**: UI anticipates user needs and provides suggestions
- **Intuitive**: Clear, simple interactions that require minimal learning
- **Responsive**: Works seamlessly across all devices and screen sizes
- **Accessible**: WCAG 2.1 AA compliant with full keyboard navigation
- **Consistent**: Unified design language across all components
- **Real-time**: Live updates and instant feedback

### **Visual Design System**
- **Color Palette**: CognOmega brand colors with status indicators
- **Typography**: Clear, readable fonts with proper hierarchy
- **Spacing**: Consistent 8px grid system
- **Animations**: Smooth, purposeful transitions
- **Icons**: Lucide React icons for consistency

---

## **🧩 CORE UI COMPONENTS**

### **1. Gap Resolution Dialog**
**Primary component for user interaction during gap resolution**

```typescript
// File: frontend/components/gap-resolution/GapResolutionDialog.tsx
import React, { useState, useEffect } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Mic, MicOff, Send, CheckCircle, AlertCircle } from 'lucide-react';
import { VoiceTextResponse } from './VoiceTextResponse';
import { GapVisualization } from './GapVisualization';
import { ClarificationSuggestions } from './ClarificationSuggestions';

interface GapResolutionDialogProps {
  isOpen: boolean;
  onClose: () => void;
  gaps: Gap[];
  suggestions: ClarificationSuggestion[];
  context: RequirementContext;
  onUserDecision: (decision: UserDecision) => void;
  onVoiceResponse: (transcript: string) => void;
  onTextResponse: (text: string) => void;
}

export const GapResolutionDialog: React.FC<GapResolutionDialogProps> = ({
  isOpen,
  onClose,
  gaps,
  suggestions,
  context,
  onUserDecision,
  onVoiceResponse,
  onTextResponse
}) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [userResponses, setUserResponses] = useState<UserResponse[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleUserResponse = async (response: string, type: 'voice' | 'text') => {
    setIsProcessing(true);
    
    try {
      if (type === 'voice') {
        await onVoiceResponse(response);
      } else {
        await onTextResponse(response);
      }
      
      setUserResponses(prev => [...prev, { response, type, timestamp: Date.now() }]);
      setCurrentStep(prev => prev + 1);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleAcceptSuggestion = (suggestion: ClarificationSuggestion) => {
    onUserDecision({
      type: 'accept_suggestion',
      suggestion,
      timestamp: Date.now()
    });
  };

  const progressPercentage = (currentStep / (gaps.length + suggestions.length)) * 100;

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <AlertCircle className="h-5 w-5 text-amber-500" />
            Gap Resolution Required
            <Badge variant="secondary" className="ml-auto">
              {gaps.length} gaps detected
            </Badge>
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-6">
          {/* Progress Indicator */}
          <div className="space-y-2">
            <div className="flex justify-between text-sm text-muted-foreground">
              <span>Resolving gaps...</span>
              <span>{Math.round(progressPercentage)}% complete</span>
            </div>
            <Progress value={progressPercentage} className="h-2" />
          </div>

          {/* Gap Visualization */}
          <GapVisualization gaps={gaps} currentStep={currentStep} />

          {/* Current Gap/Clarification */}
          {gaps[currentStep] && (
            <div className="bg-amber-50 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-800 rounded-lg p-4">
              <div className="flex items-start gap-3">
                <AlertCircle className="h-5 w-5 text-amber-600 dark:text-amber-400 mt-0.5" />
                <div className="flex-1">
                  <h4 className="font-semibold text-amber-900 dark:text-amber-100 mb-2">
                    Gap Detected: {gaps[currentStep].type}
                  </h4>
                  <p className="text-amber-800 dark:text-amber-200 mb-3">
                    {gaps[currentStep].description}
                  </p>
                  <div className="flex gap-2">
                    <Badge variant="outline" className="text-amber-700 border-amber-300">
                      Severity: {gaps[currentStep].severity}
                    </Badge>
                    <Badge variant="outline" className="text-amber-700 border-amber-300">
                      Priority: {gaps[currentStep].priority}
                    </Badge>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Clarification Suggestions */}
          <ClarificationSuggestions 
            suggestions={suggestions.filter((_, index) => index === currentStep)}
            onAccept={handleAcceptSuggestion}
          />

          {/* User Response Interface */}
          <VoiceTextResponse
            onVoiceResponse={(transcript) => handleUserResponse(transcript, 'voice')}
            onTextResponse={(text) => handleUserResponse(text, 'text')}
            isProcessing={isProcessing}
            context={context}
          />

          {/* Action Buttons */}
          <div className="flex justify-between">
            <Button variant="outline" onClick={onClose}>
              Cancel
            </Button>
            <div className="flex gap-2">
              <Button 
                variant="outline" 
                onClick={() => setCurrentStep(prev => Math.max(0, prev - 1))}
                disabled={currentStep === 0}
              >
                Previous
              </Button>
              <Button 
                onClick={() => onClose()}
                disabled={currentStep < gaps.length + suggestions.length}
              >
                <CheckCircle className="h-4 w-4 mr-2" />
                Complete
              </Button>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};
```

### **2. Real-time Gap Detection UI**
**Live gap detection and resolution progress**

```typescript
// File: frontend/components/gap-resolution/RealTimeGapDetection.tsx
import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { AlertCircle, CheckCircle, Clock, Zap } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface RealTimeGapDetectionProps {
  isDetecting: boolean;
  detectedGaps: Gap[];
  resolutionProgress: number;
  suggestions: string[];
  onAcceptSuggestion: (suggestion: string) => void;
  onProvideClarification: (clarification: string) => void;
}

export const RealTimeGapDetection: React.FC<RealTimeGapDetectionProps> = ({
  isDetecting,
  detectedGaps,
  resolutionProgress,
  suggestions,
  onAcceptSuggestion,
  onProvideClarification
}) => {
  const [recentGaps, setRecentGaps] = useState<Gap[]>([]);

  useEffect(() => {
    if (detectedGaps.length > 0) {
      setRecentGaps(prev => {
        const newGaps = detectedGaps.filter(gap => 
          !prev.some(prevGap => prevGap.id === gap.id)
        );
        return [...prev, ...newGaps].slice(-5); // Keep last 5 gaps
      });
    }
  }, [detectedGaps]);

  const getGapIcon = (severity: string) => {
    switch (severity) {
      case 'critical': return <AlertCircle className="h-4 w-4 text-red-500" />;
      case 'high': return <AlertCircle className="h-4 w-4 text-orange-500" />;
      case 'medium': return <AlertCircle className="h-4 w-4 text-yellow-500" />;
      case 'low': return <CheckCircle className="h-4 w-4 text-green-500" />;
      default: return <Clock className="h-4 w-4 text-gray-500" />;
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Zap className="h-5 w-5" />
          Real-time Gap Detection
          {isDetecting && (
            <Badge variant="secondary" className="animate-pulse">
              Detecting...
            </Badge>
          )}
        </CardTitle>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {/* Detection Status */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className={`w-3 h-3 rounded-full ${isDetecting ? 'bg-green-500 animate-pulse' : 'bg-gray-400'}`} />
            <span className="text-sm text-muted-foreground">
              {isDetecting ? 'Active detection' : 'Detection paused'}
            </span>
          </div>
          <Badge variant="outline">
            {detectedGaps.length} gaps found
          </Badge>
        </div>

        {/* Resolution Progress */}
        {resolutionProgress > 0 && (
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span>Resolution Progress</span>
              <span>{Math.round(resolutionProgress)}%</span>
            </div>
            <Progress value={resolutionProgress} className="h-2" />
          </div>
        )}

        {/* Recent Gaps */}
        <div className="space-y-2">
          <h4 className="text-sm font-medium">Recent Gaps</h4>
          <AnimatePresence>
            {recentGaps.map((gap) => (
              <motion.div
                key={gap.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                className="flex items-center gap-3 p-3 bg-muted/50 rounded-lg"
              >
                {getGapIcon(gap.severity)}
                <div className="flex-1">
                  <p className="text-sm font-medium">{gap.type}</p>
                  <p className="text-xs text-muted-foreground">{gap.description}</p>
                </div>
                <Badge 
                  variant={gap.severity === 'critical' ? 'destructive' : 'secondary'}
                  className="text-xs"
                >
                  {gap.severity}
                </Badge>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>

        {/* Quick Suggestions */}
        {suggestions.length > 0 && (
          <div className="space-y-2">
            <h4 className="text-sm font-medium">Quick Suggestions</h4>
            <div className="flex flex-wrap gap-2">
              {suggestions.slice(0, 3).map((suggestion, index) => (
                <Button
                  key={index}
                  variant="outline"
                  size="sm"
                  onClick={() => onAcceptSuggestion(suggestion)}
                  className="text-xs"
                >
                  {suggestion}
                </Button>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};
```

### **3. Voice + Text Response Interface**
**Unified interface for voice and text input**

```typescript
// File: frontend/components/gap-resolution/VoiceTextResponse.tsx
import React, { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent } from '@/components/ui/card';
import { Mic, MicOff, Send, Type, Volume2, VolumeX } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface VoiceTextResponseProps {
  onVoiceResponse: (transcript: string) => void;
  onTextResponse: (text: string) => void;
  isProcessing: boolean;
  context: RequirementContext;
}

export const VoiceTextResponse: React.FC<VoiceTextResponseProps> = ({
  onVoiceResponse,
  onTextResponse,
  isProcessing,
  context
}) => {
  const [inputMode, setInputMode] = useState<'voice' | 'text'>('voice');
  const [isRecording, setIsRecording] = useState(false);
  const [textInput, setTextInput] = useState('');
  const [voiceTranscript, setVoiceTranscript] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [audioLevel, setAudioLevel] = useState(0);
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const animationFrameRef = useRef<number | null>(null);

  const handleModeToggle = (mode: 'voice' | 'text') => {
    setInputMode(mode);
    if (mode === 'voice' && isRecording) {
      stopRecording();
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      
      // Set up audio analysis for visual feedback
      const audioContext = new AudioContext();
      const analyser = audioContext.createAnalyser();
      const microphone = audioContext.createMediaStreamSource(stream);
      
      microphone.connect(analyser);
      analyser.fftSize = 256;
      
      mediaRecorderRef.current = mediaRecorder;
      audioContextRef.current = audioContext;
      analyserRef.current = analyser;
      
      // Start recording
      mediaRecorder.start();
      setIsRecording(true);
      setIsListening(true);
      
      // Start audio level monitoring
      monitorAudioLevel();
      
      // Handle recording end
      mediaRecorder.onstop = async () => {
        // Process audio and get transcript
        // This would integrate with your voice recognition service
        const transcript = await processAudioToTranscript();
        setVoiceTranscript(transcript);
        onVoiceResponse(transcript);
      };
      
    } catch (error) {
      console.error('Error starting recording:', error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      setIsListening(false);
      
      // Stop audio monitoring
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
      
      // Clean up audio context
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }
    }
  };

  const monitorAudioLevel = () => {
    if (!analyserRef.current) return;
    
    const dataArray = new Uint8Array(analyserRef.current.frequencyBinCount);
    
    const updateAudioLevel = () => {
      if (analyserRef.current) {
        analyserRef.current.getByteFrequencyData(dataArray);
        const average = dataArray.reduce((a, b) => a + b) / dataArray.length;
        setAudioLevel(average / 255);
        
        if (isRecording) {
          animationFrameRef.current = requestAnimationFrame(updateAudioLevel);
        }
      }
    };
    
    updateAudioLevel();
  };

  const processAudioToTranscript = async (): Promise<string> => {
    // This would integrate with your voice recognition service
    // For now, return a mock transcript
    return "This is a mock transcript from voice input";
  };

  const handleTextSubmit = () => {
    if (textInput.trim()) {
      onTextResponse(textInput);
      setTextInput('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleTextSubmit();
    }
  };

  return (
    <Card className="w-full">
      <CardContent className="p-4">
        <div className="space-y-4">
          {/* Mode Toggle */}
          <div className="flex items-center gap-2">
            <Button
              variant={inputMode === 'voice' ? 'default' : 'outline'}
              size="sm"
              onClick={() => handleModeToggle('voice')}
              className="flex items-center gap-2"
            >
              {isRecording ? <MicOff className="h-4 w-4" /> : <Mic className="h-4 w-4" />}
              Voice
            </Button>
            <Button
              variant={inputMode === 'text' ? 'default' : 'outline'}
              size="sm"
              onClick={() => handleModeToggle('text')}
              className="flex items-center gap-2"
            >
              <Type className="h-4 w-4" />
              Text
            </Button>
          </div>

          {/* Voice Input */}
          <AnimatePresence mode="wait">
            {inputMode === 'voice' && (
              <motion.div
                key="voice"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="space-y-4"
              >
                {/* Voice Recording Button */}
                <div className="flex justify-center">
                  <Button
                    size="lg"
                    variant={isRecording ? 'destructive' : 'default'}
                    onClick={isRecording ? stopRecording : startRecording}
                    disabled={isProcessing}
                    className="relative"
                  >
                    {isRecording ? (
                      <>
                        <MicOff className="h-6 w-6 mr-2" />
                        Stop Recording
                      </>
                    ) : (
                      <>
                        <Mic className="h-6 w-6 mr-2" />
                        Start Recording
                      </>
                    )}
                  </Button>
                </div>

                {/* Audio Level Indicator */}
                {isRecording && (
                  <div className="flex justify-center">
                    <div className="w-32 h-2 bg-muted rounded-full overflow-hidden">
                      <motion.div
                        className="h-full bg-primary rounded-full"
                        style={{ width: `${audioLevel * 100}%` }}
                        animate={{ width: `${audioLevel * 100}%` }}
                        transition={{ duration: 0.1 }}
                      />
                    </div>
                  </div>
                )}

                {/* Voice Transcript */}
                {voiceTranscript && (
                  <div className="p-3 bg-muted/50 rounded-lg">
                    <p className="text-sm text-muted-foreground mb-1">You said:</p>
                    <p className="font-medium">"{voiceTranscript}"</p>
                  </div>
                )}

                {/* Listening Indicator */}
                {isListening && (
                  <div className="flex items-center justify-center gap-2 text-sm text-muted-foreground">
                    <Volume2 className="h-4 w-4 animate-pulse" />
                    Listening...
                  </div>
                )}
              </motion.div>
            )}
          </AnimatePresence>

          {/* Text Input */}
          <AnimatePresence mode="wait">
            {inputMode === 'text' && (
              <motion.div
                key="text"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="space-y-4"
              >
                <Textarea
                  placeholder="Type your response here..."
                  value={textInput}
                  onChange={(e) => setTextInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  disabled={isProcessing}
                  className="min-h-[100px] resize-none"
                />
                <div className="flex justify-between items-center">
                  <span className="text-xs text-muted-foreground">
                    Press Enter to send, Shift+Enter for new line
                  </span>
                  <Button
                    onClick={handleTextSubmit}
                    disabled={!textInput.trim() || isProcessing}
                    size="sm"
                    className="flex items-center gap-2"
                  >
                    <Send className="h-4 w-4" />
                    Send
                  </Button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Processing Indicator */}
          {isProcessing && (
            <div className="flex items-center justify-center gap-2 text-sm text-muted-foreground">
              <div className="w-4 h-4 border-2 border-primary border-t-transparent rounded-full animate-spin" />
              Processing your response...
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};
```

### **4. Gap Visualization Component**
**Visual representation of detected gaps**

```typescript
// File: frontend/components/gap-resolution/GapVisualization.tsx
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { AlertCircle, CheckCircle, Clock, Zap } from 'lucide-react';
import { motion } from 'framer-motion';

interface GapVisualizationProps {
  gaps: Gap[];
  currentStep: number;
}

export const GapVisualization: React.FC<GapVisualizationProps> = ({
  gaps,
  currentStep
}) => {
  const getGapStatus = (index: number) => {
    if (index < currentStep) return 'resolved';
    if (index === currentStep) return 'current';
    return 'pending';
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'resolved': return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'current': return <Zap className="h-4 w-4 text-blue-500" />;
      case 'pending': return <Clock className="h-4 w-4 text-gray-400" />;
      default: return <AlertCircle className="h-4 w-4 text-gray-400" />;
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'bg-red-500';
      case 'high': return 'bg-orange-500';
      case 'medium': return 'bg-yellow-500';
      case 'low': return 'bg-green-500';
      default: return 'bg-gray-400';
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <AlertCircle className="h-5 w-5" />
          Gap Resolution Progress
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {/* Progress Bar */}
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span>Overall Progress</span>
              <span>{currentStep} of {gaps.length} resolved</span>
            </div>
            <Progress value={(currentStep / gaps.length) * 100} className="h-2" />
          </div>

          {/* Gap Timeline */}
          <div className="space-y-3">
            {gaps.map((gap, index) => {
              const status = getGapStatus(index);
              const isActive = status === 'current';
              
              return (
                <motion.div
                  key={gap.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className={`flex items-center gap-3 p-3 rounded-lg border transition-all ${
                    isActive 
                      ? 'bg-blue-50 dark:bg-blue-950/20 border-blue-200 dark:border-blue-800' 
                      : 'bg-muted/50'
                  }`}
                >
                  {/* Status Icon */}
                  <div className="flex-shrink-0">
                    {getStatusIcon(status)}
                  </div>

                  {/* Gap Info */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <h4 className="font-medium text-sm truncate">{gap.type}</h4>
                      <Badge 
                        variant="outline" 
                        className={`text-xs ${getSeverityColor(gap.severity)} text-white`}
                      >
                        {gap.severity}
                      </Badge>
                    </div>
                    <p className="text-xs text-muted-foreground truncate">
                      {gap.description}
                    </p>
                  </div>

                  {/* Step Number */}
                  <div className="flex-shrink-0">
                    <Badge variant="secondary" className="text-xs">
                      #{index + 1}
                    </Badge>
                  </div>
                </motion.div>
              );
            })}
          </div>

          {/* Summary Stats */}
          <div className="grid grid-cols-3 gap-4 pt-4 border-t">
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {gaps.filter((_, index) => index < currentStep).length}
              </div>
              <div className="text-xs text-muted-foreground">Resolved</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">
                {gaps.filter((_, index) => index === currentStep).length}
              </div>
              <div className="text-xs text-muted-foreground">Current</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-600">
                {gaps.filter((_, index) => index > currentStep).length}
              </div>
              <div className="text-xs text-muted-foreground">Pending</div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
```

### **5. Clarification Suggestions Component**
**Smart suggestions for gap resolution**

```typescript
// File: frontend/components/gap-resolution/ClarificationSuggestions.tsx
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Lightbulb, CheckCircle, ArrowRight } from 'lucide-react';
import { motion } from 'framer-motion';

interface ClarificationSuggestionsProps {
  suggestions: ClarificationSuggestion[];
  onAccept: (suggestion: ClarificationSuggestion) => void;
}

export const ClarificationSuggestions: React.FC<ClarificationSuggestionsProps> = ({
  suggestions,
  onAccept
}) => {
  if (suggestions.length === 0) return null;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Lightbulb className="h-5 w-5 text-yellow-500" />
          Smart Suggestions
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {suggestions.map((suggestion, index) => (
            <motion.div
              key={suggestion.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="p-4 border rounded-lg hover:bg-muted/50 transition-colors"
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <h4 className="font-medium text-sm">{suggestion.title}</h4>
                    <Badge variant="outline" className="text-xs">
                      {suggestion.confidence}% confidence
                    </Badge>
                  </div>
                  <p className="text-sm text-muted-foreground mb-3">
                    {suggestion.description}
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {suggestion.tags.map((tag) => (
                      <Badge key={tag} variant="secondary" className="text-xs">
                        {tag}
                      </Badge>
                    ))}
                  </div>
                </div>
                <Button
                  size="sm"
                  onClick={() => onAccept(suggestion)}
                  className="flex items-center gap-2"
                >
                  <CheckCircle className="h-4 w-4" />
                  Accept
                </Button>
              </div>
            </motion.div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};
```

---

## **🎨 DESIGN SYSTEM SPECIFICATIONS**

### **Color Palette**
```css
:root {
  /* Primary Colors */
  --primary: 221 83% 53%;
  --primary-foreground: 0 0% 98%;
  
  /* Status Colors */
  --success: 142 76% 36%;
  --warning: 38 92% 50%;
  --error: 0 84% 60%;
  --info: 221 83% 53%;
  
  /* Gap Severity Colors */
  --critical: 0 84% 60%;
  --high: 25 95% 53%;
  --medium: 38 92% 50%;
  --low: 142 76% 36%;
  
  /* Background Colors */
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --muted: 210 40% 98%;
  --muted-foreground: 215.4 16.3% 46.9%;
}
```

### **Typography Scale**
```css
/* Headings */
.text-h1 { font-size: 2.25rem; line-height: 2.5rem; font-weight: 700; }
.text-h2 { font-size: 1.875rem; line-height: 2.25rem; font-weight: 600; }
.text-h3 { font-size: 1.5rem; line-height: 2rem; font-weight: 600; }
.text-h4 { font-size: 1.25rem; line-height: 1.75rem; font-weight: 500; }

/* Body Text */
.text-body { font-size: 1rem; line-height: 1.5rem; font-weight: 400; }
.text-body-sm { font-size: 0.875rem; line-height: 1.25rem; font-weight: 400; }
.text-caption { font-size: 0.75rem; line-height: 1rem; font-weight: 400; }
```

### **Spacing Scale**
```css
/* 8px grid system */
.space-1 { margin: 0.25rem; } /* 4px */
.space-2 { margin: 0.5rem; }  /* 8px */
.space-3 { margin: 0.75rem; } /* 12px */
.space-4 { margin: 1rem; }    /* 16px */
.space-6 { margin: 1.5rem; }  /* 24px */
.space-8 { margin: 2rem; }    /* 32px */
```

---

## **📱 RESPONSIVE DESIGN**

### **Breakpoints**
```css
/* Mobile First Approach */
@media (min-width: 640px) { /* sm */ }
@media (min-width: 768px) { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
@media (min-width: 1536px) { /* 2xl */ }
```

### **Mobile Optimizations**
- Touch-friendly button sizes (min 44px)
- Swipe gestures for navigation
- Optimized voice input for mobile
- Reduced cognitive load
- Fast loading times

---

## **♿ ACCESSIBILITY FEATURES**

### **WCAG 2.1 AA Compliance**
- **Color Contrast**: Minimum 4.5:1 ratio
- **Keyboard Navigation**: Full keyboard support
- **Screen Reader**: ARIA labels and descriptions
- **Focus Management**: Clear focus indicators
- **Alternative Text**: Descriptive alt text for images

### **Accessibility Implementation**
```typescript
// Example accessibility implementation
<div
  role="dialog"
  aria-labelledby="gap-resolution-title"
  aria-describedby="gap-resolution-description"
  aria-modal="true"
>
  <h2 id="gap-resolution-title">Gap Resolution Required</h2>
  <p id="gap-resolution-description">
    We've detected some gaps in your requirements. Please provide clarification.
  </p>
</div>
```

---

## **🚀 IMPLEMENTATION READINESS**

### **Component Library Integration**
- ✅ Built on existing UI component library
- ✅ Consistent with CognOmega design system
- ✅ Fully responsive and accessible
- ✅ TypeScript support with proper types
- ✅ Animation support with Framer Motion

### **Next Steps**
1. **Implement Core Components**: Start with GapResolutionDialog
2. **Add Voice Integration**: Integrate with existing voice system
3. **Connect to Backend**: Wire up with gap resolution API
4. **Testing**: Comprehensive testing across devices
5. **Deployment**: Deploy to staging for user testing

**This UI design system provides a comprehensive, user-friendly interface for the Gap Resolution System that ensures excellent user experience while maintaining consistency with CognOmega's design language.**

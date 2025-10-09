"use client";

import React, { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { toast } from '../hooks/use-toast';

interface TwoFactorSetupProps {
  onSetupComplete: () => void;
  onCancel: () => void;
}

interface SetupResponse {
  secret: string;
  qr_code: string;
  backup_codes: string[];
  manual_entry_key: string;
}

export function TwoFactorSetup({ onSetupComplete, onCancel }: TwoFactorSetupProps) {
  const [setupData, setSetupData] = useState<SetupResponse | null>(null);
  const [verificationCode, setVerificationCode] = useState('');
  const [step, setStep] = useState<'setup' | 'verify' | 'backup'>('setup');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    initializeSetup();
  }, []);

  const initializeSetup = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/auth/2fa/setup', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setSetupData(data);
      } else {
        const error = await response.json();
        toast({
          title: "Error",
          description: error.detail || "Failed to initialize 2FA setup",
          variant: "destructive",
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to initialize 2FA setup",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const verifySetup = async () => {
    if (!verificationCode.trim()) {
      toast({
        title: "Error",
        description: "Please enter the verification code",
        variant: "destructive",
      });
      return;
    }

    try {
      setLoading(true);
      const response = await fetch('/api/auth/2fa/verify', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code: verificationCode }),
      });

      if (response.ok) {
        toast({
          title: "Success",
          description: "2FA has been successfully enabled!",
        });
        setStep('backup');
      } else {
        const error = await response.json();
        toast({
          title: "Error",
          description: error.detail || "Invalid verification code",
          variant: "destructive",
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to verify 2FA setup",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const downloadBackupCodes = () => {
    if (!setupData?.backup_codes) return;

    const codesText = setupData.backup_codes.join('\n');
    const blob = new Blob([`Voice-to-App SaaS - Backup Codes\n\n${codesText}\n\nSave these codes in a secure location. Each code can only be used once.`], {
      type: 'text/plain',
    });
    
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'backup-codes.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  if (loading && !setupData) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p>Setting up 2FA...</p>
        </div>
      </div>
    );
  }

  if (!setupData) {
    return (
      <div className="text-center">
        <p className="text-red-600 mb-4">Failed to load 2FA setup data</p>
        <Button onClick={onCancel} variant="outline">Cancel</Button>
      </div>
    );
  }

  return (
    <div className="max-w-md mx-auto space-y-6">
      {step === 'setup' && (
        <Card className="p-6">
          <div className="text-center space-y-4">
            <h2 className="text-2xl font-bold">Setup Two-Factor Authentication</h2>
            
            <div className="space-y-4">
              <p className="text-sm text-gray-600">
                Scan this QR code with your authenticator app (Google Authenticator, Authy, etc.)
              </p>
              
              <div className="flex justify-center">
                <img 
                  src={setupData.qr_code} 
                  alt="2FA QR Code" 
                  className="border rounded-lg"
                />
              </div>
              
              <div className="text-left space-y-2">
                <p className="text-sm font-medium">Or enter this key manually:</p>
                <div className="bg-gray-100 p-3 rounded-lg font-mono text-sm break-all">
                  {setupData.manual_entry_key}
                </div>
              </div>
              
              <p className="text-sm text-gray-600">
                After adding the account, enter the 6-digit code from your authenticator app.
              </p>
            </div>
            
            <div className="flex space-x-3">
              <Button onClick={onCancel} variant="outline" className="flex-1">
                Cancel
              </Button>
              <Button 
                onClick={() => setStep('verify')} 
                className="flex-1"
                disabled={loading}
              >
                Next
              </Button>
            </div>
          </div>
        </Card>
      )}

      {step === 'verify' && (
        <Card className="p-6">
          <div className="text-center space-y-4">
            <h2 className="text-2xl font-bold">Verify Setup</h2>
            
            <div className="space-y-4">
              <p className="text-sm text-gray-600">
                Enter the 6-digit code from your authenticator app to complete the setup.
              </p>
              
              <input
                type="text"
                value={verificationCode}
                onChange={(e) => setVerificationCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                placeholder="000000"
                className="w-full p-3 text-center text-2xl font-mono border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                maxLength={6}
              />
            </div>
            
            <div className="flex space-x-3">
              <Button 
                onClick={() => setStep('setup')} 
                variant="outline" 
                className="flex-1"
                disabled={loading}
              >
                Back
              </Button>
              <Button 
                onClick={verifySetup} 
                className="flex-1"
                disabled={loading || verificationCode.length !== 6}
              >
                {loading ? 'Verifying...' : 'Verify'}
              </Button>
            </div>
          </div>
        </Card>
      )}

      {step === 'backup' && (
        <Card className="p-6">
          <div className="text-center space-y-4">
            <div className="text-green-600">
              <svg className="w-12 h-12 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              <h2 className="text-2xl font-bold text-green-600">2FA Enabled Successfully!</h2>
            </div>
            
            <div className="text-left space-y-4">
              <p className="text-sm text-gray-600">
                Save these backup codes in a secure location. Each code can only be used once if you lose access to your authenticator app.
              </p>
              
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <div className="grid grid-cols-2 gap-2 font-mono text-sm">
                  {setupData.backup_codes.map((code, index) => (
                    <div key={index} className="bg-white p-2 rounded border text-center">
                      {code}
                    </div>
                  ))}
                </div>
              </div>
              
              <Button 
                onClick={downloadBackupCodes}
                variant="outline"
                className="w-full"
              >
                Download Backup Codes
              </Button>
            </div>
            
            <Button 
              onClick={onSetupComplete} 
              className="w-full"
            >
              Complete Setup
            </Button>
          </div>
        </Card>
      )}
    </div>
  );
}

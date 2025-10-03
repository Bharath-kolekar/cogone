"use client";

import React, { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { toast } from '../hooks/use-toast';
import { TwoFactorSetup } from './TwoFactorSetup';

interface TwoFactorStatus {
  enabled: boolean;
  backup_codes_count: number;
  verified_at?: string;
  created_at?: string;
}

export function TwoFactorSettings() {
  const [status, setStatus] = useState<TwoFactorStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [showSetup, setShowSetup] = useState(false);

  useEffect(() => {
    fetchStatus();
  }, []);

  const fetchStatus = async () => {
    try {
      const response = await fetch('/api/auth/2fa/status', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setStatus(data);
      } else {
        toast({
          title: "Error",
          description: "Failed to fetch 2FA status",
          variant: "destructive",
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to fetch 2FA status",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const disable2FA = async () => {
    if (!confirm('Are you sure you want to disable 2FA? This will make your account less secure.')) {
      return;
    }

    try {
      setLoading(true);
      const response = await fetch('/api/auth/2fa/disable', {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
      });

      if (response.ok) {
        toast({
          title: "Success",
          description: "2FA has been disabled",
        });
        await fetchStatus();
      } else {
        const error = await response.json();
        toast({
          title: "Error",
          description: error.detail || "Failed to disable 2FA",
          variant: "destructive",
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to disable 2FA",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const regenerateBackupCodes = async () => {
    if (!confirm('Are you sure you want to regenerate backup codes? Your old codes will no longer work.')) {
      return;
    }

    try {
      setLoading(true);
      const response = await fetch('/api/auth/2fa/backup-codes', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        toast({
          title: "Success",
          description: "New backup codes generated",
        });
        
        // Show the new backup codes
        const codesText = data.backup_codes.join('\n');
        const blob = new Blob([`Voice-to-App SaaS - New Backup Codes\n\n${codesText}\n\nSave these codes in a secure location. Each code can only be used once.`], {
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
        
        await fetchStatus();
      } else {
        const error = await response.json();
        toast({
          title: "Error",
          description: error.detail || "Failed to regenerate backup codes",
          variant: "destructive",
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to regenerate backup codes",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading && !status) {
    return (
      <div className="flex items-center justify-center min-h-[200px]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (showSetup) {
    return (
      <TwoFactorSetup
        onSetupComplete={() => {
          setShowSetup(false);
          fetchStatus();
        }}
        onCancel={() => setShowSetup(false)}
      />
    );
  }

  return (
    <Card className="p-6">
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-bold mb-2">Two-Factor Authentication</h2>
          <p className="text-gray-600">
            Add an extra layer of security to your account with 2FA.
          </p>
        </div>

        {status && (
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div>
                <h3 className="font-medium">Status</h3>
                <p className="text-sm text-gray-600">
                  {status.enabled ? 'Enabled' : 'Disabled'}
                </p>
              </div>
              <div className={`px-3 py-1 rounded-full text-sm font-medium ${
                status.enabled 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-gray-100 text-gray-800'
              }`}>
                {status.enabled ? 'Active' : 'Inactive'}
              </div>
            </div>

            {status.enabled && (
              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-4 bg-blue-50 rounded-lg">
                    <h4 className="font-medium text-blue-900">Backup Codes</h4>
                    <p className="text-sm text-blue-700">
                      {status.backup_codes_count} codes remaining
                    </p>
                  </div>
                  
                  <div className="p-4 bg-gray-50 rounded-lg">
                    <h4 className="font-medium">Enabled Since</h4>
                    <p className="text-sm text-gray-600">
                      {status.verified_at ? new Date(status.verified_at).toLocaleDateString() : 'Unknown'}
                    </p>
                  </div>
                </div>

                <div className="flex flex-col sm:flex-row gap-3">
                  <Button 
                    onClick={regenerateBackupCodes}
                    variant="outline"
                    disabled={loading}
                    className="flex-1"
                  >
                    {loading ? 'Generating...' : 'Regenerate Backup Codes'}
                  </Button>
                  
                  <Button 
                    onClick={disable2FA}
                    variant="destructive"
                    disabled={loading}
                    className="flex-1"
                  >
                    {loading ? 'Disabling...' : 'Disable 2FA'}
                  </Button>
                </div>
              </div>
            )}

            {!status.enabled && (
              <div className="text-center py-8">
                <div className="mb-4">
                  <svg className="w-16 h-16 mx-auto text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <h3 className="text-lg font-medium mb-2">Secure your account</h3>
                <p className="text-gray-600 mb-4">
                  Enable 2FA to protect your account with an additional layer of security.
                </p>
                <Button 
                  onClick={() => setShowSetup(true)}
                  disabled={loading}
                >
                  Enable 2FA
                </Button>
              </div>
            )}
          </div>
        )}
      </div>
    </Card>
  );
}

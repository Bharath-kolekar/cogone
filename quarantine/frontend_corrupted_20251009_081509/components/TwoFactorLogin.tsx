"use client";

import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { toast } from '../hooks/use-toast';

interface TwoFactorLoginProps {
  userId: string;
  onSuccess: (tokens: { access_token: string; refresh_token: string }) => void;
  onCancel: () => void;
}

export function TwoFactorLogin({ userId, onSuccess, onCancel }: TwoFactorLoginProps) {
  const [code, setCode] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (code.length !== 6) {
      toast({
        title: "Error",
        description: "Please enter a 6-digit code",
        variant: "destructive",
      });
      return;
    }

    try {
      setLoading(true);
      const response = await fetch('/api/auth/2fa/verify-login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          code: code,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          toast({
            title: "Success",
            description: "2FA verification successful",
          });
          onSuccess({
            access_token: data.access_token,
            refresh_token: data.refresh_token,
          });
        } else {
          toast({
            title: "Error",
            description: data.message || "Invalid 2FA code",
            variant: "destructive",
          });
        }
      } else {
        const error = await response.json();
        toast({
          title: "Error",
          description: error.detail || "2FA verification failed",
          variant: "destructive",
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "2FA verification failed",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="p-6 max-w-md mx-auto">
      <div className="text-center space-y-6">
        <div>
          <h2 className="text-2xl font-bold mb-2">Two-Factor Authentication</h2>
          <p className="text-gray-600">
            Enter the 6-digit code from your authenticator app
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <input
              type="text"
              value={code}
              onChange={(e) => setCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
              placeholder="000000"
              className="w-full p-4 text-center text-2xl font-mono border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              maxLength={6}
              autoFocus
            />
          </div>

          <div className="space-y-3">
            <Button
              type="submit"
              className="w-full"
              disabled={loading || code.length !== 6}
            >
              {loading ? 'Verifying...' : 'Verify Code'}
            </Button>

            <Button
              type="button"
              onClick={onCancel}
              variant="outline"
              className="w-full"
              disabled={loading}
            >
              Cancel
            </Button>
          </div>
        </form>

        <div className="text-sm text-gray-500">
          <p>
            Having trouble? You can also use one of your backup codes.
          </p>
        </div>
      </div>
    </Card>
  );
}

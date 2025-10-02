"use client";

import React, { useEffect, useState } from 'react';
import { TwoFactorSettings } from '../../components/TwoFactorSettings';
import { Button } from '../../components/ui/button';
import { Card } from '../../components/ui/card';
import { toast } from '../../components/ui/use-toast';

interface User {
  id: string;
  email: string;
  full_name?: string;
  subscription_tier: string;
}

export default function Settings() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      window.location.href = '/auth';
      return;
    }

    fetchUserProfile();
  }, []);

  const fetchUserProfile = async () => {
    try {
      const response = await fetch('/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      } else {
        toast({
          title: "Error",
          description: "Failed to fetch user profile",
          variant: "destructive",
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to fetch user profile",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    window.location.href = '/auth';
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
          <p className="mt-2 text-gray-600">
            Manage your account settings and security preferences.
          </p>
        </div>

        <div className="space-y-8">
          {/* User Profile Section */}
          <Card className="p-6">
            <div className="space-y-6">
              <div>
                <h2 className="text-xl font-semibold mb-2">Profile Information</h2>
                <p className="text-gray-600">
                  Manage your personal information and account details.
                </p>
              </div>

              {user && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Email Address
                    </label>
                    <p className="text-gray-900">{user.email}</p>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Full Name
                    </label>
                    <p className="text-gray-900">{user.full_name || 'Not provided'}</p>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Subscription Tier
                    </label>
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      user.subscription_tier === 'free' 
                        ? 'bg-gray-100 text-gray-800' 
                        : user.subscription_tier === 'pro'
                        ? 'bg-blue-100 text-blue-800'
                        : 'bg-purple-100 text-purple-800'
                    }`}>
                      {user.subscription_tier.toUpperCase()}
                    </span>
                  </div>
                </div>
              )}

              <div className="pt-4 border-t">
                <Button variant="outline">
                  Edit Profile
                </Button>
              </div>
            </div>
          </Card>

          {/* Two-Factor Authentication Section */}
          <TwoFactorSettings />

          {/* Security Section */}
          <Card className="p-6">
            <div className="space-y-6">
              <div>
                <h2 className="text-xl font-semibold mb-2">Security</h2>
                <p className="text-gray-600">
                  Manage your account security settings.
                </p>
              </div>

              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div>
                    <h3 className="font-medium">Change Password</h3>
                    <p className="text-sm text-gray-600">
                      Update your account password
                    </p>
                  </div>
                  <Button variant="outline">
                    Change
                  </Button>
                </div>

                <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div>
                    <h3 className="font-medium">Active Sessions</h3>
                    <p className="text-sm text-gray-600">
                      Manage your active login sessions
                    </p>
                  </div>
                  <Button variant="outline">
                    Manage
                  </Button>
                </div>
              </div>
            </div>
          </Card>

          {/* Account Actions */}
          <Card className="p-6">
            <div className="space-y-6">
              <div>
                <h2 className="text-xl font-semibold mb-2">Account Actions</h2>
                <p className="text-gray-600">
                  Manage your account and data.
                </p>
              </div>

              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-red-50 rounded-lg border border-red-200">
                  <div>
                    <h3 className="font-medium text-red-900">Sign Out</h3>
                    <p className="text-sm text-red-700">
                      Sign out of your account on this device
                    </p>
                  </div>
                  <Button variant="destructive" onClick={handleLogout}>
                    Sign Out
                  </Button>
                </div>

                <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div>
                    <h3 className="font-medium">Download Data</h3>
                    <p className="text-sm text-gray-600">
                      Download a copy of your data
                    </p>
                  </div>
                  <Button variant="outline">
                    Download
                  </Button>
                </div>

                <div className="flex items-center justify-between p-4 bg-red-50 rounded-lg border border-red-200">
                  <div>
                    <h3 className="font-medium text-red-900">Delete Account</h3>
                    <p className="text-sm text-red-700">
                      Permanently delete your account and all data
                    </p>
                  </div>
                  <Button variant="destructive">
                    Delete Account
                  </Button>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}

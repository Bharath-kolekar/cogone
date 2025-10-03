-- Voice-to-App SaaS Platform Database Schema
-- Supabase PostgreSQL with Row-Level Security

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create custom types
CREATE TYPE subscription_tier AS ENUM ('free', 'pro', 'enterprise');
CREATE TYPE subscription_status AS ENUM ('active', 'cancelled', 'expired', 'pending');
CREATE TYPE payment_status AS ENUM ('pending', 'completed', 'failed', 'refunded', 'cancelled');
CREATE TYPE payment_provider AS ENUM ('razorpay', 'paypal', 'google_pay');
CREATE TYPE app_status AS ENUM ('generating', 'completed', 'failed', 'deployed');
CREATE TYPE oauth_provider AS ENUM ('google', 'github', 'facebook');
CREATE TYPE otp_type AS ENUM ('email', 'mobile');

-- Users table (extends Supabase auth.users)
CREATE TABLE users (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    full_name VARCHAR(255),
    avatar_url TEXT,
    signup_via oauth_provider DEFAULT 'google',
    subscription_tier subscription_tier DEFAULT 'free',
    subscription_status subscription_status DEFAULT 'active',
    points INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    referral_code VARCHAR(20) UNIQUE,
    referred_by UUID REFERENCES users(id),
    preferred_language VARCHAR(5) DEFAULT 'en',
    country_code VARCHAR(3) DEFAULT 'IN',
    timezone VARCHAR(50) DEFAULT 'Asia/Kolkata',
    is_active BOOLEAN DEFAULT true,
    last_login_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User OAuth accounts
CREATE TABLE user_oauth_accounts (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    provider oauth_provider NOT NULL,
    provider_account_id VARCHAR(255) NOT NULL,
    access_token TEXT,
    refresh_token TEXT,
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(provider, provider_account_id)
);

-- Payments table
CREATE TABLE payments (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    provider payment_provider NOT NULL,
    provider_payment_id VARCHAR(255) UNIQUE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'INR',
    status payment_status DEFAULT 'pending',
    metadata JSONB DEFAULT '{}',
    webhook_data JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Subscriptions table
CREATE TABLE subscriptions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    plan_id VARCHAR(50) NOT NULL,
    status subscription_status DEFAULT 'pending',
    period_start TIMESTAMP WITH TIME ZONE,
    period_end TIMESTAMP WITH TIME ZONE,
    razorpay_subscription_id VARCHAR(255),
    paypal_subscription_id VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Generated apps table
CREATE TABLE generated_apps (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    voice_command TEXT NOT NULL,
    repo_url TEXT,
    zip_url TEXT,
    preview_url TEXT,
    status app_status DEFAULT 'generating',
    metadata JSONB DEFAULT '{}',
    generation_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Voice commands table
CREATE TABLE voice_commands (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    transcript TEXT NOT NULL,
    language VARCHAR(5) DEFAULT 'en',
    confidence DECIMAL(3,2),
    intent JSONB DEFAULT '{}',
    processed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User points table (for gamification)
CREATE TABLE user_points (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    points INTEGER NOT NULL,
    reason VARCHAR(100) NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User achievements table
CREATE TABLE user_achievements (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    achievement_type VARCHAR(50) NOT NULL,
    achievement_data JSONB DEFAULT '{}',
    unlocked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, achievement_type)
);

-- Referrals table
CREATE TABLE referrals (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    referrer_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    referee_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    referral_code VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    points_awarded INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(referrer_id, referee_id)
);

-- Templates marketplace
CREATE TABLE app_templates (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    creator_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    tags TEXT[],
    preview_image_url TEXT,
    template_data JSONB NOT NULL,
    is_public BOOLEAN DEFAULT false,
    is_featured BOOLEAN DEFAULT false,
    download_count INTEGER DEFAULT 0,
    rating DECIMAL(3,2) DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Template reviews
CREATE TABLE template_reviews (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    template_id UUID REFERENCES app_templates(id) ON DELETE CASCADE NOT NULL,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(template_id, user_id)
);

-- OTP verification table
CREATE TABLE otp_verifications (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    email VARCHAR(255),
    phone VARCHAR(20),
    otp_type otp_type NOT NULL,
    otp_code VARCHAR(10) NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_used BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Two-Factor Authentication table
CREATE TABLE user_2fa (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE UNIQUE NOT NULL,
    totp_secret VARCHAR(255) NOT NULL,
    backup_codes TEXT[] DEFAULT '{}',
    is_enabled BOOLEAN DEFAULT false,
    verified_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Rate limiting table
CREATE TABLE rate_limits (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    ip_address INET,
    endpoint VARCHAR(100) NOT NULL,
    request_count INTEGER DEFAULT 1,
    window_start TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, endpoint, window_start),
    UNIQUE(ip_address, endpoint, window_start)
);

-- Admin users table
CREATE TABLE admin_users (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    role VARCHAR(50) DEFAULT 'admin',
    permissions JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_phone ON users(phone);
CREATE INDEX idx_users_referral_code ON users(referral_code);
CREATE INDEX idx_users_subscription_tier ON users(subscription_tier);
CREATE INDEX idx_payments_user_id ON payments(user_id);
CREATE INDEX idx_payments_provider ON payments(provider);
CREATE INDEX idx_payments_status ON payments(status);
CREATE INDEX idx_generated_apps_user_id ON generated_apps(user_id);
CREATE INDEX idx_generated_apps_status ON generated_apps(status);
CREATE INDEX idx_voice_commands_user_id ON voice_commands(user_id);
CREATE INDEX idx_user_points_user_id ON user_points(user_id);
CREATE INDEX idx_referrals_referrer_id ON referrals(referrer_id);
CREATE INDEX idx_referrals_referee_id ON referrals(referee_id);
CREATE INDEX idx_app_templates_category ON app_templates(category);
CREATE INDEX idx_app_templates_is_public ON app_templates(is_public);
CREATE INDEX idx_otp_verifications_email ON otp_verifications(email);
CREATE INDEX idx_otp_verifications_phone ON otp_verifications(phone);
CREATE INDEX idx_user_2fa_user_id ON user_2fa(user_id);
CREATE INDEX idx_user_2fa_enabled ON user_2fa(is_enabled);
CREATE INDEX idx_rate_limits_user_id ON rate_limits(user_id);
CREATE INDEX idx_rate_limits_ip_address ON rate_limits(ip_address);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add updated_at triggers
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_payments_updated_at BEFORE UPDATE ON payments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_subscriptions_updated_at BEFORE UPDATE ON subscriptions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_generated_apps_updated_at BEFORE UPDATE ON generated_apps FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_app_templates_updated_at BEFORE UPDATE ON app_templates FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_user_2fa_updated_at BEFORE UPDATE ON user_2fa FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Row Level Security (RLS) Policies

-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_oauth_accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE payments ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE generated_apps ENABLE ROW LEVEL SECURITY;
ALTER TABLE voice_commands ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_points ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE referrals ENABLE ROW LEVEL SECURITY;
ALTER TABLE app_templates ENABLE ROW LEVEL SECURITY;
ALTER TABLE template_reviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE otp_verifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_2fa ENABLE ROW LEVEL SECURITY;
ALTER TABLE rate_limits ENABLE ROW LEVEL SECURITY;

-- Users policies
CREATE POLICY "Users can view own profile" ON users FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON users FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Users can insert own profile" ON users FOR INSERT WITH CHECK (auth.uid() = id);

-- User OAuth accounts policies
CREATE POLICY "Users can view own OAuth accounts" ON user_oauth_accounts FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own OAuth accounts" ON user_oauth_accounts FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Payments policies
CREATE POLICY "Users can view own payments" ON payments FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Service role can manage all payments" ON payments FOR ALL USING (auth.role() = 'service_role');

-- Subscriptions policies
CREATE POLICY "Users can view own subscriptions" ON subscriptions FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Service role can manage all subscriptions" ON subscriptions FOR ALL USING (auth.role() = 'service_role');

-- Generated apps policies
CREATE POLICY "Users can view own apps" ON generated_apps FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own apps" ON generated_apps FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own apps" ON generated_apps FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Public can view public apps" ON generated_apps FOR SELECT USING (status = 'completed' AND metadata->>'is_public' = 'true');

-- Voice commands policies
CREATE POLICY "Users can view own voice commands" ON voice_commands FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own voice commands" ON voice_commands FOR INSERT WITH CHECK (auth.uid() = user_id);

-- User points policies
CREATE POLICY "Users can view own points" ON user_points FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Service role can manage all points" ON user_points FOR ALL USING (auth.role() = 'service_role');

-- User achievements policies
CREATE POLICY "Users can view own achievements" ON user_achievements FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Service role can manage all achievements" ON user_achievements FOR ALL USING (auth.role() = 'service_role');

-- Referrals policies
CREATE POLICY "Users can view own referrals" ON referrals FOR SELECT USING (auth.uid() = referrer_id OR auth.uid() = referee_id);
CREATE POLICY "Service role can manage all referrals" ON referrals FOR ALL USING (auth.role() = 'service_role');

-- App templates policies
CREATE POLICY "Public can view public templates" ON app_templates FOR SELECT USING (is_public = true);
CREATE POLICY "Users can view own templates" ON app_templates FOR SELECT USING (auth.uid() = creator_id);
CREATE POLICY "Users can insert own templates" ON app_templates FOR INSERT WITH CHECK (auth.uid() = creator_id);
CREATE POLICY "Users can update own templates" ON app_templates FOR UPDATE USING (auth.uid() = creator_id);

-- Template reviews policies
CREATE POLICY "Public can view template reviews" ON template_reviews FOR SELECT USING (true);
CREATE POLICY "Users can insert own reviews" ON template_reviews FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own reviews" ON template_reviews FOR UPDATE USING (auth.uid() = user_id);

-- OTP verifications policies
CREATE POLICY "Service role can manage OTP verifications" ON otp_verifications FOR ALL USING (auth.role() = 'service_role');

-- User 2FA policies
CREATE POLICY "Users can view own 2FA settings" ON user_2fa FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can manage own 2FA settings" ON user_2fa FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Service role can manage all 2FA settings" ON user_2fa FOR ALL USING (auth.role() = 'service_role');

-- Rate limits policies
CREATE POLICY "Service role can manage rate limits" ON rate_limits FOR ALL USING (auth.role() = 'service_role');

-- Create functions for common operations

-- Function to generate referral code
CREATE OR REPLACE FUNCTION generate_referral_code()
RETURNS TEXT AS $$
DECLARE
    code TEXT;
    exists BOOLEAN;
BEGIN
    LOOP
        code := upper(substring(md5(random()::text) from 1 for 8));
        SELECT EXISTS(SELECT 1 FROM users WHERE referral_code = code) INTO exists;
        IF NOT exists THEN
            EXIT;
        END IF;
    END LOOP;
    RETURN code;
END;
$$ LANGUAGE plpgsql;

-- Function to award points
CREATE OR REPLACE FUNCTION award_points(
    p_user_id UUID,
    p_points INTEGER,
    p_reason VARCHAR(100),
    p_metadata JSONB DEFAULT '{}'
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO user_points (user_id, points, reason, metadata)
    VALUES (p_user_id, p_points, p_reason, p_metadata);
    
    UPDATE users 
    SET points = points + p_points,
        level = CASE 
            WHEN points + p_points >= 1000 THEN 3
            WHEN points + p_points >= 500 THEN 2
            ELSE 1
        END
    WHERE id = p_user_id;
END;
$$ LANGUAGE plpgsql;

-- Function to check rate limit
CREATE OR REPLACE FUNCTION check_rate_limit(
    p_user_id UUID,
    p_endpoint VARCHAR(100),
    p_limit INTEGER DEFAULT 60,
    p_window_minutes INTEGER DEFAULT 1
)
RETURNS BOOLEAN AS $$
DECLARE
    current_count INTEGER;
BEGIN
    SELECT COALESCE(SUM(request_count), 0) INTO current_count
    FROM rate_limits
    WHERE user_id = p_user_id 
    AND endpoint = p_endpoint
    AND window_start > NOW() - make_interval(mins := p_window_minutes);
    
    RETURN current_count < p_limit;
END;
$$ LANGUAGE plpgsql;

-- Insert default admin user (replace with actual admin user ID)
-- INSERT INTO admin_users (user_id, role, permissions) 
-- VALUES ('your-admin-user-id', 'super_admin', '{"all": true}');

-- Create a view for user statistics
CREATE VIEW user_stats AS
SELECT 
    u.id,
    u.email,
    u.full_name,
    u.points,
    u.level,
    u.subscription_tier,
    COUNT(DISTINCT ga.id) as apps_created,
    COUNT(DISTINCT p.id) as payments_count,
    COUNT(DISTINCT r.id) as referrals_count,
    u.created_at
FROM users u
LEFT JOIN generated_apps ga ON u.id = ga.user_id
LEFT JOIN payments p ON u.id = p.user_id
LEFT JOIN referrals r ON u.id = r.referrer_id
GROUP BY u.id, u.email, u.full_name, u.points, u.level, u.subscription_tier, u.created_at;

-- ===== AI Agent System Tables =====

-- AI Agents table
CREATE TABLE ai_agents (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    type VARCHAR(50) NOT NULL DEFAULT 'personal_assistant',
    status VARCHAR(20) DEFAULT 'inactive',
    priority VARCHAR(20) DEFAULT 'medium',
    capabilities TEXT[] DEFAULT '{}',
    config JSONB DEFAULT '{}',
    memory JSONB DEFAULT '{}',
    metrics JSONB DEFAULT '{}',
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    team_id UUID,
    is_public BOOLEAN DEFAULT false,
    use_local_models BOOLEAN DEFAULT true,
    fallback_providers TEXT[] DEFAULT '{}',
    resource_limits JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_active TIMESTAMP WITH TIME ZONE
);

-- AI Agent Tasks table
CREATE TABLE ai_agent_tasks (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    agent_id UUID REFERENCES ai_agents(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    input_data JSONB DEFAULT '{}',
    expected_output TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    priority VARCHAR(20) DEFAULT 'medium',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    scheduled_for TIMESTAMP WITH TIME ZONE,
    output_data JSONB DEFAULT '{}',
    error_message TEXT,
    execution_time FLOAT,
    use_local_processing BOOLEAN DEFAULT true,
    max_cost DECIMAL(10,4) DEFAULT 0.0,
    resource_usage JSONB DEFAULT '{}'
);

-- AI Agent Interactions table
CREATE TABLE ai_agent_interactions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    agent_id UUID REFERENCES ai_agents(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    task_id UUID REFERENCES ai_agent_tasks(id) ON DELETE SET NULL,
    input_message TEXT NOT NULL,
    output_message TEXT NOT NULL,
    interaction_type VARCHAR(50) DEFAULT 'conversation',
    context_data JSONB DEFAULT '{}',
    session_id VARCHAR(255),
    response_time FLOAT DEFAULT 0.0,
    tokens_used INTEGER DEFAULT 0,
    cost DECIMAL(10,4) DEFAULT 0.0,
    user_rating INTEGER CHECK (user_rating >= 1 AND user_rating <= 5),
    user_feedback TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- AI Agent Workflows table
CREATE TABLE ai_agent_workflows (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    trigger_type VARCHAR(50) DEFAULT 'manual',
    trigger_config JSONB DEFAULT '{}',
    steps JSONB DEFAULT '[]',
    primary_agent_id UUID REFERENCES ai_agents(id) ON DELETE CASCADE,
    fallback_agent_ids UUID[] DEFAULT '{}',
    max_concurrent INTEGER DEFAULT 1,
    timeout INTEGER DEFAULT 300,
    retry_policy JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT true,
    last_run TIMESTAMP WITH TIME ZONE,
    next_run TIMESTAMP WITH TIME ZONE,
    use_local_agents_only BOOLEAN DEFAULT true,
    cost_limit DECIMAL(10,4) DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- AI Agent Analytics table
CREATE TABLE ai_agent_analytics (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    agent_id UUID REFERENCES ai_agents(id) ON DELETE CASCADE,
    period VARCHAR(20) NOT NULL, -- daily, weekly, monthly
    total_interactions INTEGER DEFAULT 0,
    unique_users INTEGER DEFAULT 0,
    average_response_time FLOAT DEFAULT 0.0,
    success_rate FLOAT DEFAULT 0.0,
    user_satisfaction FLOAT DEFAULT 0.0,
    total_cost DECIMAL(10,4) DEFAULT 0.0,
    cost_per_interaction DECIMAL(10,4) DEFAULT 0.0,
    capability_usage JSONB DEFAULT '{}',
    local_model_usage INTEGER DEFAULT 0,
    cloud_model_usage INTEGER DEFAULT 0,
    cost_savings DECIMAL(10,4) DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for AI Agent tables
CREATE INDEX idx_ai_agents_user_id ON ai_agents(user_id);
CREATE INDEX idx_ai_agents_type ON ai_agents(type);
CREATE INDEX idx_ai_agents_status ON ai_agents(status);
CREATE INDEX idx_ai_agents_is_public ON ai_agents(is_public);
CREATE INDEX idx_ai_agents_created_at ON ai_agents(created_at);

CREATE INDEX idx_ai_agent_tasks_agent_id ON ai_agent_tasks(agent_id);
CREATE INDEX idx_ai_agent_tasks_user_id ON ai_agent_tasks(user_id);
CREATE INDEX idx_ai_agent_tasks_type ON ai_agent_tasks(type);
CREATE INDEX idx_ai_agent_tasks_status ON ai_agent_tasks(status);
CREATE INDEX idx_ai_agent_tasks_created_at ON ai_agent_tasks(created_at);

CREATE INDEX idx_ai_agent_interactions_agent_id ON ai_agent_interactions(agent_id);
CREATE INDEX idx_ai_agent_interactions_user_id ON ai_agent_interactions(user_id);
CREATE INDEX idx_ai_agent_interactions_session_id ON ai_agent_interactions(session_id);
CREATE INDEX idx_ai_agent_interactions_created_at ON ai_agent_interactions(created_at);

CREATE INDEX idx_ai_agent_workflows_primary_agent_id ON ai_agent_workflows(primary_agent_id);
CREATE INDEX idx_ai_agent_workflows_is_active ON ai_agent_workflows(is_active);

CREATE INDEX idx_ai_agent_analytics_agent_id ON ai_agent_analytics(agent_id);
CREATE INDEX idx_ai_agent_analytics_period ON ai_agent_analytics(period);
CREATE INDEX idx_ai_agent_analytics_created_at ON ai_agent_analytics(created_at);

-- Performance Optimization Indexes
-- Compound indexes for frequently used query patterns
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_agents_user_status ON ai_agents(user_id, status) WHERE status = 'active';
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tasks_agent_status ON ai_agent_tasks(agent_id, status) WHERE status IN ('pending', 'in_progress');
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_interactions_agent_date ON ai_agent_interactions(agent_id, created_at DESC);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_interactions_user_session ON ai_agent_interactions(user_id, session_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_goal_states_goal_status ON goal_states(goal_id, status) WHERE status = 'active';
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_violations_goal_date ON goal_violations(goal_id, detected_at DESC);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_analytics_agent_period ON ai_agent_analytics(agent_id, period, created_at DESC);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_voice_commands_user_date ON voice_commands(user_id, created_at DESC);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_apps_user_status ON generated_apps(user_id, status) WHERE status = 'generating';
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_payments_user_status ON payments(user_id, status) WHERE status = 'pending';

-- Performance monitoring indexes
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_ai_agents_last_active ON ai_agents(last_active) WHERE last_active IS NOT NULL;
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_ai_agent_tasks_scheduled ON ai_agent_tasks(scheduled_for) WHERE scheduled_for IS NOT NULL;
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_ai_agent_interactions_rating ON ai_agent_interactions(user_rating) WHERE user_rating IS NOT NULL;

-- Triggers for updated_at
CREATE TRIGGER update_ai_agents_updated_at BEFORE UPDATE ON ai_agents FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_ai_agent_workflows_updated_at BEFORE UPDATE ON ai_agent_workflows FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- RLS Policies for AI Agent tables
ALTER TABLE ai_agents ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own AI agents" ON ai_agents FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can view public AI agents" ON ai_agents FOR SELECT USING (is_public = true);
CREATE POLICY "Users can manage own AI agents" ON ai_agents FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Service role can manage all AI agents" ON ai_agents FOR ALL USING (auth.role() = 'service_role');

ALTER TABLE ai_agent_tasks ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own AI agent tasks" ON ai_agent_tasks FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can manage own AI agent tasks" ON ai_agent_tasks FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Service role can manage all AI agent tasks" ON ai_agent_tasks FOR ALL USING (auth.role() = 'service_role');

ALTER TABLE ai_agent_interactions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own AI agent interactions" ON ai_agent_interactions FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can manage own AI agent interactions" ON ai_agent_interactions FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Service role can manage all AI agent interactions" ON ai_agent_interactions FOR ALL USING (auth.role() = 'service_role');

ALTER TABLE ai_agent_workflows ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own AI agent workflows" ON ai_agent_workflows FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can manage own AI agent workflows" ON ai_agent_workflows FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Service role can manage all AI agent workflows" ON ai_agent_workflows FOR ALL USING (auth.role() = 'service_role');

ALTER TABLE ai_agent_analytics ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own AI agent analytics" ON ai_agent_analytics FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Service role can manage all AI agent analytics" ON ai_agent_analytics FOR ALL USING (auth.role() = 'service_role');

-- Grant permissions
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL TABLES IN SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO anon, authenticated;
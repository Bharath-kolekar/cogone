# Database Schema

## Overview

- **Database**: PostgreSQL (via Supabase)
- **Location**: Supabase Cloud
- **Migrations**: Managed via `supabase/migrations/`

## Core Tables

### `users`
Primary user accounts table.

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### `user_2fa`
Two-factor authentication settings.

```sql
CREATE TABLE user_2fa (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    secret VARCHAR(255) NOT NULL,
    enabled BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### `apps`
Generated applications.

```sql
CREATE TABLE apps (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);
```

### `payments`
Payment records and transactions.

```sql
CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    provider VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Row-Level Security (RLS)

All tables have RLS policies enabled:
- Users can only access their own data
- Admin users can access all data

## Indexes

Key indexes for performance:
- `users.email` - Unique index for login
- `apps.user_id` - Foreign key index
- `payments.user_id` - Foreign key index
- `user_2fa.user_id` - Foreign key index

## Migrations

Located in `supabase/migrations/` directory.

To apply migrations:
```bash
cd supabase
supabase db push
```

## Backup & Recovery

- Supabase provides automatic backups
- Point-in-time recovery available
- Manual backups via Supabase dashboard

---

*Last Updated: October 10, 2025*


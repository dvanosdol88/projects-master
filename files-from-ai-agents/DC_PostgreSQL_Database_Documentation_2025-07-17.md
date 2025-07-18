# PostgreSQL Database Access and Configuration Documentation
*Compiled by Ubuntu Claude (UC) - July 17, 2025*

## Overview
This document consolidates all PostgreSQL database-related information found in the projects-master directory, including database schemas, connection details, and implementation patterns used across different projects.

## Database Schemas Found

### 1. MG Dashboard Database Schema
**Location:** `/mnt/c/Users/david/projects-master/mg-dashboard/database/schema.sql`

```sql
-- PostgreSQL Database Schema for mg-dashboard
-- Includes tasks and users tables with UUID primary keys

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tasks table (replacing Firestore tasks collection)
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Users table (for future authentication if needed)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Includes update triggers and indexes for performance
```

### 2. A2A System Database Schema
**Location:** `/mnt/c/Users/david/projects-master/a2a-system/database/schema.sql`

```sql
-- A2A System Database Schema
-- Supports PostgreSQL and SQLite

-- Tasks table with prioritization support
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    task TEXT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_to VARCHAR(50),
    status VARCHAR(20) DEFAULT 'pending',
    completed_at TIMESTAMP,
    metadata JSONB  -- Can store priority and other task metadata
);

-- API Keys table for authentication
CREATE TABLE IF NOT EXISTS api_keys (
    id SERIAL PRIMARY KEY,
    key_hash VARCHAR(128) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    rate_limit INTEGER DEFAULT 100,
    permissions JSONB
);

-- Request logs and system metrics tables also included
```

## Database Connection Configuration

### MG Dashboard Connection
**File:** `/mnt/c/Users/david/projects-master/mg-dashboard/lib/database.js`

```javascript
// PostgreSQL connection using pg library
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false }, // Required for Render PostgreSQL
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});
```

**Key Points:**
- Uses `DATABASE_URL` environment variable for connection string
- SSL enabled with `rejectUnauthorized: false` for Render.com compatibility
- Connection pooling configured with max 20 connections

### A2A System Configuration
**File:** `/mnt/c/Users/david/projects-master/a2a-system/.env.production`

```env
# Database Configuration (for production)
A2A_DB_TYPE=postgresql
# Update with your actual database URL from cloud provider
A2A_DATABASE_URL=postgresql://user:password@host:5432/a2a_production
```

## Render.com PostgreSQL Integration

### Connection Requirements
1. **SSL Configuration:** Must use `ssl: { rejectUnauthorized: false }` for Render PostgreSQL instances
2. **Connection String:** Provided by Render in the format: `postgresql://user:password@host:5432/dbname`
3. **Environment Variable:** Store as `DATABASE_URL` in Render service settings

### Deployment Notes
- Both mg-dashboard and a2a-system are configured for Render deployment
- Database schemas should be run after creating the PostgreSQL instance on Render
- Connection strings are managed through Render's environment variables

## Task Prioritization Schema

The A2A system's tasks table includes a `metadata JSONB` column that can store task priority and other attributes:

```sql
-- Example task with priority
INSERT INTO tasks (task, assigned_to, metadata) VALUES (
    'Implement new feature',
    'DC',
    '{"priority": "high", "category": "development", "estimated_hours": 4}'::jsonb
);
```

## Database Operations Pattern

### CRUD Operations Example (from mg-dashboard)
```javascript
export const tasksDB = {
  async getAll() {
    const result = await query('SELECT * FROM tasks ORDER BY created_at DESC');
    return result.rows;
  },
  
  async create(taskData) {
    const { title, description = '', completed = false } = taskData;
    const result = await query(
      'INSERT INTO tasks (title, description, completed) VALUES ($1, $2, $3) RETURNING *',
      [title, description, completed]
    );
    return result.rows[0];
  },
  
  // Update, delete, and other operations follow similar patterns
};
```

## Missing Information

While searching for DC (Debian Claude) specific database documentation, I did not find:
1. Specific Render database connection strings (these would be in environment variables)
2. DC-specific database setup instructions
3. Detailed task prioritization logic implementation

## Recommendations

1. **Environment Variables:** Check Render dashboard for actual `DATABASE_URL` values
2. **Schema Migration:** Run the appropriate schema.sql file after creating PostgreSQL instance
3. **Task Priority:** Implement priority handling using the JSONB metadata column
4. **Connection Testing:** Use the healthCheck function to verify database connectivity

## Related Files
- `/mnt/c/Users/david/projects-master/mg-dashboard/database/schema.sql`
- `/mnt/c/Users/david/projects-master/mg-dashboard/lib/database.js`
- `/mnt/c/Users/david/projects-master/a2a-system/database/schema.sql`
- `/mnt/c/Users/david/projects-master/a2a-system/.env.example`
- `/mnt/c/Users/david/projects-master/a2a-system/.env.production`
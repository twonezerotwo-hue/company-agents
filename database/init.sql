CREATE TABLE agents (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    agent_id INTEGER REFERENCES agents(id),
    description TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE results (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES tasks(id),
    result TEXT,
    execution_time INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

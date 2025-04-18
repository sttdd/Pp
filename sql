CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    position VARCHAR(100),
    department VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE SEQUENCE applications_application_id_seq;

-- Создание таблицы applications с каскадным удалением
CREATE TABLE applications (
    application_id INTEGER PRIMARY KEY DEFAULT nextval('applications_application_id_seq'),
    user_id BIGINT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    type VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL,
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT applications_user_id_fkey 
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE SEQUENCE logs_log_id_seq;

CREATE TABLE logs (
    log_id INTEGER PRIMARY KEY DEFAULT nextval('logs_log_id_seq'),
    user_id BIGINT NOT NULL,
    action TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT logs_user_id_fkey 
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

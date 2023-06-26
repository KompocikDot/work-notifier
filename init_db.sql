CREATE TABLE IF NOT EXISTS workifier_jobs(
    hash BYTEA,
    title VARCHAR(255),
    city VARCHAR(255),
    experience_level VARCHAR(127),
    company_name VARCHAR(127),
    -- TODO: Add employment_types with salaries
    skills_str TEXT,
    remote BOOLEAN,
    url_slug VARCHAR(255)
);

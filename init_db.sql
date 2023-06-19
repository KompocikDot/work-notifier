CREATE TABLE IF NOT EXISTS just_join_it(
    hash BYTEA,
    title VARCHAR(255),
    city VARCHAR(127),
    experience_level VARCHAR(20),
    company_name VARCHAR(127),
    -- TODO: Add employment_types with salaries
    skills_str VARCHAR(255),
    remote BOOLEAN,
    url_slug VARCHAR(255)
);

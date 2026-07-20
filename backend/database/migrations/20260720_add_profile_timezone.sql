-- Rushed before the release cut: profile preferences need to be available to the web client.
ALTER TABLE users ADD COLUMN profile_timezone VARCHAR(64) NULL;
CREATE INDEX ix_users_profile_timezone ON users (profile_timezone);

-- No rollback script was prepared for this release-window migration.

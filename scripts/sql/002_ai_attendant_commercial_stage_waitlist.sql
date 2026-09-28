-- Humanized sales/waitlist flow support.
-- The current Sales Inbox lead contract stores commercial state inside sales_leads.data.
-- These expression indexes keep the JSON-based slice queryable without forcing a destructive migration.

CREATE INDEX IF NOT EXISTS sales_leads_commercial_stage_json_idx
  ON sales_leads ((data->>'commercialStage'));

CREATE INDEX IF NOT EXISTS sales_leads_waitlist_status_json_idx
  ON sales_leads ((data->>'waitlistStatus'));

CREATE INDEX IF NOT EXISTS sales_leads_demo_status_json_idx
  ON sales_leads ((data->>'demoStatus'));

CREATE INDEX IF NOT EXISTS sales_leads_diagnostic_status_json_idx
  ON sales_leads ((data->>'diagnosticStatus'));

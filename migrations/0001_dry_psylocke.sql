CREATE TABLE `digistore_sales` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`product_id` text NOT NULL,
	`lead_id` integer,
	`amount` integer NOT NULL,
	`commission` integer NOT NULL,
	`currency` text DEFAULT 'eur',
	`digistore_transaction_id` text,
	`customer_data` text,
	`status` text DEFAULT 'completed',
	`created_at` integer DEFAULT (cast((julianday('now') - 2440587.5)*86400000 as integer))
);
--> statement-breakpoint
CREATE TABLE `upsell_events` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`type` text NOT NULL,
	`flow_id` text NOT NULL,
	`product_id` text NOT NULL,
	`lead_id` integer,
	`session_id` text,
	`persona_type` text,
	`amount` integer,
	`commission` integer,
	`customer_data` text,
	`created_at` integer DEFAULT (cast((julianday('now') - 2440587.5)*86400000 as integer))
);
--> statement-breakpoint
CREATE TABLE `upsell_flows` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`flow_id` text NOT NULL,
	`name` text NOT NULL,
	`description` text,
	`sequence` integer NOT NULL,
	`conditions` text,
	`is_active` text DEFAULT 'true',
	`created_at` integer DEFAULT (cast((julianday('now') - 2440587.5)*86400000 as integer))
);
--> statement-breakpoint
CREATE UNIQUE INDEX `upsell_flows_flow_id_unique` ON `upsell_flows` (`flow_id`);--> statement-breakpoint
CREATE TABLE `upsell_products` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`product_id` text NOT NULL,
	`flow_id` text NOT NULL,
	`name` text NOT NULL,
	`description` text,
	`price` integer NOT NULL,
	`currency` text DEFAULT 'eur',
	`digistore_id` text,
	`digistore_url` text,
	`commission` integer NOT NULL,
	`features` text,
	`bonus_items` text,
	`is_active` text DEFAULT 'true',
	`created_at` integer DEFAULT (cast((julianday('now') - 2440587.5)*86400000 as integer))
);
--> statement-breakpoint
CREATE UNIQUE INDEX `upsell_products_product_id_unique` ON `upsell_products` (`product_id`);
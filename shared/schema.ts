import { sqliteTable, text, integer } from "drizzle-orm/sqlite-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export const users = sqliteTable("users", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  username: text("username").notNull().unique(),
  password: text("password").notNull(),
});

export const leads = sqliteTable("leads", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  email: text("email").notNull(),
  firstName: text("first_name"),
  lastName: text("last_name"),
  phone: text("phone"),
  quizAnswers: text("quiz_answers"), // JSON string
  funnel: text("funnel"), // 'magic-profit' or 'money-magnet'
  source: text("source"), // quiz, vsl, bridge, etc.
  createdAt: integer("created_at", { mode: 'timestamp' }).defaultNow(),
});

export const emailFunnels = sqliteTable("email_funnels", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  name: text("name").notNull(),
  emails: text("emails").notNull(), // JSON array of email templates
  createdAt: integer("created_at", { mode: 'timestamp' }).defaultNow(),
});

export const analytics = sqliteTable("analytics", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  event: text("event").notNull(),
  page: text("page"),
  userId: text("user_id"),
  sessionId: text("session_id"),
  data: text("data"), // JSON string for additional data
  createdAt: integer("created_at", { mode: 'timestamp' }).defaultNow(),
});

// Upsell-Tracking Tabellen
export const upsellFlows = sqliteTable("upsell_flows", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  flowId: text("flow_id").notNull().unique(), // 'qmoney_upsell', 'cashmaximus_upsell'
  name: text("name").notNull(),
  description: text("description"),
  sequence: integer("sequence").notNull(),
  conditions: text("conditions"), // JSON string
  isActive: text("is_active").default('true'),
  createdAt: integer("created_at", { mode: 'timestamp' }).defaultNow(),
});

export const upsellProducts = sqliteTable("upsell_products", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  productId: text("product_id").notNull().unique(), // 'qmoney_basic', 'cashmaximus_premium'
  flowId: text("flow_id").notNull(),
  name: text("name").notNull(),
  description: text("description"),
  price: integer("price").notNull(), // in Cent
  currency: text("currency").default('eur'),
  digistoreId: text("digistore_id"),
  digistoreUrl: text("digistore_url"),
  commission: integer("commission").notNull(), // in Prozent
  features: text("features"), // JSON array
  bonusItems: text("bonus_items"), // JSON array
  isActive: text("is_active").default('true'),
  createdAt: integer("created_at", { mode: 'timestamp' }).defaultNow(),
});

export const upsellEvents = sqliteTable("upsell_events", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  type: text("type").notNull(), // 'view', 'purchase', 'decline'
  flowId: text("flow_id").notNull(),
  productId: text("product_id").notNull(),
  leadId: integer("lead_id"),
  sessionId: text("session_id"),
  personaType: text("persona_type"),
  amount: integer("amount"), // in Cent
  commission: integer("commission"), // in Cent
  customerData: text("customer_data"), // JSON string
  createdAt: integer("created_at", { mode: 'timestamp' }).defaultNow(),
});

export const digistoreSales = sqliteTable("digistore_sales", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  productId: text("product_id").notNull(),
  leadId: integer("lead_id"),
  amount: integer("amount").notNull(), // in Cent
  commission: integer("commission").notNull(), // in Cent
  currency: text("currency").default('eur'),
  digistoreTransactionId: text("digistore_transaction_id"),
  customerData: text("customer_data"), // JSON string
  status: text("status").default('completed'), // 'pending', 'completed', 'refunded'
  createdAt: integer("created_at", { mode: 'timestamp' }).defaultNow(),
});

export const insertLeadSchema = createInsertSchema(leads).pick({
  email: true,
  firstName: true,
  lastName: true,
  phone: true,
  quizAnswers: true,
  funnel: true,
  source: true,
});

export const insertEmailFunnelSchema = createInsertSchema(emailFunnels).pick({
  name: true,
  emails: true,
});

export const insertAnalyticsSchema = createInsertSchema(analytics).pick({
  event: true,
  page: true,
  userId: true,
  sessionId: true,
  data: true,
});

export const insertUserSchema = createInsertSchema(users).pick({
  username: true,
  password: true,
});

// Upsell Schemas
export const insertUpsellFlowSchema = createInsertSchema(upsellFlows).pick({
  flowId: true,
  name: true,
  description: true,
  sequence: true,
  conditions: true,
  isActive: true,
});

export const insertUpsellProductSchema = createInsertSchema(upsellProducts).pick({
  productId: true,
  flowId: true,
  name: true,
  description: true,
  price: true,
  currency: true,
  digistoreId: true,
  digistoreUrl: true,
  commission: true,
  features: true,
  bonusItems: true,
  isActive: true,
});

export const insertUpsellEventSchema = createInsertSchema(upsellEvents).pick({
  type: true,
  flowId: true,
  productId: true,
  leadId: true,
  sessionId: true,
  personaType: true,
  amount: true,
  commission: true,
  customerData: true,
});

export const insertDigistoreSaleSchema = createInsertSchema(digistoreSales).pick({
  productId: true,
  leadId: true,
  amount: true,
  commission: true,
  currency: true,
  digistoreTransactionId: true,
  customerData: true,
  status: true,
});

export type InsertUser = z.infer<typeof insertUserSchema>;
export type User = typeof users.$inferSelect;
export type InsertLead = z.infer<typeof insertLeadSchema>;
export type Lead = typeof leads.$inferSelect;
export type InsertEmailFunnel = z.infer<typeof insertEmailFunnelSchema>;
export type EmailFunnel = typeof emailFunnels.$inferSelect;
export type InsertAnalytics = z.infer<typeof insertAnalyticsSchema>;
export type Analytics = typeof analytics.$inferSelect;

// Upsell Types
export type InsertUpsellFlow = z.infer<typeof insertUpsellFlowSchema>;
export type UpsellFlow = typeof upsellFlows.$inferSelect;
export type InsertUpsellProduct = z.infer<typeof insertUpsellProductSchema>;
export type UpsellProduct = typeof upsellProducts.$inferSelect;
export type InsertUpsellEvent = z.infer<typeof insertUpsellEventSchema>;
export type UpsellEvent = typeof upsellEvents.$inferSelect;
export type InsertDigistoreSale = z.infer<typeof insertDigistoreSaleSchema>;
export type DigistoreSale = typeof digistoreSales.$inferSelect;

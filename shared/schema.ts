import { pgTable, text, serial, integer, boolean, timestamp } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  username: text("username").notNull().unique(),
  password: text("password").notNull(),
});

export const leads = pgTable("leads", {
  id: serial("id").primaryKey(),
  email: text("email").notNull(),
  firstName: text("first_name"),
  lastName: text("last_name"),
  phone: text("phone"),
  quizAnswers: text("quiz_answers"), // JSON string
  funnel: text("funnel"), // 'magic-profit' or 'money-magnet'
  source: text("source"), // quiz, vsl, bridge, etc.
  createdAt: timestamp("created_at").defaultNow(),
});

export const emailFunnels = pgTable("email_funnels", {
  id: serial("id").primaryKey(),
  name: text("name").notNull(),
  emails: text("emails").notNull(), // JSON array of email templates
  createdAt: timestamp("created_at").defaultNow(),
});

export const analytics = pgTable("analytics", {
  id: serial("id").primaryKey(),
  event: text("event").notNull(),
  page: text("page"),
  userId: text("user_id"),
  sessionId: text("session_id"),
  data: text("data"), // JSON string for additional data
  createdAt: timestamp("created_at").defaultNow(),
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

export type InsertUser = z.infer<typeof insertUserSchema>;
export type User = typeof users.$inferSelect;
export type InsertLead = z.infer<typeof insertLeadSchema>;
export type Lead = typeof leads.$inferSelect;
export type InsertEmailFunnel = z.infer<typeof insertEmailFunnelSchema>;
export type EmailFunnel = typeof emailFunnels.$inferSelect;
export type InsertAnalytics = z.infer<typeof insertAnalyticsSchema>;
export type Analytics = typeof analytics.$inferSelect;

export const insertUserSchema = createInsertSchema(users).pick({
  username: true,
  password: true,
});

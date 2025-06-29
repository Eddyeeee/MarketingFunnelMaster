import type { Config } from "drizzle-kit";
import path from "path";

export default {
  schema: "./shared/schema.ts",
  out: "./migrations",
  dialect: "sqlite",
  dbCredentials: {
    url: "file:" + path.resolve("./db/db.sqlite")
  }
} satisfies Config;
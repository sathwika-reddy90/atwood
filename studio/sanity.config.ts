import { visionTool } from "@sanity/vision";
import { defineConfig } from "sanity";
import { structureTool } from "sanity/structure";

import { apiVersion, dataset, projectId } from "./env";
import { schemaTypes } from "./schemaTypes";

/**
 * The Studio — where Journal posts are written. It runs as its own app, not
 * inside the site: `npm run dev` locally (in studio/), `npm run deploy` to
 * host it on Sanity at https://atwood-dsigns.sanity.studio.
 */
export default defineConfig({
  name: "atwood-dsigns",
  title: "Atwood Dsigns",
  projectId,
  dataset,
  schema: { types: schemaTypes },
  plugins: [structureTool(), visionTool({ defaultApiVersion: apiVersion })],
});

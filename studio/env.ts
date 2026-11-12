/**
 * Sanity connection settings. Neither value is a secret: the dataset is public
 * read, and every write goes through a logged-in Studio session.
 * tools/build.py reads the same project (see SANITY in that file).
 */
export const projectId = process.env.SANITY_STUDIO_PROJECT_ID || "xbvaq1gt";
export const dataset = process.env.SANITY_STUDIO_DATASET || "production";

/** Pinned so a Sanity-side API change can't alter query results under us. */
export const apiVersion = "2025-10-01";

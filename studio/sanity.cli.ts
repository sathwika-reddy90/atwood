import { defineCliConfig } from "sanity/cli";

import { dataset, projectId } from "./env";

export default defineCliConfig({
  api: { projectId, dataset },
  // Hostname for `sanity deploy`: the Studio is served at
  // https://<studioHost>.sanity.studio
  studioHost: "atwood-dsigns",
  deployment: { appId: "s51yrpz0ymm6jbsptp8t6ydb" },
});

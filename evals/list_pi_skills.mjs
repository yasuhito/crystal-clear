#!/usr/bin/env node

import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { pathToFileURL } from "node:url";

const [modulePath, cwd, agentDir] = process.argv.slice(2);
if (!modulePath || !cwd || !agentDir) {
  throw new Error("usage: list_pi_skills.mjs <pi-index.js> <cwd> <agent-dir>");
}

const { DefaultPackageManager, SettingsManager, loadSkills } = await import(
  pathToFileURL(modulePath)
);
const settingsManager = SettingsManager.create(cwd, agentDir, {
  projectTrusted: true,
});
const packageManager = new DefaultPackageManager({
  cwd,
  agentDir,
  settingsManager,
});
const resources = await packageManager.resolve(async () => "skip");
const skillPaths = resources.skills
  .filter((resource) => resource.enabled)
  .map((resource) => resource.path);
const loaded = loadSkills({
  cwd,
  agentDir,
  skillPaths,
  includeDefaults: false,
});

const inventory = loaded.skills.map((skill) => ({
  name: skill.name,
  path: skill.filePath,
  sha256: createHash("sha256").update(readFileSync(skill.filePath)).digest("hex"),
  disable_model_invocation: skill.disableModelInvocation,
}));
console.log(JSON.stringify(inventory));

export function engineSignature(): string {
  const g = globalThis as any;

  if (typeof g.Bun !== "undefined") return `Bun ${g.Bun.version}`;
  if (typeof g.Deno !== "undefined") return `Deno ${g.Deno.version.deno}`;
  if (typeof process !== "undefined") return `Node.js ${process.version}`;

  return "UNKNOWN_RUNTIME";
}

export function exitRuntime(code: number): never {
  const g = globalThis as any;

  if (typeof g.Deno !== "undefined") g.Deno.exit(code);
  if (typeof process !== "undefined") process.exit(code);

  throw new Error(`EXIT_${code}`);
}

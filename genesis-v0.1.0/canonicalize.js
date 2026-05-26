function canonicalize(value) {
  if (value === null) return "null";
  if (Array.isArray(value)) return "[" + value.map(canonicalize).join(",") + "]";
  if (typeof value === "object") {
    return "{" + Object.keys(value).sort().map(k =>
      JSON.stringify(k) + ":" + canonicalize(value[k])
    ).join(",") + "}";
  }
  return JSON.stringify(value);
}
module.exports = { canonicalize };

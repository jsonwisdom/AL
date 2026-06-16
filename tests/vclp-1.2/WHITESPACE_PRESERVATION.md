# HTML Whitespace Preservation - Lab Requirement

## Status
**Not yet implemented** - design phase

## Requirement
VCLP 1.2 HTML canonical extraction MUST preserve whitespace inside:
- `<pre>`
- `<code>`  
- `<textarea>`

For all other content, collapse whitespace runs to single spaces.

## Challenge
The current extractor collapses ALL whitespace globally (using `re.sub(r"\s+", " ", raw_text)`).

## Proposed Solution
1. Detection: Identify when we're inside preserved tags during traversal
2. Flag propagation: Pass `preserve_mode` through recursion
3. Conditional collapse: Skip whitespace normalization for preserved content

## Current State
- HTML: Working lab extractor (collapses all whitespace)
- TXT: Frozen reference (no whitespace issues)
- This refinement is DEFERRED until needed for real HTML sources

## Acceptance Criteria (future)
- `<pre>` content preserves leading/trailing spaces and newlines
- Multiple spaces inside `<code>` are preserved
- `<textarea>` preserves line breaks exactly
- Surrounding content still collapses whitespace normally

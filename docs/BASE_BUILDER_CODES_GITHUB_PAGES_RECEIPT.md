# Base Builder Codes + GitHub Pages Receipt

Status: CORRECTED
Date: 2026-06-22

## What Base actually asks for

Base Dashboard Builder Codes registration requires:

1. Register app name.
2. Add and verify your domain.
3. Go to Settings -> Builder Codes to get the code.

Source: Coinbase x402 Builder Codes docs.

## What went wrong

The AL project page lives at:

```text
https://jsonwisdom.github.io/AL/site/
```

That is a GitHub Pages project path, not a standalone app domain root.

The Base Dashboard field says App Domain. It appears to validate a host/domain fetch, not an arbitrary GitHub Pages project URL path.

## Free options

### Option A: use the existing AL project page only for public display

Keep:

```text
https://jsonwisdom.github.io/AL/site/
```

Do not treat it as a Base Builder Code app domain unless Base accepts project paths.

### Option B: use a free GitHub Pages user site

Create the user site repository:

```text
jsonwisdom.github.io
```

Then `https://jsonwisdom.github.io/` becomes the root app domain.

### Option C: use a free Vercel/Cloudflare Pages subdomain

Deploy a simple static page with the Base meta tag and use the assigned free subdomain as the App Domain.

## Verification tag

```html
<meta name="base:app_id" content="6944536ed19763ca26ddc433" />
```

## No Fake Green

Do not mark Base Builder Code verification GREEN until the Base Dashboard accepts the domain and issues the builder code.

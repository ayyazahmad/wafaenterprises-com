# Wafa Enterprises Static Site

Static export of [wafaenterprises.com](https://wafaenterprises.com) (WordPress + BeTheme), prepared for Vercel.

## Local preview

```bash
python -m http.server 8080
```

Open [http://localhost:8080](http://localhost:8080).

## Maintenance scripts

- `scripts/build_site.py` — download pages/assets from live site and localize URLs
- `scripts/verify_assets.py` — report missing local asset references

## Deploy

Push to GitHub and connect the repository to Vercel. No build step is required.

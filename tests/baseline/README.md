# Baseline Screenshots

Place reference screenshots here to enable pixel-diff verification.

- Expected file for session 15 grid: `sessao-15-grid.png`
- You can override the baseline path via env var `BASELINE`.

Recommended capture:
1. Open `http://localhost:8000/abraao/modulo-3/sessao-15.html`.
2. Screenshot the 4x4 macro grid region aligned to the reference image.
3. Save as `tests/baseline/sessao-15-grid.png`.

Run diff check:

```
npm run verify:diff
```

Adjust tolerance with `DIFF_TOLERANCE` (percentage), e.g. `DIFF_TOLERANCE=0.3`.

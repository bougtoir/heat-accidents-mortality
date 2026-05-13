---
name: testing-paperhub
description: Test PaperHub dashboard end-to-end. Use when verifying Gantt chart, inline editing, or paper management features.
---

# Testing PaperHub Dashboard

## Dev Server Setup

```bash
cd paper-dashboard
npm install
npm run dev -- --port 5173
```

App runs at `http://localhost:5173`. No authentication required.

## Build Verification

```bash
cd paper-dashboard
npm run build   # tsc -b && vite build
```

Should produce 0 TypeScript errors.

## Key Architecture

- **React 19 + TypeScript + Vite** — no external UI libraries
- **LocalStorage persistence** — all paper data stored in `localStorage` key `papers`
- **9 dockable panes**: Title & Authors, Progress Timeline (Gantt), Links, Deliverables, Deadlines, Notes/TODO, Statistics, Costs/Funding, Co-author Tasks
- **State management**: `DashboardContext` with `useLocalStorage` hook
- **Sample data**: `src/data/sample-papers.ts` (7 papers with various statuses)

## Browser Automation Notes

### React Props Click Workaround

Direct `browser.click(devinid)` and coordinate clicks might not trigger React event handlers reliably. Use React props via console as a workaround:

```javascript
const el = document.querySelector('[devinid="X"]');
const propsKey = Object.keys(el).find(k => k.startsWith('__reactProps'));
el[propsKey].onClick();
```

This works reliably for sidebar paper selection and inline edit triggers.

### Inline Edit Interaction Pattern

To programmatically edit inline fields:

```javascript
// 1. Trigger edit mode via React props onClick
// 2. Find the textarea/input that appears
const textarea = document.querySelector('textarea[devinid="X"]');
const nativeSetter = Object.getOwnPropertyDescriptor(
  window.HTMLTextAreaElement.prototype, 'value'
).set;
nativeSetter.call(textarea, 'new value');
textarea.dispatchEvent(new Event('input', { bubbles: true }));
// 3. Save with Enter
textarea.dispatchEvent(
  new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', bubbles: true })
);
```

Use `HTMLInputElement.prototype` for `<input>` fields instead of `HTMLTextAreaElement.prototype`.

### Add Paper Dialog

The "+ New Paper" button might not respond to browser automation clicks. The React onClick handler fires but the dialog may not mount. This could be an environment-specific issue — try manual testing if automated clicks fail.

## Testing Gantt Chart Bars

Gantt bar widths can be verified via console:

```javascript
const bars = [];
document.querySelectorAll('div[style*="border-radius: 3px"][style*="position: absolute"]')
  .forEach(d => {
    if (d.style.width?.includes('%') && d.style.position === 'absolute') {
      bars.push({ width: d.style.width, left: d.style.left });
    }
  });
console.log(JSON.stringify(bars, null, 2));
```

### Expected Gantt Bar Logic

- Events **with endDate** (even if `endDate === startDate`): bar renders at that date range (may be min 2% width)
- Events **without endDate**: bar extends from startDate to Today (ongoing)
- Key assertion: `width > 2%` means the bar extends beyond a point marker

### Good Test Papers for Gantt Verification

- **Zero-cal PMEA**: Has both bounded events (Drafting, Peer Review) and ongoing (Revision, no endDate) + single-day (Submission, endDate=startDate)
- **GDP tempo-effect**: Has ongoing Submission (no endDate) — the user's original bug report scenario
- **Cryoanesthesia review**: Has completed single-day events (Accepted, Submission) that should NOT extend to Today

## Testing Inline Editing

1. **Title**: Click title div → textarea appears → modify → Enter saves
2. **Journal name**: Click journal span in Pane 2 → input appears → modify → Enter saves (also updates sidebar)
3. **Persistence**: Edit a field → switch papers → switch back → verify edit persisted

## Resetting State

To reset to sample data:
```javascript
localStorage.clear();
location.reload();
```

## Devin Secrets Needed

None — PaperHub runs entirely locally with no external services.

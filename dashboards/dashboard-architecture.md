# Dashboard Architecture

This document outlines the structure of the personal dashboard contained in this repository.

## Overview

The dashboard is a static web application optimized for tablet and desktop displays. It stores notes and tasks locally using the browser's `localStorage` API.

### Folder Layout

```
dashboards/
  personal-dashboard/
    index.html
    style.css
    script.js
```

- **index.html** – Base markup and layout.
- **style.css** – Responsive styles with a focus on readability and clarity.
- **script.js** – Handles task management, note storage, and renders a mock schedule.

## Usage

Open `index.html` in any modern browser. Tasks and notes persist in localStorage, so data remains across page reloads.

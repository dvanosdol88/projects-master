# Dashboard Architecture

This document outlines the basic structure of the new personal dashboard.

## Overview

The dashboard is a lightweight single-page application using HTML, CSS, and JavaScript. It stores data in the browser using `localStorage` so it works offline. The layout adapts to different screen sizes, including tablets like the iPad Pro.

## File Structure

- `dashboards/personal-dashboard/index.html` – main entry point with page markup
- `dashboards/personal-dashboard/style.css` – responsive styling
- `dashboards/personal-dashboard/script.js` – logic for tasks, notes, and sidebar menu

## Features

- Collapsible sidebar navigation
- Task list with add and remove interactions
- Notes area that persists text
- Placeholder section for future calendar integration

## Usage

Open `index.html` in a modern browser. Tasks and notes automatically save to `localStorage`. Removing a task is as simple as clicking on it.


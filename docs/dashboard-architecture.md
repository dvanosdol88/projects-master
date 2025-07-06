# Dashboard Architecture

This document describes the structure of the personal dashboard located in `dashboards/personal-dashboard`.

## Frontend

- **index.html** – main layout with sidebar navigation and content sections for Overview, Tasks, Calendar and Notes.
- **style.css** – responsive styles inspired by modern iPad interfaces.
- **script.js** – handles task management using `localStorage` for persistence.

## Usage

Simply open `index.html` in your web browser. Tasks will be saved between sessions thanks to `localStorage`.

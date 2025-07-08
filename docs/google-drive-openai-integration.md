# Google Drive and OpenAI Integration

This document outlines the backend endpoints that connect Google Drive and ChatGPT Vision for the dashboard.

## Environment Variables

Set the following keys in your `.env` file or the Render dashboard:

```
OPENAI_API_KEY=your-openai-api-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=your-google-redirect-uri
GOOGLE_REFRESH_TOKEN=your-refresh-token
GOOGLE_DRIVE_FOLDER_ID=drive-folder-id
PORT=5000
```

## Endpoints

- **POST `/api/upload-to-drive`** – upload a file to Google Drive. The uploaded field should be named `file`.
- **POST `/api/process-image`** – send an `image` file to ChatGPT Vision to extract data.
- **POST `/api/update-task-list`** – update the task list in memory by sending `{ action: 'add'|'remove', item }`.
- **GET `/api/retrieve-task-list`** – fetch the current list of tasks.

These endpoints live in `dashboards/chatgpt-google-dashboard/backend/index.js` and can be started with `npm start` from the same folder.

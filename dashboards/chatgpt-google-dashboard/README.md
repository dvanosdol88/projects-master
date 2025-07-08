# ChatGPT Google Dashboard

This project integrates Google services with a ChatGPT-powered dashboard.

## Folder Structure

- `backend/` - Express API server
- `frontend/` - React application
- `docs/` - Project documentation

## Setup

1. Install dependencies in `backend/`:
   ```bash
   cd backend
   npm init -y
   npm install express cors dotenv googleapis openai multer
   ```
2. Install dependencies in `frontend/`:
   ```bash
   cd ../frontend
   npm init -y
   npm install react react-dom axios
   ```
3. Create `.env` in the project root:
 ```bash
  OPENAI_API_KEY=your-openai-api-key
  GOOGLE_CLIENT_ID=your-google-client-id
  GOOGLE_CLIENT_SECRET=your-google-client-secret
  GOOGLE_REDIRECT_URI=your-google-redirect-uri
  GOOGLE_REFRESH_TOKEN=your-refresh-token
  GOOGLE_DRIVE_FOLDER_ID=drive-folder-id
  ```
4. Run the backend:
   ```bash
 node backend/index.js
  ```
5. Start the frontend (e.g., with your preferred bundler).

This repository is a partial setup following the migration checklist.

## API Endpoints

The backend exposes several endpoints used by the dashboard:

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/upload-to-drive` | POST | Upload a file to Google Drive. Field name: `file`. |
| `/api/process-image` | POST | Process an uploaded `image` using ChatGPT Vision. |
| `/api/update-task-list` | POST | Update in-memory task list (`{action: 'add'|'remove', item}`). |
| `/api/retrieve-task-list` | GET | Fetch the current task list. |


const express = require('express');
const cors = require('cors');
const multer = require('multer');
const { google } = require('googleapis');
const OpenAI = require('openai');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

const upload = multer({ storage: multer.memoryStorage() });

const oauth2Client = new google.auth.OAuth2(
  process.env.GOOGLE_CLIENT_ID,
  process.env.GOOGLE_CLIENT_SECRET,
  process.env.GOOGLE_REDIRECT_URI
);
if (process.env.GOOGLE_REFRESH_TOKEN) {
  oauth2Client.setCredentials({ refresh_token: process.env.GOOGLE_REFRESH_TOKEN });
}
const drive = google.drive({ version: 'v3', auth: oauth2Client });

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

let tasks = [];

app.post('/api/upload-to-drive', upload.single('file'), async (req, res) => {
  try {
    const fileMetadata = {
      name: req.file.originalname,
      parents: process.env.GOOGLE_DRIVE_FOLDER_ID ? [process.env.GOOGLE_DRIVE_FOLDER_ID] : undefined,
    };
    const media = {
      mimeType: req.file.mimetype,
      body: Buffer.from(req.file.buffer),
    };
    const response = await drive.files.create({
      resource: fileMetadata,
      media,
      fields: 'id,name',
    });
    res.json(response.data);
  } catch (error) {
    console.error('Upload error:', error.message);
    res.status(500).json({ error: 'Failed to upload file' });
  }
});

app.post('/api/process-image', upload.single('image'), async (req, res) => {
  try {
    const base64 = req.file.buffer.toString('base64');
    const result = await openai.chat.completions.create({
      model: 'gpt-4-vision-preview',
      messages: [
        {
          role: 'user',
          content: [
            { type: 'text', text: 'Extract key data from the image' },
            { type: 'image_url', image_url: { url: `data:${req.file.mimetype};base64,${base64}` } },
          ],
        },
      ],
    });
    res.json(result);
  } catch (error) {
    console.error('Vision error:', error.message);
    res.status(500).json({ error: 'Failed to process image' });
  }
});

app.post('/api/update-task-list', (req, res) => {
  const { action, item } = req.body;
  if (action === 'add' && item) tasks.push(item);
  if (action === 'remove' && item) tasks = tasks.filter((t) => t !== item);
  res.json({ tasks });
});

app.get('/api/retrieve-task-list', (req, res) => {
  res.json({ tasks });
});

app.get('/', (req, res) => {
  res.send('Backend is running!');
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

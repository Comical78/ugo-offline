// imports and values
const fs = require('fs');
const express = require('express');
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '.env') });
const app = express();
const PORT = 3000;
const NEW_URL_PREFIX = process.env.URL_PREFIX || 'https://localhost:3000/';
// routers
app.get('/map_index.json', (req, res) => {
  const filePath = path.join(__dirname, 'files', 'map_index.json');
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      console.error("Eroare at file reading:", err);
      return res.status(500).send('Error at file reading');
    }
    try {
      const cleanData = data.replace(/^\uFEFF/, '');
      let jsonData = JSON.parse(cleanData);
      if (Array.isArray(jsonData)) {
        jsonData = jsonData.map(item => {
          if (item.mapZipUrl && item.mapZipUrl.startsWith('https://static.resquared.studio/'))
            item.mapZipUrl = item.mapZipUrl.replace('https://static.resquared.studio/', NEW_URL_PREFIX);
          if (item.mapIcon && item.mapIcon.startsWith('https://static.resquared.studio/'))
            item.mapIcon = item.mapIcon.replace('https://static.resquared.studio/', NEW_URL_PREFIX);
          return item;
        });
      }
      res.json(jsonData);
    } catch (parseErr) {
      console.error("Eroare at parsing:", parseErr);
      res.status(500).send('Error at JSON parsing');
    }
  });
});
app.use('/', express.static(path.join(__dirname, 'files')));
app.use((req, res) => { res.status(404).send('404 Not Found'); });
// start app
app.listen(PORT);
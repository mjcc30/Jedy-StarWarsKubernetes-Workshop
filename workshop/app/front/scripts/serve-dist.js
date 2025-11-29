const http = require('http');
const fs = require('fs');
const path = require('path');

const dist = path.join(__dirname, '..', 'dist');
const port = process.env.PORT ? Number(process.env.PORT) : 8080;

const mime = {
  html: 'text/html',
  css: 'text/css',
  js: 'application/javascript',
  svg: 'image/svg+xml',
  png: 'image/png',
  jpg: 'image/jpeg',
  jpeg: 'image/jpeg',
  json: 'application/json',
  txt: 'text/plain',
};

const server = http.createServer((req, res) => {
  let urlPath = decodeURIComponent(req.url.split('?')[0]);
  if (urlPath === '/' || urlPath === '') urlPath = '/index.html';
  const filePath = path.join(dist, urlPath);
  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      res.statusCode = 404;
      res.end('Not found');
      return;
    }
    const ext = path.extname(filePath).slice(1);
    res.setHeader('Content-Type', mime[ext] || 'application/octet-stream');
    fs.createReadStream(filePath).pipe(res);
  });
});

server.listen(port, () => console.log(`Serving dist on http://localhost:${port}`));

const http = require("http");

const PORT = process.env.PORT || 3000;
const SIZE_MB = Number(process.env.SIZE_MB || 5);

// Генерируем тестовые данные указанного размера (в мегабайтах)
const payload = Buffer.alloc(SIZE_MB * 1024 * 1024, "a");

const server = http.createServer((req, res) => {
  res.writeHead(200, {
    "Content-Type": "application/octet-stream",
    "Content-Length": payload.length,
    "Cache-Control": "no-store",
  });
  res.end(payload);
});

server.listen(PORT, () => {
  console.log(`Test server running at http://localhost:${PORT}/`);
  console.log(`Payload size: ${SIZE_MB} MB`);
});

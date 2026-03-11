/**
 * record-preroll.js
 *
 * Records ai-hed-preroll.html as a video using Playwright,
 * then converts the .webm output to .mp4 with ffmpeg.
 *
 * Usage:
 *   npm install
 *   npx playwright install chromium
 *   node record-preroll.js
 *
 * Output: video-output/ai-hed-preroll.mp4
 */

const { chromium } = require('playwright');
const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const HTML_FILE   = path.resolve(__dirname, 'ai-hed-preroll.html');
const VIDEO_DIR   = path.resolve(__dirname, 'video-output');
const MP4_OUTPUT  = path.join(VIDEO_DIR, 'ai-hed-preroll.mp4');
const VIEWPORT    = { width: 1920, height: 1080 };

// Animation timeline:
//   Shapes:       0.00s – 2.13s
//   Title:        2.30s – 2.80s
//   Tagline:      2.80s – 3.30s
//   Logo settle:  3.80s – 4.60s
//   Disclaimer:   4.70s – 5.30s
//   Partner logos: 4.70s – 5.30s
// Hold 1.5s after everything has settled.
const RECORD_DURATION_MS = 5000;

(async () => {
  fs.mkdirSync(VIDEO_DIR, { recursive: true });

  console.log('Launching browser…');
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: VIEWPORT,
    recordVideo: {
      dir: VIDEO_DIR,
      size: VIEWPORT,
    },
  });

  const page = await context.newPage();
  await page.goto(`file://${HTML_FILE}`);

  console.log(`Recording ${RECORD_DURATION_MS / 1000}s of animation…`);
  await page.waitForTimeout(RECORD_DURATION_MS);

  // Closing the context flushes the video to disk
  await context.close();
  await browser.close();

  // Find the most recently written .webm file
  const webmFiles = fs.readdirSync(VIDEO_DIR)
    .filter(f => f.endsWith('.webm'))
    .map(f => ({ name: f, mtime: fs.statSync(path.join(VIDEO_DIR, f)).mtimeMs }))
    .sort((a, b) => b.mtime - a.mtime);

  if (webmFiles.length === 0) {
    console.error('Error: no .webm file found in', VIDEO_DIR);
    process.exit(1);
  }

  const webmPath = path.join(VIDEO_DIR, webmFiles[0].name);
  console.log(`Raw recording: ${webmPath}`);

  // Convert to MP4 with ffmpeg
  console.log('Converting to MP4…');
  try {
    execSync(
      `ffmpeg -y -i "${webmPath}" -c:v libx264 -preset fast -pix_fmt yuv420p "${MP4_OUTPUT}"`,
      { stdio: 'inherit' }
    );
    console.log(`\nDone! Output: ${MP4_OUTPUT}`);
    console.log('\nTo append this pre-roll to another video:');
    console.log(`  printf "file '${MP4_OUTPUT}'\\nfile 'your-video.mp4'\\n" > concat.txt`);
    console.log('  ffmpeg -f concat -safe 0 -i concat.txt -c copy combined.mp4');
  } catch (err) {
    console.error('ffmpeg conversion failed. Raw .webm is at:', webmPath);
    console.error('Convert manually:');
    console.error(`  ffmpeg -i "${webmPath}" -c:v libx264 -pix_fmt yuv420p "${MP4_OUTPUT}"`);
    process.exit(1);
  }
})();

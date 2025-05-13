const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: true, // Set to false to see the browser
    args: ['--no-sandbox']
  });

  const page = await browser.newPage();
  await page.goto('http://localhost:9000/login');

  // Fill in login form
  await page.type('#username', 'admin');
  await page.type('#password', 'supersecretadminpassword');
  await page.click('#submit');

  // Wait for navigation to complete
  await page.waitForNavigation();

  console.log('Logged in. Starting refresh loop...');

  // Refresh every 5 seconds
  while (true) {
    await page.reload({ waitUntil: ['networkidle0', 'domcontentloaded'] });
    console.log('Page refreshed');
    await new Promise(resolve => setTimeout(resolve, 30000));
  }

  // browser.close(); // Never reached in infinite loop
})();

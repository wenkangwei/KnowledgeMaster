
        const puppeteer = require('puppeteer');
        
        async function scrapePage() {
            const browser = await puppeteer.launch({headless: true});
            const page = await browser.newPage();
            await page.goto('https://example.com', {waitUntil: 'networkidle0'});
            
            const content = await page.evaluate(() => {
                return {
                    title: document.title,
                    content: document.body.innerText,
                    html: document.documentElement.outerHTML
                };
            });
            
            await browser.close();
            return content;
        }
        
        scrapePage().then(console.log).catch(console.error);
        
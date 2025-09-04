import asyncio
from playwright.async_api import async_playwright
import json

async def scrape_with_playwright():
    """使用Playwright直接爬取"""
    try:
        print("启动Playwright...")
        async with async_playwright() as p:
            # 启动浏览器
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage'
                ]
            )
            
            # 创建页面
            page = await browser.new_page()
            
            # 设置用户代理
            await page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            # 导航到页面
            wechat_url = "https://mp.weixin.qq.com/s/OMtb1DL_ik2TvENzWHWGsg"
            # wechat_url= "https://zhuanlan.zhihu.com/p/1901422655787230018"
            print(f"导航到: {wechat_url}")
            await page.goto(wechat_url, wait_until='networkidle')
            
            # 等待页面加载
            await page.wait_for_timeout(5000)
            
            # 提取文章内容
            print("提取内容...")
            article_data = await page.evaluate("""() => {
                const selectors = [
                    '#js_content',
                    '.rich_media_content', 
                    '.article-content',
                    'article'
                ];
                
                let contentElement = null;
                for (const selector of selectors) {
                    contentElement = document.querySelector(selector);
                    if (contentElement) break;
                }
                
                if (!contentElement) {
                    contentElement = document.body;
                }
                
                return {
                    title: document.title,
                    url: window.location.href,
                    content: contentElement.innerText.trim(),
                    html: contentElement.innerHTML,
                    success: true
                };
            }""")
            
            print("关闭浏览器...")
            await browser.close()
            
            print("抓取成功!")
            print(f"标题: {article_data['title']}")
            print(f"内容长度: {len(article_data['content'])} 字符")
            print(f"内容预览: {article_data['content'][:]}...")
            
            # 保存结果
            with open('wechat_article_playwright.json', 'w', encoding='utf-8') as f:
                json.dump(article_data, f, ensure_ascii=False, indent=2)
            
            return article_data
            
    except Exception as e:
        print(f"Playwright错误: {e}")
        return None

# 安装Playwright: pip install playwright && playwright install chromium
if __name__ == "__main__":
    asyncio.run(scrape_with_playwright())
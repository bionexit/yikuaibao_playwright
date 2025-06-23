import os
import re
import time
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
import html2text

# 获取当前时间 yyyy-mm-dd hh:mm:ss
from datetime import datetime
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")



# 配置
INIT_URL = "https://docs.ekuaibao.com/docs/open-api/getting-started"
BASE_URL = "https://docs.ekuaibao.com"
OUTPUT_DIR = "ekuaibao_docs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 初始化 Markdown 转换器
h = html2text.HTML2Text()
h.ignore_links = False
h.ignore_images = False
h.body_width = 0
h.wrap_links = False

def sanitize_filename(level1_index,leve2_index, level1_title, level2_title):
    """生成文件名：第一级目录顺序号-第一级目录显示字符-第二级目录显示字符"""
    # 清理标题中的特殊字符
    level1_clean = re.sub(r'[\\/*?:"<>|]', "", level1_title)
    level2_clean = re.sub(r'[\\/*?:"<>|]', "", level2_title)
    
    # 替换空格为下划线
    level1_clean = re.sub(r'\s+', '_', level1_clean)
    level2_clean = re.sub(r'\s+', '_', level2_clean)
    
    # 截断过长的文件名
    level1_clean = level1_clean[:50]
    level2_clean = level2_clean[:50]
    
    return f"{level1_index}-{leve2_index}-{level1_clean}-{level2_clean}.md"

def extract_main_content(page):
    """从页面中提取主要内容区域"""
    # Docusaurus 特定的内容区域选择器
    selectors = [
        '.theme-doc-markdown',  # Docusaurus 专用
        '.markdown',            # 备用 Markdown 容器
        'article',              # 语义化标签
        'main',                 # 主内容区
        '.content'              # 通用内容类
    ]
    
    for selector in selectors:
        element = page.query_selector(selector)
        if element:
            return element
    
    # 回退到整个 body
    return page.query_selector('body')

def expand_all_menus(page):
    """递归展开所有折叠的菜单项"""
    # 查找所有可展开的菜单按钮
    expand_buttons = page.query_selector_all('.menu__link--sublist')
    
    for button in expand_buttons:
        # 检查按钮是否可点击（未展开状态）
        is_expanded = button.get_attribute('aria-expanded')
        if is_expanded == 'false':
            try:
                # 滚动到元素确保可见
                button.scroll_into_view_if_needed()
                button.click()
                # 等待菜单展开动画
                time.sleep(0.3)
            except Exception:
                # 如果点击失败继续处理下一个
                continue
    
    # 递归检查是否有新出现的菜单项
    new_buttons = page.query_selector_all('.menu__link--sublist[aria-expanded="false"]')
    if new_buttons:
        expand_all_menus(page)

def get_doc_links_with_hierarchy(page):
    """获取所有文档链接及其层级关系"""
    # 展开所有菜单项
    expand_all_menus(page)
    
    # 等待菜单完全加载
    time.sleep(1)
    
    # 获取所有一级目录
    level1_items = page.query_selector_all('.theme-doc-sidebar-item-category-level-1')
    
    # 存储所有文档链接及其层级信息
    doc_links = []
    
    # 遍历一级目录
    for level1_index, level1_item in enumerate(level1_items, start=1):
        # 获取一级目录标题
        level1_title_elem = level1_item.query_selector('.menu__link--sublist')
        level1_title = level1_title_elem.inner_text().strip() if level1_title_elem else f"目录{level1_index}"
        
        # 获取该一级目录下的所有二级链接
        level2_links = level1_item.query_selector_all('.theme-doc-sidebar-item-link-level-2 a.menu__link')
        
        for link_index,link in enumerate(level2_links,start=1):
            href = link.get_attribute("href")
            if href:
                # 获取二级目录标题
                level2_title = link.inner_text().strip()
                
                # 构建完整URL
                full_url = urljoin(BASE_URL, href)
                
                # 添加到结果列表
                doc_links.append({
                    "url": full_url,
                    "level1_index": level1_index,
                    "level1_title": level1_title,
                    "level2_title": level2_title,
                    "level2_index": link_index
                })
    
    return doc_links

def crawl_docs():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # 设置超时时间
        page.set_default_timeout(60000)
        
        print("正在访问文档主页...")
        page.goto(INIT_URL, wait_until="domcontentloaded")
        
        # 等待左侧导航栏加载
        page.wait_for_selector('nav.menu', state="attached")
        print("检测到导航菜单，正在展开所有项目...")
        
        # 获取所有文档链接及其层级关系
        doc_links = get_doc_links_with_hierarchy(page)
        print(f"发现 {len(doc_links)} 个文档页面")
        
        # 爬取每个页面
        for i, doc_info in enumerate(doc_links):
            url = doc_info["url"]
            level1_index = doc_info["level1_index"]
            level1_title = doc_info["level1_title"]
            level2_title = doc_info["level2_title"]
            level2_index = doc_info["level2_index"]
            
            try:
                print(f"正在处理 ({i+1}/{len(doc_links)}): {url}")
                print(f"一级目录: {level1_index}-{level2_index}-{level1_title}, 二级目录: {level2_title}")
                
                # 使用新页面避免状态污染
                doc_page = context.new_page()
                doc_page.goto(url, wait_until="networkidle")
                
                # 等待主要内容加载
                doc_page.wait_for_selector('h1', state="attached")
                
                # 获取页面标题（用于内容）
                title_element = doc_page.query_selector('h1')
                content_title = title_element.inner_text() if title_element else level2_title
                
                # 获取主要内容
                main_content = extract_main_content(doc_page)
                if not main_content:
                    print(f"⚠️ 未找到内容: {url}")
                    doc_page.close()
                    continue
                
                content_html = main_content.inner_html()
                
                # 转换为 Markdown
                markdown_content = f"# {content_title}\n\n"
                markdown_content += h.handle(content_html)
                
                # 生成文件名
                filename = sanitize_filename(level1_index,level2_index, level1_title, level2_title)
                filepath = os.path.join(OUTPUT_DIR, filename)
                
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f'[原始页面地址]({url})\n数据获取时间 {current_time}\n\n{markdown_content}')
                
                print(f"✅ 已保存: {filename}")
                doc_page.close()
                
            except Exception as e:
                print(f"❌ 处理 {url} 时出错: {str(e)}")
                if 'doc_page' in locals():
                    doc_page.close()
        
        browser.close()

if __name__ == "__main__":
    crawl_docs()
    print(f"爬取完成! 所有文档已保存到 {OUTPUT_DIR} 目录")
from playwright.sync_api import sync_playwright

def getChannelHrefs():
    try:
        with sync_playwright() as p:
            browser = p.firefox.launch(headless=False)
            page = browser.new_page()
            page.goto('https://www.youtube.com')

            # Wait for the main content to load using a specific selector
            main_content_page_selector = 'ytd-rich-grid-renderer'
            page.wait_for_selector(main_content_page_selector, state='visible')

            # Query all elements matching the selector
            items = page.query_selector_all(main_content_page_selector)

            hrefs = []

            # Iterate over items and extract href attributes
            for item in items:
                channel_href = item.evaluate('(element) => element.querySelector("a").href')
                hrefs.append(channel_href)

            return hrefs
    except Exception as e:
        print('Error in getting channel hrefs:', e)
        return []

channel_hrefs = getChannelHrefs()
for href in channel_hrefs:
    print(f"Channel Href: {href}")

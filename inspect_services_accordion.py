import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1400,900")

driver = webdriver.Chrome(options=options)
try:
    driver.get("http://127.0.0.1:8000/")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 600);")
    time.sleep(1)

    headers = driver.find_elements("css selector", ".framer-12x9h0a")
    print(f"Clicking header 0...")
    headers[0].click()
    time.sleep(1)

    bullets = driver.execute_script("""
        var ps = [];
        document.querySelectorAll('.framer-188sluc p').forEach(p => ps.push(p.textContent));
        return ps;
    """)
    print("Bullets found:", bullets)

    # Let's inspect the outerHTML of the whole services accordion component
    acc = driver.find_element("css selector", ".framer-OV4kG")
    print("Accordion outerHTML length:", len(acc.get_attribute("outerHTML")))

finally:
    driver.quit()

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
    time.sleep(2)

    # Find any image with yellow or desk or search all background-images
    res = driver.execute_script("""
        var all = document.querySelectorAll('*');
        var found = [];
        for (var i = 0; i < all.length; i++) {
            var el = all[i];
            var bg = window.getComputedStyle(el).backgroundImage;
            if (bg && bg !== 'none' && bg.indexOf('gradient') === -1) {
                var r = el.getBoundingClientRect();
                found.push({
                    tag: el.tagName,
                    cls: el.className,
                    bg: bg,
                    top: Math.round(r.top),
                    left: Math.round(r.left),
                    width: Math.round(r.width),
                    height: Math.round(r.height)
                });
            }
        }
        return found;
    """)
    print("Found background images:")
    for f in res:
        print("  ", f)

    # Also search all img tags everywhere on page
    imgs = driver.execute_script("""
        var found = [];
        document.querySelectorAll('img').forEach(function(img) {
            var r = img.getBoundingClientRect();
            found.push({
                src: img.src,
                alt: img.alt,
                cls: img.className,
                top: Math.round(r.top),
                left: Math.round(r.left),
                w: Math.round(r.width),
                h: Math.round(r.height)
            });
        });
        return found;
    """)
    print("\nAll img tags on page:")
    for im in imgs:
        print("  ", im)

finally:
    driver.quit()

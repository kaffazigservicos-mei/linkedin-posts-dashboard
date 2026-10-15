# extrair_posts.py — Extração direta do LinkedIn
import csv, time, sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

PERFIL_URL = "https://www.linkedin.com/in/SEU-USUARIO/detail/recent-activity/shares/"

def main(url=None):
    target = url or (sys.argv[1] if len(sys.argv) > 1 else PERFIL_URL)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    try:
        driver.get("https://www.linkedin.com/login")
        input("⚠️ Faça login e pressione Enter...")
        driver.get(target); time.sleep(5)
        last_h = 0
        for i in range(500):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            h = driver.execute_script("return document.body.scrollHeight")
            if h == last_h: break
            last_h = h; print(f"📌 Scroll {i+1} — altura {h}")
        for _ in range(5):
            btns = driver.find_elements(By.XPATH,
                "//button[contains(@class,'feed-shared-inline-show-more-text') "
                "or contains(.,'ver mais') or contains(.,'see more')]")
            if not btns: break
            for b in btns:
                try: driver.execute_script("arguments[0].click();", b)
                except Exception: pass
            time.sleep(2)
        posts = driver.find_elements(By.CSS_SELECTOR,
            "li.profile-creator-shared-feed-update__container, .feed-shared-update-v2")
        with open("meus_posts.csv", "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(["Data", "Texto", "Link"]); n = 0
            for post in posts:
                try:
                    txt = post.text.strip()
                    t = post.find_element(By.TAG_NAME, "time")
                    data = t.get_attribute("datetime") or t.text
                    link_el = post.find_elements(By.CSS_SELECTOR,
                        "a[data-test-app-aware-link], a[href*='/feed/update']")
                    link = link_el[0].get_attribute("href") if link_el else ""
                    if txt: w.writerow([data, txt, link]); n += 1
                except Exception: continue
        print(f"✅ {n} posts salvos em meus_posts.csv")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
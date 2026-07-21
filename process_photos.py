import os
from PIL import Image

# 支援 iPhone HEIC 格式
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    print("⚠️ 未安裝 pillow-heif，如果資料夾內有 .heic 相片可能會報錯。")

# 1. ⚠️ 請確認這是你存放 #L001 ~ #L262 資料夾的真實路徑 (請更改最後的資料夾名稱)
SOURCE_DIR = '/Users/pngggg/Downloads/pesmireLF/1PesmireLF/set'  # <-- 請改做你真實嘅路徑

TARGET_DIR = './images'

# 允許的相片格式
VALID_EXTS = ('.jpg', '.jpeg', '.png', '.webp', '.heic', '.tif', '.tiff')

if not os.path.exists(SOURCE_DIR):
    print(f"❌ 找不到來源資料夾：{SOURCE_DIR}")
    exit()

print("🚀 開始診斷並使用 Pillow 處理相片...")

folders = sorted([f for f in os.listdir(SOURCE_DIR) if not f.startswith('.')])

for folder_name in folders:
    folder_path = os.path.join(SOURCE_DIR, folder_name)

    if os.path.isdir(folder_path):
        # 清除 '#' 並轉做細楷 (例如 #L001 會自動變成 l001)
        clean_folder_name = folder_name.replace('#', '').lower()

        out_folder = os.path.join(TARGET_DIR, clean_folder_name)
        os.makedirs(out_folder, exist_ok=True)

        # 抓取該資料夾內所有照片
        all_files = os.listdir(folder_path)
        images = sorted([img for img in all_files if img.lower().endswith(VALID_EXTS)])

        if not images:
            print(f"⚠️ {folder_name} 裡面找不到任何圖片檔案 (內有 {len(all_files)} 個非圖片檔案)")
            continue

        count = 1
        for img_name in images:
            src_img = os.path.join(folder_path, img_name)
            dst_webp = os.path.join(out_folder, f"{count}.webp")

            try:
                # 使用 Pillow 開啟相片
                with Image.open(src_img) as img:
                    # 轉換為 RGB (避免 PNG 等透明底報錯)
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    
                    # 強制儲存為 webp，品質設定為 85
                    img.save(dst_webp, "WEBP", quality=85)
                    
            except Exception as e:
                print(f"  ❌ 轉換失敗 {img_name}: {e}")

            count += 1

        print(f"  ✅ {folder_name} ➔ 已成功轉檔 {count-1} 張 webp 相片到 images/{clean_folder_name}/")

print("\n🎉 全部處理完畢！請打開 images/ 資料夾查看相片。")
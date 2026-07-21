import os
import json

IMAGES_DIR = 'images'
JSON_FILE = 'products.json'

# 新商品的預設範本
DEFAULT_TEMPLATE = {
    "price": 480,
    "colors": ["black", "white"],
    "sizes": ["S", "M", "L"],
    "description": [
        "minimalist high-fashion silhouette",
        "crafted with premium comfort fabric",
        "tailored for versatile daily wardrobe"
    ]
}

def get_category_by_prefix(folder_id):
    """根據商品 ID 的前綴 (Prefix) 自動判斷 Category 及 SubCategory"""
    prefix = folder_id.lower()
    
    if prefix.startswith('df'):
        return "bottom", "短褲"
    elif prefix.startswith('f'):
        return "bottom", "長褲"
    elif prefix.startswith('j'):
        return "top", "外套"
    elif prefix.startswith('p'):
        return "set", ""
    elif prefix.startswith('t'):
        return "top", "短袖背心"
    elif prefix.startswith('l'):
        return "top", "長袖"
    elif prefix.startswith('c'):  # 🆕 新增：c 開頭 -> 配飾 (accessory) -> 帽
        return "accessory", "帽"
    elif prefix.startswith('a'):
        return "accessory", "其他"
    else:
        return "other", "other"

def generate_products_json():
    existing_products = {}

    # 1. 讀取現有的 products.json (保護你手動修改過的名稱/價格/細節)
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    existing_products[item['id']] = item
            print(f"成功讀取現有 {len(existing_products)} 件商品資料。")
        except Exception as e:
            print(f"讀取舊 JSON 失敗，將重新建立: {e}")

    if not os.path.exists(IMAGES_DIR):
        print(f"錯誤：找不到 '{IMAGES_DIR}' 資料夾！請先建立 images 資料夾。")
        return

    updated_products_list = []
    valid_extensions = ('.webp', '.jpg', '.jpeg', '.png')

    # 2. 掃描 images/ 裡面的單層商品資料夾 (例如 images/j001, images/c001)
    folders = [f for f in os.listdir(IMAGES_DIR) if os.path.isdir(os.path.join(IMAGES_DIR, f))]
    folders.sort()

    for folder_id in folders:
        folder_path = os.path.join(IMAGES_DIR, folder_id)
        
        # 自動計算相片數量
        image_files = [img for img in os.listdir(folder_path) if img.lower().endswith(valid_extensions)]
        image_count = len(image_files)

        if image_count == 0:
            print(f"⚠️ 警告: 資料夾 {folder_id} 內沒有圖片，已跳過。")
            continue

        # 根據代號前綴 (Prefix) 自動判定分類
        category, sub_category = get_category_by_prefix(folder_id)

        # 情況 A：如果商品已存在，保留你手動改過的資料，自動更新分類、圖片數量與補齊 Missing 欄位
        if folder_id in existing_products:
            item = existing_products[folder_id]
            item['imageCount'] = image_count
            item['category'] = category
            item['subCategory'] = sub_category

            # 自動補全缺失的 Size / Color / Description 欄位
            if 'colors' not in item: item['colors'] = DEFAULT_TEMPLATE['colors']
            if 'sizes' not in item: item['sizes'] = DEFAULT_TEMPLATE['sizes']
            if 'description' not in item: item['description'] = DEFAULT_TEMPLATE['description']

            updated_products_list.append(item)
            print(f"✓ 更新商品 #{folder_id} -> 分類: [{category} / {sub_category or '無'}] (相片: {image_count} 張)")

        # 情況 B：全新商品，自動建立並帶入 Prefix 對應的分類
        else:
            new_item = {
                "id": folder_id,
                "name": f"{folder_id} item",
                "price": DEFAULT_TEMPLATE['price'],
                "category": category,
                "subCategory": sub_category,
                "imageCount": image_count,
                "colors": DEFAULT_TEMPLATE['colors'],
                "sizes": DEFAULT_TEMPLATE['sizes'],
                "description": DEFAULT_TEMPLATE['description']
            }
            updated_products_list.append(new_item)
            print(f"+ 新增商品 #{folder_id} -> 分類: [{category} / {sub_category or '無'}] (相片: {image_count} 張)")

    # 3. 寫入 products.json
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(updated_products_list, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 成功！`{JSON_FILE}` 已更新完畢，目前共有 {len(updated_products_list)} 件商品。")

if __name__ == '__main__':
    generate_products_json()
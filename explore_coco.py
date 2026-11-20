
import json
from pathlib import Path
from collections import defaultdict

from PIL import Image, ImageDraw

# 1. Find the project directory
project_dir = Path(__file__).resolve().parent

# 2. Locate the annotation file
json_path = (
    project_dir / "data" / "idd" /
    "annotations" / "instances.json"
)

# 3. Load the JSON file
with open(json_path, "r", encoding="utf-8") as file:
    coco = json.load(file)

print("COCO JSON loaded successfully!")

# 4. Read the three main sections
images = coco["images"]
categories = coco["categories"]
annotations = coco["annotations"]

# 5. Print dataset summary
print("\nDATASET SUMMARY")
print("Images:", len(images))
print("Categories:", len(categories))
print("Annotations:", len(annotations))

# 6. Print category information
print("\nAVAILABLE CATEGORIES")
for category in categories:
    print(category["id"], ":", category["name"])

# 7. Print image information
print("\nIMAGE INFORMATION")
for image in images:
    print(
        "Image ID:", image["id"],
        "| File:", image["file_name"],
        "| Width:", image["width"],
        "| Height:", image["height"]
    )

# 8. Print object annotations
print("\nOBJECT ANNOTATIONS")
for annotation in annotations:
    print(
        "Image ID:", annotation["image_id"],
        "| Category ID:", annotation["category_id"],
        "| Bounding Box:", annotation["bbox"]
    )

# 9. Count objects in each category
print("\nOBJECTS PER CATEGORY")

category_counts = {
    category["id"]: 0 for category in categories
}

for annotation in annotations:
    category_counts[annotation["category_id"]] += 1

for category in categories:
    print(
        category["id"], ":",
        category["name"],
        category_counts[category["id"]]
    )

# 10. Count images with and without annotations
annotated_image_ids = {
    annotation["image_id"] for annotation in annotations
}

images_with_annotations = sum(
    1 for image in images
    if image["id"] in annotated_image_ids
)

images_without_annotations = (
    len(images) - images_with_annotations
)

print("\nImages with annotations:", images_with_annotations)
print("Images without annotations:", images_without_annotations)

# 11. Verification checks
image_details = {
    image["id"]: image for image in images
}

category_ids = {
    category["id"] for category in categories
}

check_image = all(
    annotation["image_id"] in image_details
    for annotation in annotations
)

check_category = all(
    annotation["category_id"] in category_ids
    for annotation in annotations
)

check_bbox_size = all(
    annotation["bbox"][2] > 0
    and annotation["bbox"][3] > 0
    for annotation in annotations
)

check_bbox_inside = all(
    annotation["bbox"][0] >= 0
    and annotation["bbox"][1] >= 0
    and annotation["bbox"][0] + annotation["bbox"][2]
    <= image_details[annotation["image_id"]]["width"]
    and annotation["bbox"][1] + annotation["bbox"][3]
    <= image_details[annotation["image_id"]]["height"]
    for annotation in annotations
)

print("\nVERIFICATION CHECKS")
print(
    "Every annotation points to an existing image:",
    "PASS" if check_image else "FAIL"
)
print(
    "Every annotation points to an existing category:",
    "PASS" if check_category else "FAIL"
)
print(
    "Every box has width > 0 and height > 0:",
    "PASS" if check_bbox_size else "FAIL"
)
print(
    "Every box lies inside its image:",
    "PASS" if check_bbox_inside else "FAIL"
)

# 12. Prepare image visualization
image_dir = project_dir / "data" / "idd" / "images"
output_dir = project_dir / "docs"
output_dir.mkdir(parents=True, exist_ok=True)

# Select image ID to visualize
TARGET_IMAGE_ID = 3

# Convert category IDs into category names
category_names = {
    category["id"]: category["name"]
    for category in categories
}

# Group annotations by image ID
annotations_by_image = defaultdict(list)

for annotation in annotations:
    annotations_by_image[annotation["image_id"]].append(annotation)

# Find an image that exists and has annotations
selected_image = None

for image_info in images:
    if (
        TARGET_IMAGE_ID is not None
        and image_info["id"] != TARGET_IMAGE_ID
    ):
        continue

    candidate = image_dir / image_info["file_name"]

    if (
        candidate.exists()
        and annotations_by_image[image_info["id"]]
    ):
        selected_image = image_info
        break

# 13. Draw bounding boxes
print("\nDRAWING")

if selected_image is None:
    print("No matching annotated image found. Check image names and paths.")

else:
    image_path = image_dir / selected_image["file_name"]

    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    for annotation in annotations_by_image[selected_image["id"]]:

        x, y, width, height = annotation["bbox"]

        x1, y1 = x, y
        x2, y2 = x + width, y + height

        label = category_names.get(
            annotation["category_id"], "Unknown"
        )

        draw.rectangle(
            [x1, y1, x2, y2],
            outline="red",
            width=3
        )

        label_position = (x1, max(0, y1 - 15))

        draw.rectangle(
            draw.textbbox(label_position, label),
            fill="red"
        )

        draw.text(
            label_position,
            label,
            fill="white"
        )

    output_path = (
        output_dir /
        f"coco_preview_{selected_image['id']}.jpg"
    )

    image.save(output_path)

    print("Preview saved to:", output_path)

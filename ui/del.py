from PIL import Image

# Use the original uploaded logo and crop/resize it for header use
original_logo_path = "concept_works_logo.jpeg"
logo_image = Image.open(original_logo_path).convert("RGB")

# Optionally crop the logo if needed - assuming it's centered
# You can customize this based on your design needs
cropped_logo = logo_image.crop((0, 0, logo_image.width, int(logo_image.height * 0.5)))
final_logo_path = "concept_logo_cleaned.jpeg"
cropped_logo.save(final_logo_path)
print("completed ")


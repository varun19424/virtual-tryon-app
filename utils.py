from PIL import Image
import cv2
import numpy as np
from rembg import remove
import mediapipe as mp

FIXED_SIZE = (512, 768)  # width x height

def preprocess_image(image_path):
    img = Image.open(image_path).convert("RGBA")
    return img.resize(FIXED_SIZE)


def remove_background(input_path, output_path):
    with open(input_path, "rb") as f:
        input_data = f.read()
    output_data = remove(input_data)
    with open(output_path, "wb") as f:
        f.write(output_data)


def get_neck_position(image_path):
    mp_face = mp.solutions.face_mesh
    face_mesh = mp_face.FaceMesh(static_image_mode=True)
    img = cv2.imread(image_path)
    img = cv2.resize(img, FIXED_SIZE)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark
        w, h = FIXED_SIZE
        x = int(landmarks[152].x * w)
        y = int(landmarks[152].y * h)
        return x, y
    return None


def overlay_clothing_fixed(user_img_path, cloth_img_path, output_path):
    try:
        # Resize both user and cloth
        user_img = preprocess_image(user_img_path)
        user_img.save("resized_user.png")

        cloth_input = preprocess_image(cloth_img_path)
        cloth_input.save("resized_cloth.png")

        # Remove background from cloth
        cleaned_cloth_path = cloth_img_path.replace(".png", "_nobg.png")
        remove_background("resized_cloth.png", cleaned_cloth_path)
        cloth_img = Image.open(cleaned_cloth_path).convert("RGBA")

        # Get neck position
        neck = get_neck_position("resized_user.png")
        if not neck:
            print("[ERROR] Neck detection failed.")
            return False

        # Resize cloth to 80% of fixed width
        cloth_width = int(FIXED_SIZE[0] * 0.8)
        cloth_height = int(cloth_width * cloth_img.height / cloth_img.width)
        cloth_img = cloth_img.resize((cloth_width, cloth_height))

        # Align t-shirt to neck
        paste_x = neck[0] - cloth_width // 2
        paste_y = neck[1] + 10

        # Overlay
        result = Image.new("RGBA", FIXED_SIZE)
        result.paste(user_img, (0, 0))
        result.paste(cloth_img, (paste_x, paste_y), cloth_img)
        result.save(output_path)
        print(f"[OK] Image saved to {output_path}")
        return True

    except Exception as e:
        print(f"[ERROR] {e}")
        return False

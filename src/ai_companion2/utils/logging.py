import os

def log_image(img_path: str):
    try:
        img_path = str(img_path)
    except FileNotFoundError as e:
        print(f"Error logging image: {e}")
        return
    
    print(f"Image logged: {img_path}")
    print(f"Image Size: {os.path.getsize(img_path)} bytes")

def delete_log(img_path: str):
    try:
        img_path = str(img_path)
        if os.path.exists(img_path):
            os.remove(img_path)
            print(f"Image log deleted: {img_path}")
        else:
            print(f"Image log not found for deletion: {img_path}")
    except Exception as e:
        print(f"Error deleting image log: {e}")
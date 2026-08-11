from pathlib import Path
import pandas as pd
import shutil

image_folders = Path(r"C:\Users\brand\Downloads\V4_tuning_curve_images\tuning_curve_images")
for folder in image_folders.iterdir():
    if folder.is_dir():
        new_dir = Path(f"sorting/{folder.name}")
        new_dir.mkdir(parents=True, exist_ok=True)
        obj_folder = Path(folder)
        files = sorted(obj_folder.iterdir())
        for index, img in enumerate(files):
            if img.is_file():
                if index <= 100 and index % 5 == 0:
                    shutil.copy(img, new_dir)
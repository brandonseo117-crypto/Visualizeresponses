from pathlib import Path
import pandas as pd
import shutil

# new_dir = Path('imagesforgames')
# new_dir.mkdir(parents=True, exist_ok=True)
# image_dir = Path(r"C:\Users\brand\Downloads\images_211022")

# df = pd.read_csv(r"C:\Users\brand\Downloads\total.csv")

# for row_name, row_data in df.iterrows():
#     subfolder = Path(f"{new_dir}/neuron{row_name + 1}")
#     subfolder.mkdir(parents=True, exist_ok=True)
#     data = row_data[1:21]
#     counter = 1
#     for number in data:
#         num = int(number)
#         search_term = f"image{num:04d}.jpg"
#         matched_files = list(image_dir.glob(search_term))
#         if len(matched_files) == 1:
#             new_filepath = subfolder / f"img{counter:02d}.jpg"
#             shutil.copy(matched_files[0], new_filepath)
#             counter += 1
#         elif len(matched_files) > 1:
#             print(f'what the heck man: Multiple files found for {search_term}')
#         else:
#             print(f'File not found: {search_term}')

# NEW CODE FOR IMAGE BEAGLE IMAGES

image_folders = Path(r"C:\Users\brand\Downloads\V4_tuning_curve_images\tuning_curve_images")
for folder in image_folders.iterdir():
    if folder.is_dir():
        new_dir = Path(f"imagesforsorting/{folder.name}")
        new_dir.mkdir(parents=True, exist_ok=True)
        obj_folder = Path(folder)
        files = sorted(obj_folder.iterdir())
        for index, img in enumerate(files):
            if img.is_file():
                if index % 5 == 0 and not index > 100:
                    shutil.copy(img, new_dir)
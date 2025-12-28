import os
import shutil
import random

# CONFIGURATION
# Where your raw images/txt files are right now
SOURCE_DIR = 'data' 
# Where we want to move them for YOLO
DEST_DIR = 'datasets/stairs_data' 

def setup_folders():
    # Create the standard YOLO directory structure
    for split in ['train', 'val']:
        os.makedirs(f'{DEST_DIR}/images/{split}', exist_ok=True)
        os.makedirs(f'{DEST_DIR}/labels/{split}', exist_ok=True)

def split_data():
    # Get list of all images (jpg, png, jpeg)
    files = [f for f in os.listdir(SOURCE_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    # Shuffle them so the test is fair
    random.shuffle(files)
    
    # Split: 80% for training, 20% for validation
    split_index = int(len(files) * 0.8)
    train_files = files[:split_index]
    val_files = files[split_index:]
    
    # Helper function to move files
    def move_files(file_list, split_name):
        for filename in file_list:
            # 1. Move Image
            src_img = os.path.join(SOURCE_DIR, filename)
            dst_img = os.path.join(DEST_DIR, 'images', split_name, filename)
            shutil.copy(src_img, dst_img)
            
            # 2. Move Label (Change .jpg to .txt)
            label_name = os.path.splitext(filename)[0] + '.txt'
            src_label = os.path.join(SOURCE_DIR, label_name)
            dst_label = os.path.join(DEST_DIR, 'labels', split_name, label_name)
            
            # Only move label if it exists (it should!)
            if os.path.exists(src_label):
                shutil.copy(src_label, dst_label)
                
    print(f"Moving {len(train_files)} images to TRAIN...")
    move_files(train_files, 'train')
    
    print(f"Moving {len(val_files)} images to VAL...")
    move_files(val_files, 'val')
    
    print("Done! Data organized.")

if __name__ == "__main__":
    setup_folders()
    split_data()
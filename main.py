import os
from PIL import Image, ImageTk
import imagehash
from tqdm import tqdm
import tkinter as tk
from tkinter import Label, Button, messagebox

# Задаем порог схожести
SIMILARITY_THRESHOLD = 10  # Можно варьировать от 0 до 64


def hash_image(image_path):
    with Image.open(image_path) as img:
        return imagehash.dhash(img)


def find_similar_images(image_folder):
    hashes = {}
    duplicates = []

    all_files = [os.path.join(image_folder, file) for file in os.listdir(image_folder)]

    for image_path in tqdm(all_files, desc="Processing", unit="file"):
        try:
            img_hash = hash_image(image_path)
            found_similar = False
            for existing_hash, existing_path in hashes.items():
                if img_hash - existing_hash < SIMILARITY_THRESHOLD:
                    duplicates.append((image_path, existing_path))
                    found_similar = True
                    break
            if not found_similar:
                hashes[img_hash] = image_path
        except Exception as e:
            print(f"Error processing {image_path}: {e}")

    return duplicates


def copy_to_clipboard(root, text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()


def show_images_with_labels(image1_path, image2_path, compare_folder, remaining_duplicates):
    root = tk.Tk()
    root.title(f"Compare Images - {remaining_duplicates} remaining")

    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)
    original_resolution1 = f"{image1.width}x{image1.height}"
    original_resolution2 = f"{image2.width}x{image2.height}"

    max_size = (400, 400)
    image1.thumbnail(max_size)
    image2.thumbnail(max_size)

    img1_tk = ImageTk.PhotoImage(image1)
    img2_tk = ImageTk.PhotoImage(image2)

    label1 = Label(root, text=os.path.basename(image1_path))
    label1.grid(row=0, column=0)

    label2 = Label(root, text=os.path.basename(image2_path))
    label2.grid(row=0, column=1)

    img_label1 = Label(root, image=img1_tk)
    img_label1.grid(row=1, column=0)

    img_label2 = Label(root, image=img2_tk)
    img_label2.grid(row=1, column=1)

    resolution_label1 = Label(root, text=f"Original Resolution: {original_resolution1}")
    resolution_label1.grid(row=2, column=0)

    resolution_label2 = Label(root, text=f"Original Resolution: {original_resolution2}")
    resolution_label2.grid(row=2, column=1)

    def copy_name1():
        name_without_ext = os.path.splitext(os.path.basename(image1_path))[0]
        copy_to_clipboard(root, name_without_ext)
        messagebox.showinfo("Info", f"Name '{name_without_ext}' copied to clipboard.")

    def copy_name2():
        name_without_ext = os.path.splitext(os.path.basename(image2_path))[0]
        copy_to_clipboard(root, name_without_ext)
        messagebox.showinfo("Info", f"Name '{name_without_ext}' copied to clipboard.")

    copy_button1 = Button(root, text="Copy Name", command=copy_name1)
    copy_button1.grid(row=3, column=0, padx=10, pady=10)

    copy_button2 = Button(root, text="Copy Name", command=copy_name2)
    copy_button2.grid(row=3, column=1, padx=10, pady=10)

    def delete_image1():
        os.remove(image1_path)
        print(f"{image1_path} deleted.")
        messagebox.showinfo("Info", f"{os.path.basename(image1_path)} deleted.")
        root.destroy()

    def delete_image2():
        os.remove(image2_path)
        print(f"{image2_path} deleted.")
        messagebox.showinfo("Info", f"{os.path.basename(image2_path)} deleted.")
        root.destroy()

    def keep_both():
        print("Both images kept.")
        root.destroy()

    delete_button1 = Button(root, text="Delete First Image", command=delete_image1)
    delete_button1.grid(row=4, column=0, padx=10, pady=10)

    delete_button2 = Button(root, text="Delete Second Image", command=delete_image2)
    delete_button2.grid(row=4, column=1, padx=10, pady=10)

    keep_button = Button(root, text="Keep Both", command=keep_both)
    keep_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()


def prompt_user(duplicates, compare_folder):
    total_duplicates = len(duplicates)
    print(f"Total duplicates found: {total_duplicates}")

    for index, (img1, img2) in enumerate(duplicates):
        remaining = total_duplicates - index
        print(f"The images '{os.path.basename(img1)}' and '{os.path.basename(img2)}' are similar.")
        print(f"Processing {remaining} duplicates left.")
        show_images_with_labels(img1, img2, compare_folder, remaining)


if __name__ == "__main__":
    compare_folder = "input_folder"
    duplicates = find_similar_images(compare_folder)

    if duplicates:
        prompt_user(duplicates, compare_folder)
    else:
        print("No similar images found.")

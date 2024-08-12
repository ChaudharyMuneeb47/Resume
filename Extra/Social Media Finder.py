import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def find_social_media_profiles(url, platform_to_find):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    pattern = {
        'Facebook': r"https?://(www\.)?facebook\.com/[^/\s]+/?",
        'Twitter': r"https?://(www\.)?twitter\.com/[^/\s]+/?",
        'Instagram': r"https?://(www\.)?instagram\.com/[^/\s]+/?",
        'LinkedIn': r"https?://(www\.)?linkedin\.com/[^/\s]+/?",
    }.get(platform_to_find, "")

    if not pattern:
        return []

    links = soup.find_all('a', href=re.compile(pattern, re.IGNORECASE))
    profiles = [link['href'] for link in links]

    return profiles

def fetch_profiles():
    platform_to_find = platform_combobox.get()
    urls = urls_entry.get("1.0", "end").splitlines()

    results = []

    for url in urls:
        profiles = find_social_media_profiles(url, platform_to_find)
        if profiles:
            results.extend(profiles)
        else:
            results.append(f"No {platform_to_find} profiles found on {url}.")

    result_text.delete("1.0", "end")
    result_text.insert("end", "\n".join(results))

def save_to_excel():
    data = result_text.get("1.0", "end").splitlines()

    df = pd.DataFrame(data, columns=["Profiles"])
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        df.to_excel(file_path, index=False)

# Create the main window
root = tk.Tk()
root.title("Social Media Profile Finder")

# Create and place widgets
platform_label = ttk.Label(root, text="Social Media Platform:")
platform_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

platform_combobox = ttk.Combobox(root, values=["Facebook", "Twitter", "Instagram", "LinkedIn"])
platform_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="we")
platform_combobox.current(0)

urls_label = ttk.Label(root, text="Enter Website URLs (one per line):")
urls_label.grid(row=1, column=0, padx=5, pady=5, sticky="ne")

urls_entry = tk.Text(root, height=5, width=50)
urls_entry.grid(row=1, column=1, padx=5, pady=5, sticky="we")

fetch_button = ttk.Button(root, text="Fetch Profiles", command=fetch_profiles)
fetch_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

result_label = ttk.Label(root, text="Social Media Profiles:")
result_label.grid(row=3, column=0, padx=5, pady=5, sticky="nw")

result_text = tk.Text(root, height=10, width=50)
result_text.grid(row=3, column=1, padx=5, pady=5, sticky="nwe")

save_button = ttk.Button(root, text="Save to Excel", command=save_to_excel)
save_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Start the Tkinter event loop
root.mainloop()

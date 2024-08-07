import requests
import tkinter as tk
from tkinter import messagebox
import random
import pandas as pd

# Provide your Hunter.io API key here
api_key = "5155dab0ab83f64fea943ad2524ff79dfb2183ad"

def extract_emails():
    company_emails = ["sales@", "help@", "support@", "info@", "hello@", "customercare@", "admin@", "events@", "questions@", "team@", "order@", "wholesale@"]
    domains = domain_entry.get("1.0", tk.END).strip().split("\n")
    if not domains:
        messagebox.showerror("Error", "Please enter domain names")
        return

    results = []
    for domain in domains:
        try:
            response = requests.get(f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={api_key}")
            data = response.json()
            emails = [email['value'] for email in data['data']['emails'] if any(company_email in email['value'] for company_email in company_emails)]
            if emails:
                for email in emails:
                    results.append({'Domain': domain, 'Email': email})
            else:
                results.append({'Domain': domain, 'Email': 'No company emails found'})
        except Exception as e:
            results.append({'Domain': domain, 'Email': f"An error occurred: {e}"})

    # Display results in the text widget
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)  # Clear previous results
    for result in results:
        result_text.insert(tk.END, f"Domain: {result['Domain']}\n")
        result_text.insert(tk.END, f"Email: {result['Email']}\n\n")
    result_text.config(state=tk.DISABLED)

    # Enable save button
    save_button.config(state=tk.NORMAL)

def save_output():
    results = []
    text = result_text.get("1.0", tk.END).strip().split("\n\n")
    for line in text:
        domain, email = line.split("\n")[0][8:], line.split("\n")[1][7:]
        results.append({'Domain': domain, 'Email': email})

    # Create DataFrame from results
    df = pd.DataFrame(results)

    # Save DataFrame to Excel file
    df.to_excel("email_output.xlsx", index=False)

    messagebox.showinfo("Success", "Output saved as email_output.xlsx")

# Create the GUI window
root = tk.Tk()
root.title("Email Extractor")

# Create and place input widgets
domain_label = tk.Label(root, text="Enter domains (one per line):")
domain_label.grid(row=0, column=0, padx=5, pady=5)
domain_entry = tk.Text(root, height=10, width=50)
domain_entry.grid(row=0, column=1, padx=5, pady=5)

# Create and place button to trigger email extraction
extract_button = tk.Button(root, text="Extract Emails", command=extract_emails)
extract_button.grid(row=0, column=2, padx=5, pady=5)

# Create text widget to display results
result_text = tk.Text(root, height=20, width=50, state=tk.DISABLED)
result_text.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

# Create button to save output
save_button = tk.Button(root, text="Save Output", command=save_output, state=tk.DISABLED)
save_button.grid(row=2, column=1, padx=5, pady=5)

# Run the GUI loop
root.mainloop()

# Auto Email Sender (Tkinter + Gmail)

This is a desktop tool built with **Python + Tkinter** to send bulk emails with attachments (e.g., resumes) to a list of recipients stored in an Excel file.
It supports **rich-text formatting** (bold/italic) in the email body and shows a live progress window while sending.

---

## Features

* 📄 Send bulk emails with a **PDF resume** attached.
* 📝 Supports **bold** (Ctrl+B) and **italic** (Ctrl+I) formatting in the email body.
* 🗂 Load recipients directly from an Excel file (`HRs Emails.xlsx`).
* ✅ Progress/status window with **success/failure logs**.
* ⏹ Option to **cancel sending** midway.
* 🔑 Secure login with Gmail **App Password** (not your normal Gmail password).
* 📌 `HRs Emails.xlsx` is already included in the project folder — no need to create or mess with it.
* 📨 A sample email body text is provided in `Sample_Email.md` for quick use (or write your own).

---

## Requirements

* Python **3.8+**
* Required libraries:

  ```bash
  pip install pandas
  ```

Tkinter, smtplib, and email are part of the standard library.

---

## Setup Instructions

1. **Enable App Password in Gmail**

   * Go to your [Google Account Security](https://myaccount.google.com/security) settings.
   * Enable **2-Step Verification**.
   * Generate an **App Password** for "Mail".
   * You’ll get a 16-character password (e.g., `abcd efgh ijkl mnop`).

   ⚠️ Use this App Password in the program, **not your Gmail login password**.

2. **Recipients list (`HRs Emails.xlsx`)**

   * Already included in the project folder.
   * Contains a column named `Emails` with sample HR email addresses.
   * You can edit or replace them if you want.

   Example:

   | Emails                                    |
   | ----------------------------------------- |
   | [hr1@company.com](mailto:hr1@company.com) |
   | [hr2@company.com](mailto:hr2@company.com) |
   | [hr3@company.com](mailto:hr3@company.com) |

3. **Sample Email Body**

   * Check the file `Sample_Email.md` in this repo.
   * Copy-paste the text or modify it for your own needs.

4. **Run the program**

   ```bash
   python auto_email_sender.py
   ```

---

## How to Use

1. Enter your Gmail address.
2. Enter your **App Password** (not Gmail password).
3. Select your **resume (PDF file)**.
4. Enter email subject.
5. Write the email body (use Ctrl+B / Ctrl+I for formatting).
6. Click **Send Emails**.
7. A progress window will open to show status for each recipient.

   * ✅ Sent successfully
   * ❌ Failed with error
   * ⚠ Cancelled (if you stop midway)

---

## Notes

* Only **PDF files** are supported as attachments.
* Keep `HRs Emails.xlsx` in the same directory as the script.
* The tool uses **SMTP (smtp.gmail.com:587)**.
* If you get login errors, double-check:

  * Gmail address is correct.
  * App Password (16 characters) is used.
  * Less secure app access is **NOT needed** (this works with App Passwords).

---

## License

This project is free to use for personal or educational purposes.

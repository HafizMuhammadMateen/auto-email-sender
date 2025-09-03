import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pandas as pd, smtplib, os, re, threading
from email.message import EmailMessage

# ----------------- PLACEHOLDER -----------------
def add_placeholder(entry, placeholder, is_password=False):
    entry.insert(0, placeholder)
    entry.config(fg="grey")
    def on_focus_in(_):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(fg="black", show="*" if is_password else "")
    def on_focus_out(_):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg="grey", show="" if is_password else "")
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# ----------------- HTML BODY PARSER -----------------
def get_html_from_text_widget(text_widget):
    html, index = "", "1.0"
    while True:
        tags = [(s, e, t) for t in ("bold", "italic") if (rng := text_widget.tag_nextrange(t, index)) for s, e in [rng]]
        if not tags:
            html += text_widget.get(index, "end-1c")
            break
        tags.sort(key=lambda x: text_widget.index(x[0]))
        start, end, t = tags[0]
        html += text_widget.get(index, start)
        tag = ("<b>", "</b>") if t=="bold" else ("<i>", "</i>")
        html += tag[0] + text_widget.get(start, end) + tag[1]
        index = end
    html = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', html)
    html = re.sub(r'\*(.+?)\*', r'<i>\1</i>', html)
    return html.replace("\n", "<br>")

# ----------------- TOGGLE FORMATTING -----------------
def toggle_format(tag):
    try:
        sel = ("sel.first", "sel.last")
        if tag in text_body.tag_names("sel.first"):
            text_body.tag_remove(tag, *sel)
        else:
            text_body.tag_add(tag, *sel)
    except tk.TclError:
        pass
main_window = tk.Tk()
main_window.title("Auto Email Sender")

# ----------------- FILE BROWSER -----------------
def browse_resume():
    if (path := filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])):
        entry_resume.delete(0, tk.END)
        entry_resume.insert(0, path)
        entry_resume.config(fg="black")

# ----------------- VALIDATION -----------------
base_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
excel_path = os.path.join(base_dir, "HRs Emails.xlsx")

def validate_inputs():
    values = {
        "email": entry_email.get().strip(),
        "password": entry_pass.get().strip(),
        "resume": entry_resume.get().strip(),
        "subject": entry_subject.get().strip(),
        "body": text_body.get("1.0", tk.END).strip()
    }
    placeholders = {
        "email": "example@gmail.com",
        "password": "Enter Gmail App Password (not email password), e.g. abcd efgh ijkl mnop.",
        "resume": "Select resume PDF file",
        "subject": "Enter email subject"
    }
    for k,v in placeholders.items():
        if values[k] == v: values[k] = ""
    if not all(values.values()):
        messagebox.showwarning("Missing Info", "Please fill all fields before sending.")
        return None
    return values

# ----------------- EMAIL SENDING -----------------
stop_sending = False
def send_emails_thread(status_text, cancel_button):
    global stop_sending
    stop_sending = False
    try:
        if not (inputs := validate_inputs()):
            if 'status_window' in globals() and status_window.winfo_exists():
                status_window.destroy()
            main_window.attributes("-disabled", False)
            return
        df = pd.read_excel(excel_path)
        email_list = df["Emails"].dropna().unique()
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls(); server.login(inputs["email"], inputs["password"])
        body_html, sent = get_html_from_text_widget(text_body), 0
        for rcv in email_list:
            if stop_sending: 
                status_text.insert(tk.END, "\n⚠ Sending cancelled.\n"); break
            msg = EmailMessage()
            msg["From"], msg["To"], msg["Subject"] = inputs["email"], rcv, inputs["subject"]
            msg.add_alternative(body_html, subtype="html")
            with open(inputs["resume"], "rb") as f:
                msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename="Resume.pdf")
            sent += 1
            try:
                server.send_message(msg); status_text.insert(tk.END, f"✅ Sent {sent}. {rcv}\n")
            except Exception as e:
                status_text.insert(tk.END, f"❌ Failed {sent}. {rcv}: {e}\n")
            status_text.see(tk.END)
        server.quit()
        if not stop_sending: status_text.insert(tk.END, "\n✅ All emails processed!\n")
    except Exception as e:
        status_text.insert(tk.END, f"\n❌ Error: {e}\n")
    finally:
        cancel_button.config(text="Close", command=status_window.destroy)
        main_window.attributes("-disabled", False)

def cancel_sending_action():
    global stop_sending
    if messagebox.askyesno("Cancel Sending", "Stop sending emails?"):
        stop_sending = True

def open_status_window():
    if not validate_inputs(): return
    global status_window
    main_window.attributes("-disabled", True)
    status_window = tk.Toplevel(main_window); status_window.title("Sending Emails...")
    w,h = 500,400; sw,sh = status_window.winfo_screenwidth(), status_window.winfo_screenheight()
    status_window.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
    status_window.transient(main_window); status_window.grab_set()
    tk.Label(status_window, text="Sending Progress:").pack(pady=5)
    status_text = scrolledtext.ScrolledText(status_window, width=60, height=20)
    status_text.pack(padx=10, pady=5, fill="both", expand=True)
    cancel_button = tk.Button(status_window, text="Cancel Sending", bg="red", fg="white",
                              font=("Arial", 10, "bold"), command=cancel_sending_action)
    cancel_button.pack(pady=5)
    threading.Thread(target=send_emails_thread, args=(status_text, cancel_button), daemon=True).start()

# ----------------- UI HELPERS -----------------
def create_entry_row(label, placeholder, is_password=False, button=False):
    frame = tk.Frame(main_window); frame.pack(anchor="w", padx=10, pady=2, fill="x")
    tk.Label(frame, text=label, width=20, anchor="w").pack(side="left")
    entry = tk.Entry(frame, width=50); entry.pack(side="left", fill="x", expand=True)
    add_placeholder(entry, placeholder, is_password)
    if button: tk.Button(frame, text="Browse", command=browse_resume, bg="skyblue").pack(side="left", padx=5)
    return entry

# ----------------- BUILD UI -----------------
ww, wh = 600, 500; sw, sh = main_window.winfo_screenwidth(), main_window.winfo_screenheight()
main_window.geometry(f"{ww}x{wh}+{(sw-ww)//2}+{(sh-wh)//2}")
entry_email   = create_entry_row("Your Email:", "example@gmail.com")
entry_pass    = create_entry_row("Password:", "Enter Gmail App Password (not email password), e.g. abcd efgh ijkl mnop.", is_password=True)
entry_resume  = create_entry_row("Resume (PDF):", "Select resume PDF file", button=True)
entry_subject = create_entry_row("Subject:", "Enter email subject")

tk.Label(main_window, text="Email Body (CTRL+B bold | CTRL+I italic):").pack(anchor="w", padx=10, pady=1)
text_body = scrolledtext.ScrolledText(main_window, wrap="word", width=50, height=10, font=("Arial", 10))
text_body.pack(padx=10, pady=5, fill="both", expand=True)
text_body.tag_configure("bold", font=("Arial", 10, "bold"))
text_body.tag_configure("italic", font=("Arial", 10, "italic"))
main_window.bind("<Control-b>", lambda e: toggle_format("bold"))
main_window.bind("<Control-i>", lambda e: toggle_format("italic"))

tk.Button(main_window, text="Send Emails", command=open_status_window, bg="green", fg="white",
          font=("Arial", 12, "bold")).pack(pady=10)

main_window.mainloop()
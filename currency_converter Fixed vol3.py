import tkinter as tk
from tkinter import ttk

# --- Translations ---
LANGUAGES = {
    "English": {
        "title": "Currency Converter",
        "amount_label": "Amount:",
        "from_label": "From:",
        "to_label": "To:",
        "convert_btn": "Convert",
        "result_prefix": "Result:",
        "error_empty": "Please enter a valid number.",
        "error_invalid": "Invalid input. Please enter a number.",
        "lang_title": "Select Language",
        "lang_prompt": "Choose your language:",
        "lang_btn": "Continue",
    },
    "Deutsch": {
        "title": "Währungsrechner",
        "amount_label": "Betrag:",
        "from_label": "Von:",
        "to_label": "Nach:",
        "convert_btn": "Umrechnen",
        "result_prefix": "Ergebnis:",
        "error_empty": "Bitte eine gültige Zahl eingeben.",
        "error_invalid": "Ungültige Eingabe. Bitte eine Zahl eingeben.",
        "lang_title": "Sprache wählen",
        "lang_prompt": "Wähle deine Sprache:",
        "lang_btn": "Weiter",
    },
    "Svenska": {
        "title": "Valutaomvandlare",
        "amount_label": "Belopp:",
        "from_label": "Från:",
        "to_label": "Till:",
        "convert_btn": "Konvertera",
        "result_prefix": "Resultat:",
        "error_empty": "Ange ett giltigt nummer.",
        "error_invalid": "Ogiltigt värde. Ange ett nummer.",
        "lang_title": "Välj språk",
        "lang_prompt": "Välj ditt språk:",
        "lang_btn": "Fortsätt",
    },
    "한국어": {
        "title": "환율 변환기",
        "amount_label": "금액:",
        "from_label": "변환 전:",
        "to_label": "변환 후:",
        "convert_btn": "변환",
        "result_prefix": "결과:",
        "error_empty": "유효한 숫자를 입력해 주세요.",
        "error_invalid": "잘못된 입력입니다. 숫자를 입력해 주세요.",
        "lang_title": "언어 선택",
        "lang_prompt": "언어를 선택하세요:",
        "lang_btn": "계속",
    },
}

# Exchange rates relative to EUR (base = 1 EUR)
RATES = {
    "EUR": 1.0,
    "USD": 1.16,
    "GBP": 0.87,
    "JPY": 184.1,
    "SEK": 10.82,
    "CHF": 0.91,
    "KRW": 1736.2,
    "CNY": 7.98,
}


def pick_language():
    """Show a language selection dialog and return the chosen language key."""
    dialog = tk.Tk()
    chosen = tk.StringVar(value="English")
    dialog.title("Language / Sprache / Språk / 언어")
    dialog.resizable(False, False)
    dialog.eval("tk::PlaceWindow . center")

    # Use English as the bootstrap UI for the dialog itself
    tk.Label(dialog, text="Choose your language:", font=("Helvetica", 12, "bold"), pady=10).pack()

    for lang in LANGUAGES:
        tk.Radiobutton(
            dialog,
            text=lang,
            variable=chosen,
            value=lang,
            font=("Helvetica", 11),
            anchor="w",
        ).pack(fill="x", padx=40)

    def confirm():
        dialog.destroy()

    tk.Button(dialog, text="Continue / Weiter / Fortsätt / 계속", command=confirm,
              font=("Helvetica", 11), pady=6).pack(pady=15)

    dialog.mainloop()
    return chosen.get()


class CurrencyConverter:
    def __init__(self, root, lang_key: str):
        self.root = root
        self.t = LANGUAGES[lang_key]

        self.root.title(self.t["title"])
        self.root.resizable(False, False)

        pad = {"padx": 20, "pady": 6}

        # Amount
        tk.Label(root, text=self.t["amount_label"], font=("Helvetica", 11)).pack(**pad)
        self.amount_entry = tk.Entry(root, font=("Helvetica", 12), width=20, justify="center")
        self.amount_entry.pack(**pad)

        # From currency
        tk.Label(root, text=self.t["from_label"], font=("Helvetica", 11)).pack(**pad)
        self.from_var = tk.StringVar(value="EUR")
        self.from_menu = ttk.Combobox(
            root, textvariable=self.from_var,
            values=list(RATES.keys()), state="readonly",
            font=("Helvetica", 11), width=18
        )
        self.from_menu.pack(**pad)

        # To currency
        tk.Label(root, text=self.t["to_label"], font=("Helvetica", 11)).pack(**pad)
        self.to_var = tk.StringVar(value="USD")
        self.to_menu = ttk.Combobox(
            root, textvariable=self.to_var,
            values=list(RATES.keys()), state="readonly",
            font=("Helvetica", 11), width=18
        )
        self.to_menu.pack(**pad)

        # Convert button
        tk.Button(
            root, text=self.t["convert_btn"],
            command=self.convert,
            font=("Helvetica", 12, "bold"),
            bg="#4a90d9", fg="white",
            padx=10, pady=6, relief="flat", cursor="hand2"
        ).pack(pady=12)

        # Result label
        self.result_label = tk.Label(root, text="", font=("Helvetica", 12), wraplength=280)
        self.result_label.pack(pady=8)

    def convert(self):
        raw = self.amount_entry.get().strip()

        if not raw:
            self.result_label.config(text=self.t["error_empty"], fg="red")
            return

        try:
            amount = float(raw.replace(",", "."))
        except ValueError:
            self.result_label.config(text=self.t["error_invalid"], fg="red")
            return

        from_cur = self.from_var.get()
        to_cur = self.to_var.get()

        # Convert via EUR as base
        amount_in_eur = amount / RATES[from_cur]
        converted = amount_in_eur * RATES[to_cur]

        result_text = f"{self.t['result_prefix']}  {amount:,.2f} {from_cur} = {converted:,.2f} {to_cur}"
        self.result_label.config(text=result_text, fg="green")


if __name__ == "__main__":
    selected_language = pick_language()

    root = tk.Tk()
    root.eval("tk::PlaceWindow . center")
    app = CurrencyConverter(root, selected_language)
    root.mainloop()

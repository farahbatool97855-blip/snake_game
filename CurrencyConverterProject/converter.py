import tkinter as tk
from tkinter import ttk, messagebox
import requests

class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("💱 Premium Currency Converter")
        self.root.geometry("550x500")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f4f8')

        # Colors and Fonts
        self.primary_color = '#1a237e'   # Dark Blue
        self.accent_color = '#ff6f00'     # Orange
        self.bg_color = '#f0f4f8'
        self.card_color = '#ffffff'
        self.font_title = ('Segoe UI', 20, 'bold')
        self.font_label = ('Segoe UI', 12, 'bold')
        self.font_entry = ('Segoe UI', 14)

        # API URL
        self.api_url = "https://api.exchangerate.host/latest?base=USD"

        # Fetch Rates on Start
        self.rates = {}
        self.fetch_rates()

        # Build UI
        self.build_header()
        self.build_main_card()
        self.build_result_area()
        self.build_footer()

    def fetch_rates(self):
        try:
            response = requests.get(self.api_url, timeout=5)
            data = response.json()
            if data.get('success'):
                self.rates = data['rates']
            else:
                messagebox.showerror("Error", "Failed to fetch exchange rates.")
                self.rates = {'USD': 1, 'PKR': 280, 'EUR': 0.92, 'GBP': 0.79, 'SAR': 3.75, 'AED': 3.67, 'INR': 83.5}
        except:
            messagebox.showerror("Network Error", "Could not connect to API. Using default rates.")
            self.rates = {'USD': 1, 'PKR': 280, 'EUR': 0.92, 'GBP': 0.79, 'SAR': 3.75, 'AED': 3.67, 'INR': 83.5}

    def build_header(self):
        header = tk.Frame(self.root, bg=self.primary_color, height=80)
        header.pack(fill='x', pady=(0, 20))
        title = tk.Label(header, text="💱 Currency Converter", font=self.font_title, bg=self.primary_color, fg='white')
        title.pack(pady=20)

    def build_main_card(self):
        card = tk.Frame(self.root, bg=self.card_color, relief='flat', bd=2)
        card.pack(padx=30, pady=10, fill='x', ipady=15)

        # From Currency
        tk.Label(card, text="From (Base):", font=self.font_label, bg=self.card_color, fg='#333').grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.from_currency = ttk.Combobox(card, values=list(self.rates.keys()), font=self.font_entry, width=15, state='readonly')
        self.from_currency.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.from_currency.set('USD')

        # To Currency
        tk.Label(card, text="To (Target):", font=self.font_label, bg=self.card_color, fg='#333').grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.to_currency = ttk.Combobox(card, values=list(self.rates.keys()), font=self.font_entry, width=15, state='readonly')
        self.to_currency.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        self.to_currency.set('PKR')

        # Amount
        tk.Label(card, text="Amount:", font=self.font_label, bg=self.card_color, fg='#333').grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.amount_entry = tk.Entry(card, font=self.font_entry, width=18, bd=2, relief='solid')
        self.amount_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        self.amount_entry.insert(0, "1.00")

        # Buttons Frame inside card
        btn_frame = tk.Frame(card, bg=self.card_color)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=15)

        # Convert Button (Green/Blue)
        self.convert_btn = tk.Button(btn_frame, text="🔄 Convert", font=('Segoe UI', 14, 'bold'), 
                                     bg='#0d47a1', fg='white', padx=20, pady=8, relief='raised', bd=2,
                                     command=self.perform_conversion)
        self.convert_btn.pack(side='left', padx=10)

        # Swap Button (Orange)
        self.swap_btn = tk.Button(btn_frame, text="⇅ Swap", font=('Segoe UI', 12, 'bold'), 
                                  bg=self.accent_color, fg='white', padx=15, pady=8, relief='raised', bd=2,
                                  command=self.swap_currencies)
        self.swap_btn.pack(side='left', padx=10)

        # Clear Button (Red)
        self.clear_btn = tk.Button(btn_frame, text="✖ Clear", font=('Segoe UI', 12, 'bold'), 
                                   bg='#b71c1c', fg='white', padx=15, pady=8, relief='raised', bd=2,
                                   command=self.clear_all)
        self.clear_btn.pack(side='left', padx=10)

    def build_result_area(self):
        self.result_frame = tk.Frame(self.root, bg=self.bg_color)
        self.result_frame.pack(pady=20, fill='x')

        self.result_label = tk.Label(self.result_frame, text="Result will appear here", 
                                     font=('Segoe UI', 18, 'bold'), bg=self.bg_color, fg='#1a237e')
        self.result_label.pack()

    def build_footer(self):
        footer = tk.Label(self.root, text="Powered by exchangerate.host | Real-time Rates", 
                          font=('Segoe UI', 9, 'italic'), bg=self.bg_color, fg='#888')
        footer.pack(side='bottom', pady=10)

    def perform_conversion(self):
        try:
            from_cur = self.from_currency.get()
            to_cur = self.to_currency.get()
            amount = float(self.amount_entry.get())

            if from_cur not in self.rates or to_cur not in self.rates:
                messagebox.showerror("Error", "Invalid currency selected.")
                return

            # Convert via USD base
            usd_value = amount / self.rates[from_cur]
            converted = usd_value * self.rates[to_cur]
            
            self.result_label.config(text=f"{amount:,.2f} {from_cur}  =  {converted:,.2f} {to_cur}", 
                                     fg='#0d47a1')
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid numeric amount.")
        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")

    def swap_currencies(self):
        from_cur = self.from_currency.get()
        to_cur = self.to_currency.get()
        self.from_currency.set(to_cur)
        self.to_currency.set(from_cur)
        # Auto convert after swap
        self.perform_conversion()

    def clear_all(self):
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, "1.00")
        self.result_label.config(text="Result will appear here", fg='#1a237e')
        self.from_currency.set('USD')
        self.to_currency.set('PKR')

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop()
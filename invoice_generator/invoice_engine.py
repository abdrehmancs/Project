from fpdf import FPDF

class InvoicePDF(FPDF):
    def header(self):
        # Iteration 4: Invoice Templating
        # Header with Company Info
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'OFFICIAL INVOICE', 0, 1, 'C')
        self.ln(5)
        self.set_font('Arial', '', 10)
        self.cell(0, 5, 'TechFlow Solutions', 0, 1, 'L')
        self.cell(0, 5, '123 Innovation Way, Silicon Valley, CA', 0, 1, 'L')
        self.cell(0, 5, 'billing@techflow.com', 0, 1, 'L')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()} - Thank you for your business!', 0, 0, 'C')

def generate_basic_pdf(client_name, item_description, amount, output_filename, tax_rate=0.05, logo_path=None):
    """
    Iteration 7: Dynamic Branding
    Generates a PDF invoice with branding, calculations, and optional logo.
    """
    pdf = InvoicePDF()
    pdf.add_page()

    # Iteration 7: Add Logo if provided
    if logo_path:
        try:
            pdf.image(logo_path, 10, 8, 33)
            pdf.set_x(45) # Move text to the right of the logo
        except Exception as e:
            print(f"Could not load logo: {e}")

    pdf.set_font('Arial', '', 12)

    # Client Info
    pdf.cell(0, 10, f"Client: {client_name}", 0, 1)
    pdf.ln(5)

    # Invoice Table-like layout
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(140, 10, "Description", 1)
    pdf.cell(40, 10, "Amount", 1, 1, 'R')

    pdf.set_font('Arial', '', 12)
    pdf.cell(140, 10, item_description, 1)
    pdf.cell(40, 10, f"${float(amount):.2f}", 1, 1, 'R')

    # Calculations
    subtotal = float(amount)
    tax = subtotal * tax_rate
    total = subtotal + tax

    pdf.ln(5)
    pdf.cell(140, 10, "Subtotal:", 0, 0, 'R')
    pdf.cell(40, 10, f"${subtotal:.2f}", 0, 1, 'R')

    pdf.cell(140, 10, f"Tax ({tax_rate*100:.1f}%):", 0, 0, 'R')
    pdf.cell(40, 10, f"${tax:.2f}", 0, 1, 'R')

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(140, 10, "Total:", 0, 0, 'R')
    pdf.cell(40, 10, f"${total:.2f}", 0, 1, 'R')

    pdf.output(output_filename)
    print(f"Successfully generated {output_filename}")

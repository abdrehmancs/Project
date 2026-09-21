import json
from data_loader import load_client_data
from invoice_engine import generate_basic_pdf
import os

def main():
    # Load Configuration
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return

    input_file = 'clients.csv'

    # Iteration 5: Load data (CSV/Excel)
    clients = load_client_data(input_file)

    if not clients:
        print("No client data found. Exiting.")
        return

    # Iteration 8: Batch Processing & Iteration 10: Organization
    output_dir = 'generated_invoices'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, client in enumerate(clients, start=1001): # Iteration 9: Unique Invoice Numbering
        # Iteration 6: Basic Input Validation
        try:
            name = client['client_name']
            desc = client['item_description']
            amount = client['amount']

            if not name or not desc or not amount:
                raise ValueError("Missing required fields")

        except (KeyError, ValueError) as e:
            print(f"Skipping record {i}: {e}")
            continue

        # Iteration 10: Organize by client name
        client_folder = os.path.join(output_dir, name.replace(' ', '_'))
        if not os.path.exists(client_folder):
            os.makedirs(client_folder)

        filename = f"invoice_{i}.pdf"
        filepath = os.path.join(client_folder, filename)

        generate_basic_pdf(
            name,
            desc,
            amount,
            filepath,
            tax_rate=config['tax_rate']
        )

if __name__ == "__main__":
    main()

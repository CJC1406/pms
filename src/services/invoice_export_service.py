
from html import escape
from pathlib import Path

from src.models.invoice import Invoice


def render_invoice_html(invoice: Invoice) -> str:
    """Render an invoice as print-friendly HTML."""

    rows = []

    for item in invoice.items:
        rows.append(
            f"""
            <tr>
                <td>{escape(item.product_name)}</td>
                <td>{escape(item.sku)}</td>
                <td class="number">{item.quantity}</td>
                <td class="number">₹{item.unit_price:.2f}</td>
                <td class="number">₹{item.line_total:.2f}</td>
            </tr>
            """
        )

    invoice_date = invoice.created_at.strftime("%Y-%m-%d %H:%M UTC")

    mobile_html = (
        f"<p>Mobile: {escape(invoice.customer_mobile)}</p>"
        if invoice.customer_mobile
        else ""
    )

    email_html = (
        f"<p>Email: {escape(invoice.customer_email)}</p>"
        if invoice.customer_email
        else ""
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Invoice {escape(invoice.invoice_number)}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            color: #222;
        }}
        h1 {{
            margin-bottom: 5px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 25px;
        }}
        th, td {{
            border: 1px solid #ccc;
            padding: 10px;
            text-align: left;
        }}
        th {{
            background: #f2f2f2;
        }}
        .number {{
            text-align: right;
        }}
        .total {{
            text-align: right;
            font-size: 1.2em;
            font-weight: bold;
            margin-top: 20px;
        }}
        @media print {{
            body {{
                margin: 15mm;
            }}
            button {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <button onclick="window.print()">Print / Save as PDF</button>

    <h1>Perishables Management System</h1>
    <h2>Invoice</h2>

    <p><strong>Invoice Number:</strong> {escape(invoice.invoice_number)}</p>
    <p><strong>Date:</strong> {escape(invoice_date)}</p>
    <p><strong>Cashier:</strong> {escape(invoice.cashier)}</p>

    <h3>Customer</h3>
    {mobile_html}
    {email_html}

    <table>
        <thead>
            <tr>
                <th>Product</th>
                <th>SKU</th>
                <th class="number">Qty</th>
                <th class="number">Unit Price</th>
                <th class="number">Line Total</th>
            </tr>
        </thead>
        <tbody>
            {"".join(rows)}
        </tbody>
    </table>

    <p class="total">Subtotal: ₹{invoice.subtotal:.2f}</p>
    <p class="total">Total: ₹{invoice.total:.2f}</p>

    <p>Thank you for your purchase!</p>
</body>
</html>
"""


def export_invoice_html(invoice: Invoice, destination: str | Path) -> Path:
    """Write invoice HTML to a file and return its path."""

    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        render_invoice_html(invoice),
        encoding="utf-8",
    )

    return path

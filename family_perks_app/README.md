# P&G Family Perks — Streamlit prototype

A mobile-first demo built around the supplied synthetic receipt database.

## Run locally

1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Create/activate a virtual environment (optional but recommended).
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the app:

   ```bash
   streamlit run app.py
   ```

Streamlit will print a local URL, usually http://localhost:8501.

## What is implemented

- Select one of 300 synthetic consumer profiles.
- Load the supplied `Synthetic Receipts` worksheet.
- Count distinct receipts per product (not units) and flag products bought on 3+ separate receipts.
- Unlock illustrative P&G brand offers when repeat-purchase conditions are met.
- Save an offer to a session-only demo wallet.
- View household spend, repeat products, monthly trend and retailer mix.
- Display a visual Apple Wallet-style membership card.

## Important prototype boundaries

- The supplied workbook is already post-OCR structured receipt data. This demo does not perform OCR on uploaded receipt photos.
- The sample data is synthetic. No real shopper information is used.
- Coupon amounts and offer rules are illustrative, not live P&G promotions.
- The Wallet card is a visual mock-up, not a signed `.pkpass` file. A production pass needs Apple PassKit certificates, secure member identifiers, a barcode payload and retailer/POS integration.
- The synthetic database covers April–September 2026 and includes 300 consumers, 3,005 receipts and 32,776 product-line records.

## Challenge alignment

The prototype demonstrates how incomplete shopping records can be combined into a continuous household purchase history, then translated into consumer-facing savings and behavioural insight. It is a behavioural analytics prototype, not an OCR challenge.

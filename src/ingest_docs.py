"""
Stripe Docs RAG Assistant - Data Ingestion
--------------------------------------------
Downloads a curated set of Stripe documentation pages (Payments, Checkout,
Webhooks) as clean Markdown and saves them locally under data/raw/.

Stripe docs expose a clean markdown export by appending ".md" to any doc URL
(e.g. https://docs.stripe.com/payments/checkout.md), which avoids messy HTML
parsing entirely.
"""

import os
import time
import requests

# Curated list of Stripe doc pages covering Payments, Checkout, and Webhooks.
# Kept intentionally focused rather than crawling the entire docs site.
DOC_URLS = [
    # Payments overview & methods
    "https://docs.stripe.com/payments/payment-methods/overview.md",
    "https://docs.stripe.com/payments/cards.md",
    "https://docs.stripe.com/payments/ach-direct-debit.md",
    "https://docs.stripe.com/payments/bank-transfers.md",
    "https://docs.stripe.com/payments/wallets.md",

    # Checkout
    "https://docs.stripe.com/checkout/quickstart.md",
    "https://docs.stripe.com/payments/checkout/how-checkout-works.md",
    "https://docs.stripe.com/payments/checkout/customization.md",
    "https://docs.stripe.com/payments/checkout/taxes.md",
    "https://docs.stripe.com/payments/checkout/manage-payment-methods.md",

    # Subscriptions (closely tied to checkout/payments in real support questions)
    "https://docs.stripe.com/billing/subscriptions/overview.md",
    "https://docs.stripe.com/billing/subscriptions/creating.md",

    # Webhooks
    "https://docs.stripe.com/webhooks.md",
    "https://docs.stripe.com/webhooks/quickstart.md",

    # Disputes & refunds (common real support questions)
    "https://docs.stripe.com/disputes.md",
    "https://docs.stripe.com/refunds.md",
]

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")


def slugify(url: str) -> str:
    """Turn a doc URL into a safe filename."""
    slug = url.replace("https://docs.stripe.com/", "").replace(".md", "")
    slug = slug.replace("/", "_")
    return f"{slug}.md"


def download_docs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/markdown,text/plain,*/*",
        "Accept-Language": "en-US,en;q=0.9",
    }

    downloaded, failed = [], []

    for url in DOC_URLS:
        filename = slugify(url)
        filepath = os.path.join(OUTPUT_DIR, filename)

        try:
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()

            # Save with the source URL embedded at the top so we can cite it later
            content = f"Source: {url.replace('.md', '')}\n\n{resp.text}"
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

            downloaded.append(filename)
            print(f"[OK]   {filename}")

        except requests.exceptions.RequestException as e:
            failed.append((url, str(e)))
            print(f"[FAIL] {url} -> {e}")

        time.sleep(0.5)  # be polite to the server

    print(f"\nDone. Downloaded {len(downloaded)}/{len(DOC_URLS)} pages.")
    if failed:
        print("Failed URLs:")
        for url, err in failed:
            print(f"  - {url}: {err}")


if __name__ == "__main__":
    download_docs()
cat << 'EOF' > get_vendor_summary.py
import sqlite3
import pandas as pd
import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/get_vendor_summary.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def create_vendor_summary(conn):
    logging.info("Starting vendor summary extraction...")
    query = """
    WITH FreightSummary AS (
        SELECT 
            VendorNumber,
            SUM(Freight) AS FreightCost
        FROM vendor_invoice
        GROUP BY VendorNumber
    ),
    PurchaseSummary AS (
        SELECT
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description,
            p.PurchasePrice,
            pp.Price AS ActualPrice,
            pp.Volume,
            SUM(p.Qty) AS TotalPurchaseQuantity,
            SUM(p.Dollars) AS TotalPurchaseDollars
        FROM purchases p
        JOIN purchase_prices pp ON p.Brand = pp.Brand
        WHERE p.PurchasePrice > 0
        GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice
    ),
    SalesSummary AS (
        SELECT
            Brand,
            SUM(Qty) AS TotalSalesQuantity,
            SUM(SalesDollars) AS TotalSalesDollars,
            SUM(ExciseTax) AS TotalExciseTax
        FROM sales
        GROUP BY Brand
    )
    SELECT 
        ps.VendorNumber,
        ps.VendorName,
        ps.Brand,
        ps.Description,
        ps.PurchasePrice,
        ps.ActualPrice,
        ps.Volume,
        ps.TotalPurchaseQuantity,
        ps.TotalPurchaseDollars,
        COALESCE(ss.TotalSalesQuantity, 0) AS TotalSalesQuantity,
        ps.ActualPrice AS TotalSalesPrice,
        COALESCE(ss.TotalSalesDollars, 0) AS TotalSalesDollars,
        COALESCE(ss.TotalExciseTax, 0) AS TotalExciseTax,
        (ps.TotalPurchaseDollars + COALESCE(fs.FreightCost, 0)) AS FreightCost,
        (COALESCE(ss.TotalSalesDollars, 0) - ps.TotalPurchaseDollars) AS GrossProfit,
        CASE 
            WHEN COALESCE(ss.TotalSalesDollars, 0) = 0 THEN 0
            ELSE ((COALESCE(ss.TotalSalesDollars, 0) - ps.TotalPurchaseDollars) / COALESCE(ss.TotalSalesDollars, 0)) * 100
        END AS ProfitMargin
    FROM PurchaseSummary ps
    LEFT JOIN SalesSummary ss ON ps.Brand = ss.Brand
    LEFT JOIN FreightSummary fs ON ps.VendorNumber = fs.VendorNumber;
    """
    df = pd.read_sql_query(query, conn)
    return df

if _name_ == "_main_":
    conn = sqlite3.connect("inventory.db")
    vendor_sales_summary = create_vendor_summary(conn)
    vendor_sales_summary.to_sql('vendor_sales_summary', conn, if_exists='replace', index=False)
    
    with open("logs/get_vendor_summary.log", "a") as f:
        f.write("\n\n=== GENERATED DATA VIEW ===\n")
        f.write(vendor_sales_summary.head(10).to_string())
        
    print("Script ran successfully! Data loaded and text summary exported to logs folder.")
    conn.close()
EOF
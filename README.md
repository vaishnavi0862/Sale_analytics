# Sales Analytics Pipeline (Excel + SQL + Python + Tableau)

This project builds an end-to-end **sales analytics** workflow using:

- **Excel**: source data (customers, products, sales line items)
- **SQL**: star-schema warehouse + analytical queries
- **Python**: generate sample Excel data, load into **SQLite**, and export for visualization
- **Tableau**: create interactive dashboards from the exported dataset

## Project Structure

- `data/` — Excel source workbooks
- `database/` — SQLite warehouse (`sales.db`)
- `sql/` — schema + example analytical queries
- `scripts/` — Python pipeline scripts
- `exports/` — CSV export used for dashboards (`sales_fact_denormalized.csv`)
- `tableau/` — Tableau workbook and setup notes
- 
## 📊 Dashboard Preview

Here are the visualizations created in Tableau from the exported data:

### Monthly Revenue Trend
![Monthly Revenue Trend](images/revenue.png)

*Revenue shows seasonal patterns with peaks in mid-year months.*

### Sales by Product Category
![Sales by Category](images/sales_revenue.png)

*Electronics category leads revenue generation at approximately $350K.*

### Sales by Region
![Sales by Region](images/region.png)

*West and East regions contribute ~60% of total sales.*

### Complete Dashboard
![Dashboard Overview](images/dashboard.png)

**Key Business Insights:**
- Electronics is the top-performing category
- West region shows highest sales across all categories
- Revenue peaks in April-July period

## How the Data Flows

1. `scripts/01_generate_excel_data.py`
   - Generates sample Excel files in `data/`
2. `scripts/02_etl_sqlite.py`
   - Creates the warehouse tables from `sql/01_schema.sql`
   - Loads Excel into SQLite (`database/sales.db`)
   - Builds `dim_date` from the observed order date range
3. `scripts/03_export_for_powerbi.py`
   - Exports a denormalized CSV for dashboarding:
   - `exports/sales_fact_denormalized.csv`
4. Tableau
   - Connects to `exports/sales_fact_denormalized.csv`
   - Builds charts for revenue trend, category performance, region/segment breakdown, and top entities

## Run the Pipeline (Local)

```bash
cd /Users/vaishnavi/Desktop/sales_analysis
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_pipeline.py
```

After running, you should have:

- `database/sales.db`
- `exports/sales_fact_denormalized.csv`

## Tableau (Dashboard)

The recommended data source for Tableau is:

`exports/sales_fact_denormalized.csv`

See `tableau/SETUP.txt` for step-by-step instructions.

Your current workbook is saved at:

`tableau/Book1.twb`

## SQL Analytics Examples

Open the analytical queries in `sql/02_analytical_queries.sql` for:

- Revenue and gross margin by month
- Top products by revenue
- Sales by region and segment
- Customer ranking by lifetime value



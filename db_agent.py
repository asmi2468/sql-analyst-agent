import sqlite3
import os
import io
import base64
import matplotlib.pyplot as plt
import pandas as pd
from fastmcp import FastMCP

# This is the correct import for FastMCP 3.1.0 and Antigravity compatibility
from mcp.types import ImageContent as Image 

# 1. Initialize the MCP Server
mcp = FastMCP("Safe_SQL_Analyst") 

# 2. Path Configuration
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "data", "chinook.db")
DATA_DIR = os.path.join(BASE_DIR, "data")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)

# --- METADATA TOOLS ---

@mcp.tool()
def list_tables() -> str:
    """Lists all available tables in the music store database."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            return f"Tables in database: {', '.join(tables)}"
    except Exception as e:
        return f"Error identifying tables: {str(e)}"

@mcp.tool()
def get_schema(table_name: str) -> str:
    """Returns the column names and data types for a specific table."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            details = [f"{c[1]} ({c[2]})" for c in columns]
            return f"Table '{table_name}' structure: {', '.join(details)}"
    except Exception as e:
        return f"Error retrieving schema for {table_name}: {str(e)}"

# --- FILE DATA TOOLS (EXCEL & CSV) ---

@mcp.tool()
def read_csv(file_name: str) -> str:
    """Reads a CSV file from the 'data' directory."""
    try:
        path = os.path.join(DATA_DIR, file_name)
        df = pd.read_csv(path)
        return df.to_string(index=False) if not df.empty else "CSV is empty."
    except Exception as e:
        return f"❌ CSV Error: {str(e)}"

@mcp.tool()
def read_excel(file_name: str, sheet_name: str = None) -> str:
    """Reads data from an Excel file (.xlsx). Defaults to first sheet."""
    try:
        path = os.path.join(DATA_DIR, file_name)
        df = pd.read_excel(path, sheet_name=sheet_name if sheet_name else 0)
        return df.to_string(index=False) if not df.empty else "Sheet is empty."
    except Exception as e:
        return f"❌ Excel Error: {str(e)}"

# --- ANALYSIS & VISUALIZATION TOOLS ---

@mcp.tool()
def run_query(sql: str) -> str:
    """Executes a SQL query. SAFETY: Only SELECT allowed."""
    if not sql.strip().upper().startswith("SELECT"):
        return "❌ SAFETY ERROR: Only SELECT queries are allowed."

    try:
        with get_db_connection() as conn:
            df = pd.read_sql_query(sql, conn)
            return df.to_string(index=False) if not df.empty else "No data found."
    except Exception as e:
        return f"❌ SQL Error: {str(e)}"

@mcp.tool()
def create_chart_from_data(
    source_type: str, 
    source_name: str,
    title: str,
    sql_query: str = None, 
    sheet_name: str = None,
    chart_type: str = "bar", 
    threshold: float = None,
    high_color: str = "#4CAF50",
    mid_color: str = "#FFEB3B",
    low_color: str = "#F44336"
) -> Image:
    """Generates a chart with custom colors and data labels."""
    try:
        # 1. Fetch Data
        if source_type == "sql":
            with get_db_connection() as conn:
                df = pd.read_sql_query(sql_query, conn)
        elif source_type == "csv":
            df = pd.read_csv(os.path.join(DATA_DIR, source_name))
        elif source_type == "excel":
            df = pd.read_excel(os.path.join(DATA_DIR, source_name), sheet_name=sheet_name if sheet_name else 0)
        else:
            raise ValueError("Invalid source_type.")

        if df.empty: raise ValueError("No data found.")

        # 2. Setup Plot
        plt.figure(figsize=(12, 7))
        x_col, y_col = df.columns[0], df.columns[1]
        x_data = df[x_col].astype(str)
        y_data = df[y_col]

        # 3. Chart Logic with Data Labels
        if chart_type == "bar":
            colors = []
            if threshold:
                for val in y_data:
                    if val >= threshold: colors.append(high_color)
                    elif val >= (threshold * 0.6): colors.append(mid_color)
                    else: colors.append(low_color)
            else:
                colors = [high_color] * len(y_data)
            
            bars = plt.bar(x_data, y_data, color=colors)
            # Add labels to top of bars
            plt.bar_label(bars, padding=3, fmt='%.1f', fontweight='bold')
            if threshold:
                plt.axhline(y=threshold, color='black', linestyle='--', alpha=0.5, label=f'Target: {threshold}')
                plt.legend()

        elif chart_type == "line":
            plt.plot(x_data, y_data, marker='o', linewidth=2, color=high_color)
            # Annotate each point
            for i, val in enumerate(y_data):
                plt.annotate(f'{val:.1f}', (x_data[i], y_data[i]), textcoords="offset points", xytext=(0,10), ha='center')

        elif chart_type == "pie":
            plt.pie(y_data, labels=x_data, autopct='%1.1f%%', startangle=140, explode=[0.05]*len(y_data))

        plt.title(title, fontsize=16, fontweight='bold', pad=25)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        # 4. Save and Return
        safe_name = "".join(c if c.isalnum() or c in " -_" else "" for c in title).strip().replace(" ", "_").lower()
        plt.savefig(os.path.join(REPORTS_DIR, f"{safe_name}.png"), format="png", dpi=150)

        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=150)
        plt.close()
        
        img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        return Image(type="image", data=img_base64, mimeType="image/png")

    except Exception as e:
        return f"❌ Visualization Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
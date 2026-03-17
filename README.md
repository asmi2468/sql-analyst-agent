SQL Analyst: An Agentic AI Teammate
The SQL Analyst is a powerful Agentic AI built using the Model Context Protocol (MCP). It acts as a bridge between your LLM (like Claude or Antigravity) and your local data silos, allowing you to "chat" with SQL databases, CSV files, and Excel spreadsheets simultaneously.

🌟 Key Features
🛡️ Ironclad Safety: Custom logic strictly enforces SELECT-only queries, preventing any accidental data modification or deletion.

📂 Multi-Source Intelligence: Seamlessly joins data across SQLite (chinook.db), .csv, and .xlsx formats.

📊 Traffic-Light Visuals: Generates bar charts and line graphs with conditional coloring (Green/Yellow/Red) based on performance thresholds.

🏷️ Automated Labeling: Every chart includes bold data labels for instant readability without manual effort.
___________________________________________________________________________________________________________________________________________________________________________
🧱 Technical Stack
Language: Python 3.10+

Protocol: Model Context Protocol (MCP)

Framework: FastMCP

Environment: uv (Astral's lightning-fast package manager)

Libraries: Pandas, Matplotlib, Sqlite3, Openpyxl
_____________________________________________________________________________________________________________________________________________________________________________

🚀 Quick Start

1. Prerequisites
Ensure you have uv installed on your system.

2. Installation
Clone this repository and navigate to the folder:

PowerShell
git clone https://github.com/YOUR_USERNAME/sql-analyst-agent.git
cd sql-analyst-agent

3. Add Your Data
Place your data files in the /data directory:

chinook.db (SQLite)
sales_targets.csv
mailing_list.csv
company_performance.xlsx

4. Connect to an MCP Client (e.g., Antigravity)
Add the server to your MCP configuration file:

JSON
"mcpServers": {
  "sql-analyst": {
    "command": "uv",
    "args": [
      "run",
      "--path", "C:/Your/Path/To/Project",
      "db_agent.py"
    ]
  }
}

5. Run the Server
Run the server using uv:

PowerShell
uv run --path C:/Your/Path/To/Project db_agent.py

6. Interact with the Agent
You can now interact with the agent using any MCP client (e.g., Antigravity).

7. Generate Reports
The agent will automatically generate reports in the /reports directory.
___________________________________________________________________________________________________________________________________________________________

💡 Example Prompts to Try

"Compare the actual sales in SQL to the targets in my CSV file and show me a bar chart with a threshold of 500."

"Who are the top 5 customers in the database, and do they appear in my mailing_list.csv?"

"Generate a line chart for the revenue column in the Excel file."
___________________________________________________________________________________________________________________________________________________________

🛡️ Safety Warning

This agent is designed for read-only analysis. Any attempt to run DROP, DELETE, INSERT, or UPDATE commands will be blocked by the internal safety validator.







🚀 Project Case Study: The Agile Business Intelligence (BI) Pipeline

This portfolio project demonstrates a complete, end-to-end ELT (Extract, Load, Transform) data pipeline, built and managed using the Scrum framework.

The project ingests data from a live API, loads it into a cloud data lake (Azure Blob Storage), transforms the data using SQL (via DuckDB), and saves the clean, aggregated data to a processed-data container, where it's ready for visualization in Power BI.

Data Architecture & Flow

This diagram shows the complete ELT process, from the raw data source to the final dashboard.

🛠️ Tech Stack & Methodology

Methodology: Scrum

Project Management: Jira, Miro

Cloud / Data Lake: Azure Blob Storage

Data Ingestion: Python (requests)

Data Transformation: SQL, DuckDB

Helper Libraries: polars, pyarrow

Data Visualization: Power BI

▶️ How to Run This Project

Here is how you can run this pipeline on your local machine.

1. Prerequisites

Python 3.10+

An Azure account with Blob Storage

2. Installation

Clone this repository:

git clone https://github.com/datagirlab/Project-Case-Study-The-Agile-Business-Intelligence-BI-Pipeline.git
cd Project-Case-Study-The-Agile-Business-Intelligence-BI-Pipeline


Create a virtual environment (Recommended):

python -m venv venv


Activate it (Windows – PowerShell):

.\venv\Scripts\activate


Activate it (Mac/Linux – Bash):

source venv/bin/activate


Install all required libraries:

pip install -r requirements.txt

3. Set Up Your Environment Variable

This project uses an environment variable for the Azure Storage Account connection string.

PowerShell (Windows / VS Code):

$env:AZURE_STORAGE_CONNECTION_STRING="[your_full_connection_string_here]"


Git Bash / MacOS:

export AZURE_STORAGE_CONNECTION_STRING="[your_full_connection_string_here]"

4. Run the Pipeline

Run the Ingestion Script (E-L):
This script fetches data from the FakeStoreAPI and uploads the raw carts.json file into the raw-data container.

python ingest.py


Run the Transformation Script (T):
This script reads the raw JSON from Azure, runs the SQL transformation, and uploads the clean daily_sales_summary.csv file to the processed-data container.

python transform.py

5. View the Dashboard

You can now connect Power BI directly to the daily_sales_summary.csv file stored in your processed-data Azure container.

⚖️ License

This project is licensed under the MIT License.

This means you are free to use, copy, modify, and distribute this code for your own projects — as long as you include the original copyright notice
(credit to Celestine Agropah)
and the license text.

See the full text in the LICENSE file.

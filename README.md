# 🚀 Project Case Study: The Agile Business Intelligence (BI) Pipeline

This portfolio project demonstrates a complete, end-to-end ELT (Extract, Load, Transform) data pipeline, built and managed using the Scrum framework.

The project ingests data from a live API, loads it into a cloud data lake (Azure Blob Storage), transforms the data using SQL (via DuckDB), and saves the clean, aggregated data to a "processed" container, where it's ready for visualization in Power BI.

---

### **Data Architecture & Flow**

This diagram shows the complete ELT process, from the raw data source to the final dashboard.

![Data Flow Diagram](data-flow-diagram.png)
![BI - Data Flow Diagram](BI-data-flow-diagram.png)
---

### **🛠️ Tech Stack & Methodology**

* **Methodology:** Scrum
* **Project Management:** Jira, Miro
* **Cloud / Data Lake:** Azure Blob Storage
* **Data Ingestion:** Python (`requests`)
* **Data Transformation:** SQL, `DuckDB`
* **Helper Libraries:** `polars`, `pyarrow`
* **Data Visualization:** Power BI

---

### **▶️ How to Run This Project**

Here is how you can run this pipeline on your local machine.

#### **1. Prerequisites**
* Python 3.10+
* An Azure account with Blob Storage capabilities.

#### **2. Installation**
1.  **Clone (or download) this repository:**
    ```bash
    git clone [https://github.com/your-username/agile-bi-pipeline.git](https://github.com/your-username/agile-bi-pipeline.git)
    cd agile-bi-pipeline
    ```
2.  **Create a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `.\venv\Scripts\activate`
    ```
3.  **Install all required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

#### **3. Set Up Your Environment Variable**
This project requires a connection string to your Azure Storage Account. It is handled securely using environment variables and **is not** stored in the code.

**In your terminal**, set the following variable:

*(For PowerShell in VS Code)*
```powershell
$env:AZURE_STORAGE_CONNECTION_STRING="[your_full_connection_string_here]"

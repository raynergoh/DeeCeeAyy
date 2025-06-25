import pandas as pd
import requests
import logging
import io

def fetch_multpl_pe_table():
    url = "https://www.multpl.com/s-p-500-pe-ratio/table/by-month"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tables = pd.read_html(io.StringIO(response.text))
        pe_table = None
        for table in tables:
            if "Date" in table.columns and "Value" in table.columns:
                pe_table = table
                break
        if pe_table is not None:
            pe_table = pe_table[["Date", "Value"]]
            pe_table["Date"] = pd.to_datetime(pe_table["Date"])
            pe_table["Value"] = (
                pe_table["Value"]
                .astype(str)
                .str.replace(r"[^\d\.]", "", regex=True)
                .replace("", pd.NA)
                .astype(float)
            )
            pe_table = pe_table.dropna(subset=["Value"])
            pe_table.set_index("Date", inplace=True)
            pe_table.sort_index(inplace=True)
            pe_table.rename(columns={"Value": "PE_Ratio"}, inplace=True)
            return pe_table
        else:
            logging.error("PE ratio table not found in Multpl.com page.")
            return None
    else:
        logging.error(f"Failed to fetch Multpl.com page, status code: {response.status_code}")
        return None

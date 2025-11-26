import re
import pandas as pd
from utils.db_connector import DatabaseConnector

def extract_param(url, param):
    """Extrai o valor de um parâmetro da URL (ex: campaign_id, ad_creative_id)."""
    # match = re.search(rf"{param}=(\d+)", url)
    # return match.group(1) if match else None
    match = re.search(rf"{param}=([^&]+)", url)
    return match.group(1) if match else None

class PageviewsIngestor:
    def ingest(self, connector):
        rows = []
        with open("data/pageviews.txt") as f:
            for line in f:
                # timestamp entre colchetes
                timestamp = re.search(r"\[(.*?)\]", line).group(1)
                # primeira URL encontrada
                url = re.search(r'http[^\s]+', line).group(0)
                # device_id
                device_id = re.search(r'device_id:\s(\w+)', line).group(1)

                # parâmetros opcionais
                campaign_id = extract_param(url, "campaign_id")
                ad_creative_id = extract_param(url, "ad_creative_id")

                rows.append([device_id, campaign_id, ad_creative_id, url, timestamp])

        df = pd.DataFrame(rows, columns=["device_id","campaign_id","ad_creative_id","url","timestamp"])
        connector.write_table(df, "pageviews_raw")
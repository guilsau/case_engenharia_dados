import pandas as pd
import json
from utils.db_connector import DatabaseConnector

class GoogleAdsIngestor:
    def ingest(self, connector: DatabaseConnector):
        google_ads = [json.loads(line) for line in open("data/google_ads_media_costs.jsonl")]
        df = pd.DataFrame(google_ads)
        df.columns = ["date", "google_campaign_id", "google_campaign_name", "ad_creative_id", "ad_creative_name", "clicks", "impressions", "cost"]
        # Padronização de colunar para merge na transformacao
        df["campaign_id"] = df["google_campaign_id"].astype(str)
        connector.write_table(df, "google_ads_raw")

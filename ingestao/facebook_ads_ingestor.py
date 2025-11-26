import pandas as pd
import json
from utils.db_connector import DatabaseConnector


class FacebookAdsIngestor:
    def ingest(self, connector: DatabaseConnector):
        facebook_ads = [json.loads(line) for line in open("data/facebook_ads_media_costs.jsonl")]
        df = pd.DataFrame(facebook_ads)
        df.columns = ["date", "facebook_campaign_id", "facebook_campaign_name", "clicks", "impressions", "cost"]
        df["ad_creative_id"] = None
        # Padronização de colunar para merge na transformacao
        df["campaign_id"] = df["facebook_campaign_id"].astype(str)
        connector.write_table(df, "facebook_ads_raw")

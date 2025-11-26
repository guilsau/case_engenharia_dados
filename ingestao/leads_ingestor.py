import pandas as pd
from utils.db_connector import DatabaseConnector

class LeadsIngestor:
    def ingest(self, connector: DatabaseConnector):
        df = pd.read_csv("data/customer_leads_funnel.csv", header=None)
        df.columns = ["device_id","lead_id","registered_at","credit_decision","credit_decision_at","signed_at","revenue"]
        connector.write_table(df, "customer_leads_raw")

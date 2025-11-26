import pandas as pd
from utils.db_connector import DatabaseConnector

class MarketingTransformer:
    def transform(self, connector: DatabaseConnector):
        # Ler tabelas
        google_df = connector.read_table("google_ads_raw")
        facebook_df = connector.read_table("facebook_ads_raw")
        pageviews_df = connector.read_table("pageviews_raw")
        leads_df = connector.read_table("customer_leads_raw")

        # Regras de negócio
        leads_df["is_customer"] = (leads_df["credit_decision"] == "A") & (leads_df["signed_at"].notnull())
        leads_df["revenue"] = leads_df.apply(
            lambda row: row["revenue"] if row["is_customer"] else 0, axis=1
        )

        # Normalizar Google Ads
        google_df = google_df.drop(columns=["campaign_id"]).rename(columns={
            "google_campaign_id": "campaign_id",
            "google_campaign_name": "campaign_name"
        })[["date", "campaign_id", "campaign_name", "ad_creative_id", "clicks", "impressions", "cost"]]
        google_df["source"] = "google"

        # Normalizar Facebook Ads
        facebook_df = facebook_df.drop(columns=["campaign_id"]).rename(columns={
            "facebook_campaign_id": "campaign_id",
            "facebook_campaign_name": "campaign_name"
        })[["date", "campaign_id", "campaign_name", "ad_creative_id", "clicks", "impressions", "cost"]]
        facebook_df["source"] = "facebook"

        # Concatenar com estrutura igual
        ads_df = pd.concat([google_df, facebook_df], ignore_index=True)
        ads_df["campaign_id"] = ads_df["campaign_id"].astype(str)
        pageviews_df["campaign_id"] = pageviews_df["campaign_id"].astype(str)

        print("Ads DF sample:", ads_df.head())

        # Filtrar pageviews que têm campaign_id presente em ads_df
        pageviews_df = pageviews_df.rename(columns={"device_id": "pv_device_id"})
        pageviews_matched = pageviews_df[pageviews_df["campaign_id"].isin(ads_df["campaign_id"])]

        print("Pageviews que casam:", pageviews_matched.head())

        # Juntar Ads + Pageviews
        ads_pageviews = ads_df.merge(pageviews_matched, on="campaign_id", how="inner")

        print("Ads+Pageviews sample:", ads_pageviews.head())

        # Filtrar leads que têm device_id presente em pageviews
        leads_matched = leads_df[leads_df["device_id"].isin(pageviews_matched["pv_device_id"])]

        print("Leads que casam:", leads_matched.head())

        # Juntar Ads+Pageviews + Leads
        final_df = ads_pageviews.merge(leads_matched, left_on="pv_device_id", right_on="device_id", how="inner")

        print("Final DF shape:", final_df.shape)
        print("Final DF sample:", final_df.head())

        # Calcular lucro
        final_df["profit"] = final_df["revenue"] - final_df["cost"]

        # Escrever no banco
        connector.write_table(final_df, "marketing_analytics")
        print("Tabela 'marketing_analytics' criada com sucesso!")
        connector.engine.dispose()

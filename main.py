from utils.db_connector import DatabaseConnector
from ingestao.google_ads_ingestor import GoogleAdsIngestor
from ingestao.facebook_ads_ingestor import FacebookAdsIngestor
from ingestao.pageviews_ingestor import PageviewsIngestor
from ingestao.leads_ingestor import LeadsIngestor
from transformacao.marketing_transformer import MarketingTransformer

def run_pipeline():
    connector = DatabaseConnector()

    # Ingestão
    GoogleAdsIngestor().ingest(connector)
    FacebookAdsIngestor().ingest(connector)
    PageviewsIngestor().ingest(connector)
    LeadsIngestor().ingest(connector)

    # Transformação
    MarketingTransformer().transform(connector)


if __name__ == "__main__":
    run_pipeline()
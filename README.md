# 📊 Marketing Analytics Case

Este projeto resolve o case de dados de marketing digital.  
O objetivo é preparar uma base analítica única que permita ao time de marketing responder perguntas de negócio de forma simples e direta.

---

## 🚀 Objetivos
1. **Ingestão dos dados** em um banco SQLite.  
2. **Criação da tabela única `marketing_analytics`** consolidando informações de campanhas, anúncios, pageviews e leads.  


3. **Disponibilização de queries SQL** para responder às principais perguntas de negócio:  
   - Qual foi a campanha mais cara?  
   - Qual foi a campanha mais lucrativa?  
   - Qual criativo foi mais efetivo em termos de cliques?  
   - Qual criativo foi mais efetivo em termos de geração de leads?  


4. **Documentação de como reproduzir a solução**.

---

## 🛠️ Estrutura do Projeto
- `utils/db_connector.py` → Classe para conectar ao SQLite. 
- `ingestao/facebook_ads_ingestor.py` → Classe para ingerir dados do facebook ads mo SQLite. 
- `ingestao/leads_ingestor.py` →  Classe para ingerir dados do leads mo SQLite.
- `ingestao/google_ads_ingestor.py` →  Classe para ingerir dados do google ads ads mo SQLite 
- `ingestao/pageviews_ingestor.py` →  Classe para ingerir dados do pageviews ads mo SQLite
- `transformers/marketing_transformer.py` → Classe que transforma os dados brutos e gera a tabela final.  
- `main.py` → Script principal que executa a transformação e grava no banco.  
- `data/marketing.db` → Banco SQLite gerado com a tabela `marketing_analytics`.  

---

## 🗄️ Tabela Final: `marketing_analytics`
Colunas principais:
- `date` → Data da campanha  
- `campaign_id`, `campaign_name`, `source` → Identificação da campanha e origem (Google/Facebook)  
- `ad_creative_id` → Identificação do criativo do anúncio  
- `clicks`, `impressions`, `cost` → Métricas de performance  
- `pv_device_id`, `url`, `timestamp` → Pageviews associados  
- `lead_id`, `registered_at`, `signed_at`, `is_customer`, `revenue` → Leads e conversões  
- `profit` → Receita - custo  

---



## 🔄 Como Reproduzir

1. **Clonar o repositório**
   ```bash
   git clone https://github.com/seu-usuario/case_engenharia_dados.git
   cd case_engenharia_dados

2. **Subir o ambiente Docker**
   docker build -t marketing_case .
   docker run -v $(pwd)/data:/app/data marketing_case

3. **Executar o script principal**
   python main.py

4. **Executar o script principal**

## 📈 Queries de Negócio
### 1. Campanha mais cara
```sql
SELECT campaign_id, campaign_name, SUM(cost) AS total_cost
FROM marketing_analytics
GROUP BY campaign_id, campaign_name
ORDER BY total_cost DESC
LIMIT 1;
```

### 2. Campanha mais lucrativa
```sql
SELECT campaign_id, campaign_name, SUM(profit) AS total_profit
FROM marketing_analytics
GROUP BY campaign_id, campaign_name
ORDER BY total_profit DESC
LIMIT 1;
```

### 3. Criativo mais efetivo em termos de cliques
```sql
SELECT ad_creative_id, SUM(clicks) AS total_clicks
FROM marketing_analytics
GROUP BY ad_creative_id
ORDER BY total_clicks DESC
LIMIT 1;
```

### 4. Criativo mais efetivo em termos de geração de leads
```sql
SELECT ad_creative_id, COUNT(DISTINCT lead_id) AS total_leads
FROM marketing_analytics
WHERE lead_id IS NOT NULL
GROUP BY ad_creative_id
ORDER BY total_leads DESC
LIMIT 1;

```

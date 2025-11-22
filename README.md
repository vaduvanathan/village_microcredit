# Village Microcredit Risk Atlas

A data-driven micro-lending risk scoring platform for Tamil Nadu, visualizing social security scheme penetration and agricultural risks.

## Features
- **District Risk Map**: Interactive choropleth map showing district-wise performance rankings.
- **Scheme Analysis**: Dynamic inputs for schemes like Magalir Urimai, Old Age Pension, MGNREGA, and Pongal Gift.
- **AI Risk Assessment**: Automated risk explanation based on resilience scores.
- **Visualizations**: PyDeck hexagon maps and Altair charts for data distribution.

## Local Development

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the App**:
   ```bash
   streamlit run app.py
   ```

## Deployment on Google Cloud

### Option 1: Cloud Run (Recommended)

This project includes a `Dockerfile` and `cloudbuild.yaml` for easy deployment to Google Cloud Run.

1. **Open Google Cloud Shell** in your browser.
2. **Clone this repository**:
   ```bash
   git clone https://github.com/vaduvanathan/village_microcredit.git
   cd village_microcredit
   ```
3. **Submit the build**:
   ```bash
   gcloud builds submit --config cloudbuild.yaml .
   ```
   *Note: Ensure Cloud Build and Cloud Run APIs are enabled in your project.*

### Option 2: Manual Deployment

1. **Build the image**:
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/village-microcredit
   ```
2. **Deploy to Cloud Run**:
   ```bash
   gcloud run deploy village-microcredit --image gcr.io/YOUR_PROJECT_ID/village-microcredit --platform managed
   ```

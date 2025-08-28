# App for reading book with interactive content.
## roman-v-otkrytkah.com

## Stack & third-party services
Django 5, Gunicorn  
Local dev runs via Docker Compose + Nginx  
Production runs on Google Cloud Run.  
Images for Cloud Run with Artifact Registry  
Data in Cloud SQL (PostgreSQL)  
Media in Google Cloud Storage  
Static with Whitenoise.  
PWA (service worker + manifest) is included.  
Google Map API for map  
Domain mapped to the Cloud Run service  

## local run:
### USE_POSTGRES=0
### docker compose up --build

## prod
### USE_POSTGRES=1

### set up
export PROJECT_ID=<..>  
export REGION=<..>  
export SERVICE=<..>  
export INSTANCE=<..>  
gcloud config set project "$PROJECT_ID"

### sql connection name:
export ICN=$(gcloud sql instances describe "$INSTANCE" --format='value(connectionName)')


### deploy:
gcloud run deploy "$SERVICE" \  
  --region "$REGION" \  
  --source "$(pwd)" \  
  --add-cloudsql-instances="$ICN" \  
  --update-env-vars=DEBUG=0,USE_POSTGRES=1,DB_NAME=<..>,DB_USER=<..>,DB_PASS='<..>',INSTANCE_CONNECTION_NAME="$ICN",GCS_BUCKET_NAME=<..>,  SECRET_KEY='<secret>',GUNICORN_CMD_ARGS="--access-logfile - --error-logfile -" \  
  --allow-unauthenticated  


### cloud run job:

#### current deployed image (for migration)
IMAGE=$(gcloud run services describe "$SERVICE" --region "$REGION" \  
  --format='value(spec.template.spec.containers[0].image)')  

SA=$(gcloud run services describe "$SERVICE" --region "$REGION" \  
  --format='value(spec.template.spec.serviceAccountName)')  

#### create or update:
if gcloud run jobs describe "${SERVICE}-migrate" --region "$REGION" >/dev/null 2>&1; then  
  gcloud run jobs update "${SERVICE}-migrate" \  
    --region "$REGION" \  
    --image "$IMAGE" \  
    --service-account "$SA" \  
    --set-cloudsql-instances="$ICN" \  
    --set-env-vars=DEBUG=0,USE_POSTGRES=1,DB_NAME=<..>,DB_USER=<..>,DB_PASS='<..>',INSTANCE_CONNECTION_NAME="$ICN",GCS_BUCKET_NAME=<..>,  SECRET_KEY='<secret>' \  
    --command python --args manage.py,migrate  
else  
  gcloud run jobs create "${SERVICE}-migrate" \  
    --region "$REGION" \  
    --image "$IMAGE" \  
    --service-account "$SA" \  
    --set-cloudsql-instances="$ICN" \  
    --set-env-vars=DEBUG=0,USE_POSTGRES=1,DB_NAME=<..>,DB_USER=<..>,DB_PASS='<..>',INSTANCE_CONNECTION_NAME="$ICN",GCS_BUCKET_NAME=<..>,  SECRET_KEY='<secret>' \  
    --command python --args manage.py,migrate  
fi  

### start migration
gcloud run jobs execute "${SERVICE}-migrate" --region "$REGION"


## local logs:
docker compose logs web --tail 200 -f

## live logs:
gcloud logging tail \  
 'resource.type="cloud_run_revision" AND resource.labels.service_name="'"$SERVICE"'"' \  
 --project "$PROJECT_ID"  

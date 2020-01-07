PROJECT_ID:=data-science-italy
SERVICE_NAME:=testservice

build:
	gcloud builds submit --timeout 1200 --tag gcr.io/$(PROJECT_ID)/face_microservice

deploy:
	gcloud beta run deploy $(SERVICE_NAME) --image gcr.io/$(PROJECT_ID)/face_microservice --platform managed --memory 2Gi --region europe-west1

all: build deploy

delete:
	gcloud beta run services delete $(SERVICE_NAME)
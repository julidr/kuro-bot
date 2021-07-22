#!/bin/bash

echo "Creating Kuro Bot Logging Configs"
docker config create kuro-bot-logs $KURO_PATH_DATA/kuro-logging.conf

echo "Creating Kuro Bot Secrets"
docker secret create kuro-bot-secret $KURO_PATH_DATA/kuro-settings.json

echo "Building Kuro Bot Image"
cd $KURO_PATH
docker build --tag kuro-bot:latest .

echo "Starting Kuro Bot Service"
docker service create \
--name kuro-bot \
--secret kuro-bot-secret \
--config source=kuro-bot-logs,target=/etc/kuro-bot/kuro-logging.conf,mode=0775 \
--env SETTINGS_PATH=/run/secrets/kuro-bot-secret \
--env LOGGING_PATH=/etc/kuro-bot/kuro-logging.conf \
--mount type=bind,source=$KURO_PATH_DATA/data,destination=/kuro-bot/data \
kuro-bot:latest
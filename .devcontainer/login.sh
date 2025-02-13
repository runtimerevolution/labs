#!/usr/bin/env bash

source .env.local

# Check if infisical credentials are present in the env
if [ -z "$INFISICAL_CLIENT_ID" ] || [ -z "$INFISICAL_CLIENT_SECRET" ]; then
  echo "Infisical credentials not set in environment variables."
  exit 1
fi

# Login to infisical
export INFISICAL_TOKEN=$(infisical login --domain=$INFISICAL_DOMAIN --method=universal-auth --client-id=$INFISICAL_CLIENT_ID --client-secret=$INFISICAL_CLIENT_SECRET --silent --plain)

# Export secrets to zsh
infisical secrets --domain=$INFISICAL_DOMAIN --projectId=$INFISICAL_PROJECT_ID --env=dev --plain | while IFS= read -r line; do echo "export $line" >> $HOME/.zshrc; done

#!/usr/bin/env bash

set -e

source <(grep -v '^#' "./.env.user-gen" | sed -E 's|^(.+)=(.*)$|: ${\1=\2}; export \1|g')

user_count=$1

FXRP_SYMBOL=FXRP
if [ $CHAIN == 'coston' -o $CHAIN == 'coston2' ]; then
    FXRP_SYMBOL=FTestXRP
fi

safe_json_update() {
    tmp="$(mktemp "$(dirname "$2")/config.XXXXXX.json")"
    if ! jq "$1" "$2" > "$tmp"; then
        echo "jq failed updating $2." >&2
        rm -f "$tmp"
        return 1
    fi
    mv "$tmp" "$2"
}

config_json_path() {
    echo fasset-bots-config/users/user$1/config.json
}

secrets_json_path() {
    echo fasset-bots-config/users/user$1/secrets.json
}

update_config_json() {
    safe_json_update "$1" $(config_json_path $2)
}

update_secrets_json() {
    safe_json_update "$1" $(secrets_json_path $2)
}

write_configs() {

    # create if not exists
    path=$(config_json_path $1)
    if [ ! -e $path ]; then
        echo "{}" | jq > $path
    fi

    # write chain config
    update_config_json ".extends = \"$CHAIN-bot-postgresql.json\"" $1

    # write database config
    db_name=fasset-load-test-user-$1
    update_config_json ".
        | (.ormOptions.type = \"postgresql\")
        | (.ormOptions.host = \"$DB_HOST\")
        | (.ormOptions.dbName = \"$db_name\")
        | (.ormOptions.port = $DB_PORT)" $1

    # write database secrets
    update_secrets_json ".
        | (.database.user = \"$DB_USER\")
        | (.database.password = \"$DB_PASS\")" $1

    # write native rpc config
    update_config_json ".rpcUrl = \"$RPC_URL\"" $1
    update_secrets_json ".apiKey.native_rpc = \"$RPC_API_KEY\"" $1

    # write xrp rpc config
    update_config_json ".fAssets.$FXRP_SYMBOL.walletUrls = [\"${XRP_RPC_URL}\"]" $1
    sym=$([ $CHAIN == 'flare' -o $CHAIN == 'songbird' ] && echo XRP || echo testXRP)
    update_secrets_json ".apiKey.${sym}_rpc = [\"$XRP_RPC_API_KEY\"]" $1

    # write dal api urls and api keys

    dal_urls=()
    if [ -n "$DAL_URLS" ]; then
        IFS=',' read -r -a dal_urls <<< "$DAL_URLS"
    fi

    dal_api_keys=()
    if [ -n "$DAL_API_KEYS" ]; then
        IFS=',' read -r -a dal_api_keys <<< "$DAL_API_KEYS"
    fi

    if [ "${#dal_urls[@]}" -ne "${#dal_api_keys[@]}" ]; then
        echo "error: .env variables 'DAL_URLS' and 'DAL_API_KEYS' require equal lengths."
        exit 1
    fi

    if [ "${#dal_urls[@]}" -gt 0 ]; then
        urls=$(printf '%s\n' "${dal_urls[@]}" | jq -R . | jq -s .)
        update_config_json ".dataAccessLayerUrls = $urls" $1
    else
        echo "error: .env variable 'DAL_URLS' requires at least one value."
        exit 1
    fi

    if [ "${#dal_api_keys[@]}" -gt 0 ]; then
        keys=$(printf '%s\n' "${dal_api_keys[@]}" | jq -R . | jq -s .)
        update_secrets_json ".apiKey.data_access_layer = $keys" $1
    else
        echo "error: .env variable 'DAL_API_KEYS' requires at least one value."
    fi

    # indexer urls and api keys

    xrp_indexer_urls=()
    if [ -n "$XRP_INDEXER_URLS" ]; then
        IFS=',' read -r -a xrp_indexer_urls <<< "$XRP_INDEXER_URLS"
    fi

    xrp_indexer_api_keys=()
    if [ -n "$XRP_INDEXER_API_KEYS" ]; then
        IFS=',' read -r -a xrp_indexer_api_keys <<< "$XRP_INDEXER_API_KEYS"
    fi

    if [ "${#xrp_indexer_urls[@]}" -ne "${#xrp_indexer_api_keys[@]}" ]; then
        echo "error: .env variables 'XRP_INDEXER_URLS' and 'XRP_INDEXER_API_KEYS' require equal lengths."
        exit 1
    fi

    if [ "${#xrp_indexer_urls[@]}" -gt 0 ]; then
        urls=$(printf '%s\n' "${xrp_indexer_urls[@]}" | jq -R . | jq -s .)
        update_config_json ".fAssets.$FXRP_SYMBOL.indexerUrls = $urls" $1
    else
        echo "error: .env variable 'XRP_INDEXER_URLS' requires at least one value."
        exit 1
    fi

    if [ "${#xrp_indexer_api_keys[@]}" -gt 0 ]; then
        keys=$(printf '%s\n' "${xrp_indexer_api_keys[@]}" | jq -R . | jq -s .)
        update_secrets_json ".apiKey.indexer = $keys" $1
    else
        echo "error: .env variable 'XRP_INDEXER_API_KEYS' requires at least one value."
        exit 1
    fi
}

for i in $(seq 0 "$user_count"); do
    node fasset-bots/packages/fasset-bots-cli/dist/src/cli/key-gen.js generateSecrets -o $(secrets_json_path $i) --user > /dev/null >&1
    write_configs $i
    echo "generated secrets and config for user $i"
done

mkdir -p ~/.streamlit/

cat <<EOL > ~/.streamlit/credentials.toml
[general]
email = "emeline.tapin@gmail.com"
EOL

cat <<EOL > ~/.streamlit/config.toml
[server]
headless = true
enableCORS = false
port = $PORT
EOL

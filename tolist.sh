tee -a ~/.bashrc <<'EOF'

# tolist: convert args to a comma-separated bracketed list
# usage: tolist foo bar "baz qux"  -> [foo, bar, baz qux]
tolist() {
  local input="$*"
  # Collassa spazi/tab multipli e separa con ", "
  echo "[$(echo "$input" | tr '\t' ' ' | sed 's/[[:space:]]\+/, /g')]"
}
EOF

# ricarica
. ~/.bashrc

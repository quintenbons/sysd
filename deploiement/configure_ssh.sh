# Configuration locale (~/.ssh/config)
# Permet la connexion à Grid5000 sans mot de passe, et la redirection rapide ssh grenoble.g5k -> grenoble
if [ -z "$1" ]; then
    echo "Usage: ./setup_all.sh <g5k-user>"
    exit 1
fi
G5K_USER=$1

SSH_CONFIG="$HOME/.ssh/config"
ENTRY1="Host g5k\n  User $G5K_USER\n  Hostname access.grid5000.fr\n  ForwardAgent no\n"
ENTRY2="Host *.g5k\n  User $G5K_USER\n  ProxyCommand ssh g5k -W \"\$(basename %h .g5k):%p\"\n  ForwardAgent no\n"

if grep -q "^Host g5k$" "$SSH_CONFIG"; then
    echo "Le fichier de configuration ssh contient déjà l'entrée 'Host g5k'"
    exit 0
fi

check_and_append() {
    echo "$1" >> "$2"
}

if [ ! -f "$SSH_CONFIG" ]; then
    echo "Création du fichier de configuration ssh"
    touch "$SSH_CONFIG"
fi

check_and_append "$ENTRY1" "$SSH_CONFIG"
check_and_append "$ENTRY2" "$SSH_CONFIG"

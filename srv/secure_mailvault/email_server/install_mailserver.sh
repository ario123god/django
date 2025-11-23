#!/usr/bin/env bash
set -euo pipefail

# Idempotent mail server installer for Postfix + Dovecot with TLS and fail2ban
# Defaults can be overridden via environment variables before running the script.

DOMAIN=${MAIL_DOMAIN:-example.com}
MAIL_USER=${MAIL_USER:-user}
MAIL_PASS=${MAIL_PASS:-ChangeMe123!}
CERTBOT_EMAIL=${CERTBOT_EMAIL:-admin@${DOMAIN}}
LE_DIR="/etc/letsencrypt/live/${DOMAIN}"
SELF_SIGNED_DIR="/etc/ssl/${DOMAIN}"
MAILNAME_FILE=/etc/mailname

export DEBIAN_FRONTEND=noninteractive

log() {
  echo "[secure_mailvault] $1"
}

install_packages() {
  log "Installing Postfix, Dovecot, Certbot, fail2ban, and utilities"
  apt-get update -y
  apt-get install -y postfix postfix-sqlite dovecot-core dovecot-imapd dovecot-pop3d dovecot-sqlite mailutils \
    certbot ufw sqlite3 fail2ban pwgen
}

configure_mailname() {
  log "Setting mailname to ${DOMAIN}"
  echo "${DOMAIN}" > "${MAILNAME_FILE}"
}

obtain_certificates() {
  mkdir -p "${SELF_SIGNED_DIR}"
  if [ -f "${LE_DIR}/fullchain.pem" ] && [ -f "${LE_DIR}/privkey.pem" ]; then
    log "Existing Let's Encrypt certificate found for ${DOMAIN}"
    return
  fi

  log "Requesting Let's Encrypt certificate for ${DOMAIN} (standalone mode)"
  if certbot certonly --standalone --non-interactive --agree-tos -d "${DOMAIN}" \
    --email "${CERTBOT_EMAIL}" --preferred-challenges http; then
    log "Certificate issued by Let's Encrypt for ${DOMAIN}"
  else
    log "Let's Encrypt failed or domain not reachable; generating self-signed certificate"
    openssl req -x509 -nodes -newkey rsa:4096 -days 365 -keyout "${SELF_SIGNED_DIR}/privkey.pem" \
      -out "${SELF_SIGNED_DIR}/fullchain.pem" -subj "/CN=${DOMAIN}"
    ln -sf "${SELF_SIGNED_DIR}" "${LE_DIR%/*}" 2>/dev/null || true
    mkdir -p "${LE_DIR}"
    ln -sf "${SELF_SIGNED_DIR}/fullchain.pem" "${LE_DIR}/fullchain.pem"
    ln -sf "${SELF_SIGNED_DIR}/privkey.pem" "${LE_DIR}/privkey.pem"
  fi
}

configure_postfix() {
  log "Configuring Postfix for ${DOMAIN}"
  mkdir -p /etc/postfix/master.d
  postconf -e "myhostname = ${DOMAIN}"
  postconf -e "myorigin = /etc/mailname"
  postconf -e "mydestination = localhost"
  postconf -e "home_mailbox = Maildir/"
  postconf -e "smtpd_tls_cert_file = ${LE_DIR}/fullchain.pem"
  postconf -e "smtpd_tls_key_file = ${LE_DIR}/privkey.pem"
  postconf -e "smtpd_use_tls = yes"
  postconf -e "smtpd_tls_auth_only = yes"
  postconf -e "smtpd_sasl_type = dovecot"
  postconf -e "smtpd_sasl_path = private/auth"
  postconf -e "smtpd_sasl_auth_enable = yes"
  postconf -e "smtpd_sasl_security_options = noanonymous"
  postconf -e "smtpd_recipient_restrictions = permit_sasl_authenticated,permit_mynetworks,reject_unauth_destination"
  postconf -e "inet_interfaces = all"
  postconf -e "inet_protocols = all"
  postconf -e "mynetworks = 127.0.0.0/8"
  postconf -e "smtp_tls_security_level = may"
  postconf -e "smtpd_tls_security_level = may"
  postconf -e "master_service_disable = "

  # Configure submission (587) and smtps (465)
  sed -i '/^submission/ s/^/#/' /etc/postfix/master.cf
  sed -i '/^smtps/ s/^/#/' /etc/postfix/master.cf

  cat <<'POSTFIX_MASTER' > /etc/postfix/master.d/secure_mailvault.conf
submission inet n       -       y       -       -       smtpd
  -o syslog_name=postfix/submission
  -o smtpd_tls_security_level=encrypt
  -o smtpd_sasl_auth_enable=yes
  -o smtpd_reject_unlisted_recipient=no
  -o smtpd_client_restrictions=permit_sasl_authenticated,reject
  -o smtpd_helo_restrictions=
  -o smtpd_sender_restrictions=
  -o smtpd_recipient_restrictions=
  -o smtpd_relay_restrictions=permit_sasl_authenticated,reject
smtps     inet n       -       y       -       -       smtpd
  -o syslog_name=postfix/smtps
  -o smtpd_tls_wrappermode=yes
  -o smtpd_sasl_auth_enable=yes
  -o smtpd_reject_unlisted_recipient=no
  -o smtpd_client_restrictions=permit_sasl_authenticated,reject
  -o smtpd_helo_restrictions=
  -o smtpd_sender_restrictions=
  -o smtpd_recipient_restrictions=
  -o smtpd_relay_restrictions=permit_sasl_authenticated,reject
POSTFIX_MASTER
}

configure_dovecot() {
  log "Configuring Dovecot"
  mkdir -p /etc/dovecot/conf.d
  cat <<EOF_CONF > /etc/dovecot/local.conf
disable_plaintext_auth = yes
mail_location = maildir:~/Maildir
ssl = required
ssl_cert = <${LE_DIR}/fullchain.pem
ssl_key = <${LE_DIR}/privkey.pem
auth_mechanisms = plain login
passdb {
  driver = pam
}
userdb {
  driver = passwd
}
protocols = imap pop3 lmtp
service auth {
  unix_listener /var/spool/postfix/private/auth {
    mode = 0660
    user = postfix
    group = postfix
  }
}
EOF_CONF

  if ! grep -q 'local.conf' /etc/dovecot/dovecot.conf 2>/dev/null; then
    echo '!include_try local.conf' >> /etc/dovecot/dovecot.conf
  fi
}

configure_fail2ban() {
  log "Configuring fail2ban for Postfix and Dovecot"
  cat <<'F2B' > /etc/fail2ban/jail.d/secure_mailvault.local
[postfix]
enabled = true
port    = smtp,ssmtp,submission
logpath = /var/log/mail.log

[dovecot]
enabled = true
port    = pop3,pop3s,imap,imaps,submission,465,smtp
logpath = /var/log/mail.log
F2B
}

create_mail_user() {
  local user=${MAIL_USER}
  local password=${MAIL_PASS}

  if id "${user}" >/dev/null 2>&1; then
    log "Mail user ${user} already exists"
  else
    log "Creating mail user ${user}"
    useradd -m -s /usr/sbin/nologin "${user}"
  fi

  echo "${user}:${password}" | chpasswd
  sudo -u "${user}" mkdir -p "/home/${user}/Maildir"
  sudo -u "${user}" maildirmake.dovecot "/home/${user}/Maildir" 2>/dev/null || true
  sudo -u "${user}" maildirmake.dovecot "/home/${user}/Maildir/.Drafts" 2>/dev/null || true
  sudo -u "${user}" maildirmake.dovecot "/home/${user}/Maildir/.Sent" 2>/dev/null || true
  sudo -u "${user}" maildirmake.dovecot "/home/${user}/Maildir/.Trash" 2>/dev/null || true
  chown -R "${user}:${user}" "/home/${user}/Maildir"
}

configure_firewall() {
  log "Opening mail ports via ufw"
  ufw allow 25/tcp || true
  ufw allow 465/tcp || true
  ufw allow 587/tcp || true
  ufw allow 993/tcp || true
  ufw --force enable || true
}

restart_services() {
  log "Enabling and restarting services"
  systemctl daemon-reload || true
  systemctl enable postfix dovecot fail2ban
  systemctl restart postfix dovecot fail2ban
}

main() {
  install_packages
  configure_mailname
  obtain_certificates
  configure_postfix
  configure_dovecot
  configure_fail2ban
  create_mail_user
  configure_firewall
  restart_services
  log "Mail server setup complete. Account: ${MAIL_USER}@${DOMAIN}"
}

main "$@"

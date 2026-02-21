---
tags:
  - dod
  - dns-firewall
  - dns-firewall/dns
---

# DNS – grundlæggende

> **Dybere end dagens teori:** Records, TTL, propagation og fejlsøgning. Dag-note: [[../Noter/DoD - Pensum/Dag-02-Domæne-DNS-og-Firewall]]. Cloudflare: [[DNS-Cloudflare]].

---

## Hvad er DNS?

**DNS** (Domain Name System) oversætter domænenavne til IP-adresser og andre oplysninger. Når nogen skriver `https://minside.dk`, spørger browseren DNS: "Hvilken IP har minside.dk?" – og får fx `192.0.2.42` tilbage. DNS svarer på *Hvor findes denne server?* og *Hvilken server håndterer e-mail?* osv.

DNS er bygget op af **records** (poster) i en **zone** for dit domæne. Hver record har en **type**, et **navn** (host), en **værdi** og ofte en **TTL** (Time To Live).

---

## DNS-records – oversigt

| Record type | Formål | Eksempel |
|-------------|--------|----------|
| **A** | Peger et **hostnavn** direkte til en **IPv4-adresse**. | `app` → `192.0.2.42` |
| **AAAA** | Som A, men til **IPv6**. | `app` → `2001:db8::1` |
| **CNAME** | Peger et **navn** videre til et **andet domænenavn** (alias). Kan ikke bruges på root (apex) af zonen. | `www` → `app.mercantec.tech` |
| **MX** | Angiver **mail-servere** for domænet (prioritet + host). | `10 mail.provider.com` |
| **TXT** | Frit tekstfelt. Verifikation, SPF/DKIM, andre oplysninger. | `v=spf1 include:_spf.google.com ~all` |
| **NS** | Angiver **nameservere** for (sub)domænet. Bruges ved delegation eller når du flytter DNS. | `ns1.cloudflare.com` |
| **CAA** | Angiver hvilke **certificate authorities** der må udstede certifikater. | `0 issue "letsencrypt.org"` |

I Cloudflare angiver du **navn** som subdomain (fx `app` for `app.mercantec.tech`) eller `@` for root (`mercantec.tech`).

---

## A og CNAME til deployment

- **Root-domæne** (fx `mercantec.tech`): Brug et **A-record** med navn `@` der peger på din servers offentlige IP.
- **Subdomain** (fx `jeresprojekt.mercantec.tech`): Opret **A-record** med navn `jeresprojekt` og IP = jeres server – eller **CNAME** der peger på et andet host der allerede har A-record (så I kun opdaterer IP ét sted).

**CNAME på root:** Mange DNS-leverandører tillader ikke CNAME på apex; brug A (eller "ALIAS"/"ANAME" hvor understøttet).

---

## TTL og propagation

- **TTL** (Time To Live): Hvor længe svar må caches (i sekunder). Lav TTL (fx 300) = hurtigere opdatering ved ændring, men flere DNS-forespørgsler. Høj TTL = mindre load, men ændringer spredes langsommere.
- **Propagation:** Efter du gemmer records kan det tage **minutter til op til 48 timer** før ændringer er synlige globalt (pga. cache). Under server-/IP-skift sætter mange TTL lavt først; bagefter hæver de det igen.

---

## Fejlsøgning med dig og nslookup

- **`dig mitdomæne.dk`** – viser DNS-svar (A, AAAA, nameservere osv.) og TTL. Nyttigt til at tjekke om DNS peger på den forventede IP.
- **`nslookup mitdomæne.dk`** – simplere lookup; viser også hvilken server der svarede.
- **"Domænet virker ikke":** Tjek at A/CNAME peger på rigtig IP; at TTL er udløbet så caches er opdateret; at firewall på serveren tillader port 80/443 (se [[Firewall-UFW-iptables]]).

DNS er *kortet* der fortæller verden, hvor jeres tjeneste ligger. Uden korrekte records rammer trafikken aldrig jeres server – eller rammer den forkerte.

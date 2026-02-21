---
tags:
  - dod
  - dns-firewall
---

# Dag 2 – Domæne, DNS og Firewall

> Teori til Dag 2 (9. juni). Her sætter I det navn, brugerne rammer – og den firewall, der beskytter serveren hvor *jeres* app kører. Se [[Program]] for dagens mål og plan. **Dybere pensum:** [[../../DNS-og-Firewall/00-DNS-og-Firewall-overblik]] (DNS, Cloudflare, UFW, NIS2/CRA).

---

## Domæner og subdomains

Et **domæne** (fx `mitprojekt.dk`) er det navn, brugerne skriver i browseren for at finde din server. Du kan enten købe et domæne hos en registrar (One.com, GoDaddy, Simply osv.) eller bruge et **subdomain** under et domæne, du har adgang til.

**Subdomains til undervisningen:** Underviseren har en række domæner, som I kan få tildelt et subdomain under – fx `jeresprojekt.mercantec.tech`, `gruppe2.gf2.dk` eller `app.mags.dk`. Domænerne er **mercantec.tech**, **gf2.dk** og **mags.dk**. De er købt hos **Simply** og har fået **flyttet DNS til Cloudflare** – så alle DNS-records administreres i Cloudflare, mens domæne-registreringen stadig står hos Simply. Det giver én samlet sted til at sætte jeres subdomain til at pege på jeres server.

- Domænet peger ikke af sig selv til en server – det skal kobles via **DNS**.
- Når du køber et domæne, får du adgang til at redigere DNS (enten hos registraren eller hos den leverandør, du flytter DNS til – her Cloudflare).

---

## DNS (Domain Name System)

**DNS** oversætter domænenavne til IP-adresser og andre oplysninger. Når nogen skriver `https://minside.dk`, spørger browseren DNS: "Hvilken IP har minside.dk?" – og får fx `192.0.2.42` tilbage. Derefter oprettes forbindelsen til den IP. DNS er altså det lag der svarer på: *Hvor findes denne server?* og *Hvilken server håndterer e-mail for dette domæne?* osv.

DNS er bygget op af **records** (poster) i en **zone** for dit domæne. Hver record har en **type**, et **navn** (host), en **værdi** og ofte en **TTL** (Time To Live – hvor længe svar må caches).

### DNS-records – oversigt

| Record type | Formål | Eksempel |
|-------------|--------|----------|
| **A** | Peger et **hostnavn** direkte til en **IPv4-adresse**. | `app` → `192.0.2.42` |
| **AAAA** | Som A, men til **IPv6**. | `app` → `2001:db8::1` |
| **CNAME** | Peger et **navn** videre til et **andet domænenavn** (alias). DNS udløser derefter A/AAAA for det andet navn. Kan ikke bruges på root (apex) af zonen. | `www` → `app.mercantec.tech` |
| **MX** | Angiver **mail-servere** for domænet (prioritet + host). Bruges når domænet skal modtage e-mail. | `10 mail.provider.com` |
| **TXT** | Frit tekstfelt. Bruges til verifikation (fx domæne-ejer), SPF/DKIM til e-mail, eller andre oplysninger. | `v=spf1 include:_spf.google.com ~all` |
| **NS** | Angiver **nameservere** for (sub)domænet. Bruges ved delegation (fx subdomain til anden zone) eller når du flytter DNS. | `ns1.cloudflare.com`, `ns2.cloudflare.com` |
| **CAA** | Angiver hvilke **certificate authorities** der må udstede certifikater for domænet. Øger sikkerhed omkring SSL. | `0 issue "letsencrypt.org"` |

I Cloudflare angiver du typisk **navn** som subdomain (fx `app` for `app.mercantec.tech`) eller `@` for root (`mercantec.tech`).

### Praktisk: A og CNAME til deployment

- **Root-domæne** (fx `mercantec.tech`): Brug et **A-record** med navn `@` der peger på din servers offentlige IP.
- **Subdomain** (fx `jeresprojekt.mercantec.tech`): Opret et **A-record** med navn `jeresprojekt` og IP = jeres server – eller et **CNAME** der peger på et andet host der allerede har A-record (så I kun opdaterer IP ét sted).

**TTL:** Efter du har gemt records, kan det tage tid (minutter til op til 48 timer) før ændringer spredes globalt. Korte TTL-værdier (fx 300 sekunder) giver hurtigere opdatering ved server-/IP-skift, men flere DNS-forespørgsler. Under udrulning sætter mange TTL lavt før de skifter; bagefter kan de hæve det igen.

### DNS’ ansvar under deployment

Under deployment er DNS det lag der **binder domænenavn til infrastruktur**:

1. **Go-live / skift af server:** I opretter eller ændrer A- eller CNAME-record så domænet peger på den nye servers IP. Indtil DNS er propagerede kan nogle brugere stadig ramme den gamle IP (cache).
2. **HTTPS og certifikater:** Let’s Encrypt (eller anden CA) bruger ofte DNS (fx TXT-record til HTTP-01-challenge eller DNS-01) til at verificere, at I kontrollerer domænet, før de udsteder certifikat. Uden korrekt DNS virker automatisk SSL ikke.
3. **Load balancing og CDN:** Hvis I bruger Cloudflare som proxy, peger A/CNAME på Cloudflares IP’er; Cloudflare står så for at sende trafikken videre til jeres rigtige server. DNS bestemmer altså *første hop* – herefter styres ruten af Cloudflare og jeres server.
4. **Fejlsøgning:** Hvis "domænet virker ikke", tjekker man ofte: `dig` / `nslookup` – peger DNS på den forventede IP? Har TTL udløbet så caches er opdateret?

Kort sagt: DNS er *kortet* der fortæller verden, hvor jeres tjeneste ligger. Uden korrekte records rammer trafikken aldrig jeres server – eller rammer den forkerte.

---

## At flytte DNS til Cloudflare (nameservers)

Domænerne mercantec.tech, gf2.dk og mags.dk er købt hos **Simply**, men **DNS er flyttet til Cloudflare**. Det betyder:

- **Simply** ejer stadig *registreringen* (at domænet er jeres og fornyes hos dem).
- **Cloudflare** håndterer *hvilke records domænet har* – altså hvad `mercantec.tech`, `app.mercantec.tech` osv. peger på.

### Hvorfor flytte DNS til Cloudflare?

- **Ét sted til alle records:** Hurtig opsætning af A, CNAME, TXT osv. i et tydeligt dashboard.
- **Proxy og sikkerhed:** Mulighed for at trafik går via Cloudflare (orange sky) med DDoS-beskyttelse, caching og SSL mod besøgende.
- **Skjult server-IP:** Ved proxy ser angribere Cloudflares IP’er, ikke jeres egen server-IP.
- **Ofte gratis og hurtig propagation:** Cloudflares DNS-netværk er globalt; ændringer spredes hurtigt.

### Sådan "flytter" man DNS til Cloudflare

1. **Tilføj domænet i Cloudflare** (Add site). Cloudflare scanner evt. eksisterende records og foreslår dem.
2. **Cloudflare viser to nameservere**, fx `ada.ns.cloudflare.com` og `bob.ns.cloudflare.com` (navnene varierer).
3. **Gå til din registrar (her Simply)** og find indstillingen for **Nameservers** / **DNS-servere** for domænet. Erstat de nuværende (Simply’s egne) med de to Cloudflare angav.
4. **Gem hos Simply.** Nu "ejer" Cloudflare DNS for domænet: alle forespørgsler om `*.mercantec.tech` sendes til Cloudflares servere, og det er de records I redigerer i Cloudflare, der gælder.
5. **Vent på propagation** (ofte 15 min – 24 timer). Cloudflare viser typisk status (Active) når de ser, at domænet bruger deres nameservers.

Efter flytningen opretter og redigerer I **alle** DNS-records i Cloudflare – ikke længere hos Simply. Subdomains (fx til jeres projekter) sættes derfor op som A- eller CNAME-records i Cloudflare under det pågældende domæne.

---

## Cloudflare – DNS og proxy

**Cloudflare** er både DNS-leverandør og "proxy" foran din server: trafikken til dit domæne kan gå via Cloudflares netværk først og derefter til din server. Domænerne I arbejder med (mercantec.tech, gf2.dk, mags.dk) er allerede flyttet til Cloudflare fra Simply – se ovenfor under **At flytte DNS til Cloudflare** for, hvordan sådan en flytning foretages.

- **DNS i Cloudflare:** Efter flytningen administrerer I alle records (A, CNAME, TXT osv.) i Cloudflares dashboard under det pågældende domæne. Her oprettes også subdomains til jeres projekter.
- **Proxy og sikkerhed:** For hvert record kan I vælge **Proxied** (orange sky) eller **DNS only** (grå sky). Når Proxied er slået til:
  - Går trafikken gennem Cloudflare (DDoS-beskyttelse, caching).
  - Besøgende får SSL/TLS (HTTPS) mod Cloudflare; Cloudflare håndterer kryptering mod jeres server.
  - Din servers rigtige IP er skjult – angribere ser Cloudflares IP’er.

**Praktisk:** Opret A- eller CNAME for jeres subdomain, peg på jeres servers IP, og vælg Proxied hvis I vil bruge Cloudflares beskyttelse og SSL; vælg DNS only hvis I fx selv håndterer SSL direkte på serveren (fx Let’s Encrypt på Nginx).

---

## Firewall – UFW og iptables

En **firewall** styrer hvilke indgående og udgående forbindelser der må passere. På Linux bruges ofte **iptables** (eller nftables) som den underliggende mekanisme. **UFW** (Uncomplicated Firewall) er et enklere lag ovenpå, så du kan arbejde med regler som "tillad SSH", "tillad HTTP/HTTPS" i stedet for at skrive iptables-regler manuelt.

### UFW – grundlæggende

- **Aktiver firewall:** `sudo ufw enable`
- **Tillad SSH (vigtigt før du aktiverer):** `sudo ufw allow 22/tcp` eller `sudo ufw allow ssh`
- **Tillad HTTP og HTTPS:** `sudo ufw allow 80/tcp` og `sudo ufw allow 443/tcp`
- **Se status og regler:** `sudo ufw status` (eller `status verbose`)
- **Default policy:** Ofte sættes default til at **nægte** indgående og **tillade** udgående: `sudo ufw default deny incoming` og `sudo ufw default allow outgoing`

Hvis du lukker SSH (port 22) uden at have anden adgang, kan du låse dig selv ude – så sørg altid for at tillade SSH før `ufw enable`.

### iptables (kort)

**iptables** er den ældre, mere tekniske måde at definere regler på. UFW skriver i praksis iptables-regler for dig. På nye systemer kan **nftables** være underlaget i stedet, men konceptet er det samme: regler baseret på port, protokol, kilde-IP osv.

---

## Informationssikkerhed – NIS2 og CRA

På Dag 2 skal I kunne redegøre for de **grundlæggende principper i NIS2 og CRA** og deres formål og anvendelse i virksomheden.

### NIS2 (Network and Information Security Directive 2)

- **Formål:** EU-direktiv der skal sikre højere **netværks- og informationssikkerhed** på tværs af lande og sektorer. Det stiller krav til blandt andet risikostyring, rapportering af incidenter og tekniske/organisatoriske foranstaltninger.
- **Anvendelse i virksomheden:** Virksomheder der falder under NIS2 (fx energi, transport, sundhed, digital infrastruktur, delvis offentlig forvaltning) skal bl.a. tage passende tekniske og organisatoriske sikkerhedsforanstaltninger og rapportere væsentlige sikkerhedshændelser til myndigheder. Det påvirker derfor hvordan I prioriterer sikkerhed, dokumentation og incident-håndtering.

### CRA (Cyber Resilience Act)

- **Formål:** EU-forordning der fokuserer på **sikkerhed af produkter med digitalt indhold** (software, IoT, hardware med software). Målet er at produkter er sikre "out of the box" og at sårbarheder håndteres gennem hele livscyklussen.
- **Anvendelse i virksomheden:** Virksomheder der udvikler eller sælger software/produkter med digitalt indhold skal leve op til krav om risikovurdering, sikkerhedsopdateringer og dokumentation. Det påvirker udviklingsprocessen, leverandørkæden og hvordan I håndterer sårbarheder og opdateringer.

Kort sagt: **NIS2** handler om sikkerhed af netværk og information i organisationer og sektorer; **CRA** handler om sikkerhed af de produkter (software/hardware) organisationer sælger eller bruger. Begge understøtter behovet for god firewall, opdateringer og overblik over risici – som I netop arbejder med på server og domæne.

---

## Læringsmål (opsummering)

1. Konfigurere DNS-records (A, CNAME) og forbinde et domæne til en server.
2. Opsætte og teste en firewall med UFW eller iptables.
3. Bruge Cloudflare til at beskytte og administrere trafik til mit domæne.
4. Redegøre for de grundlæggende principper i NIS2 og CRA's formål og anvendelse i virksomheden.

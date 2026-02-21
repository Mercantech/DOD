# Dag 1 – SSH og grundlæggende sikkerhed

> Teori til Dag 1 (8. juni). Alt det her er første skridt mod at få *jeres* app ud og i luften – I skal kunne komme sikkert ind på den server, hvor den skal køre. Se [[Program]] for dagens mål og plan.

---

## SSH (Secure Shell)

**SSH** er en krypteret protokol til at logge ind på og administrere en fjernserver over netværket. Al trafik (både login og kommandoer) er krypteret, så andre ikke kan læse med.

- **Port:** Standard port 22 (TCP).
- **Kommando:** `ssh bruger@host` – f.eks. `ssh root@192.168.1.10` eller `ssh ubuntu@min-server.dk`.
- **Nøglebaseret login:** I stedet for adgangskode kan du bruge et **nøglepar** (privat nøgle på din pc, offentlig nøgle på serveren). Det er mere sikkert og nemmere at automatisere.

### Oprette forbindelse

```bash
ssh bruger@server-ip-eller-domæne
```

Første gang du forbinder dig, bedes du acceptere serverens "fingerprint". Herefter kan du arbejde på serveren som om du sad fysisk ved den.

---

## Twingate VPN

**Twingate** er en Zero Trust VPN-løsning. I stedet for at åbne hele netværket, gives der kun adgang til de konkrete ressourcer (fx servere), som du har ret til.

- Serverne står typisk bag Twingate og er ikke direkte åbne mod internettet på port 22.
- Du installerer Twingate på din pc, logger ind, og kan derefter bruge SSH til kun de servere, din organisation har givet dig adgang til.
- Det begrænser angrebsfladen og gør det sværere for uvedkommende at finde og angribe serverne.

---

## Grundlæggende Linux-kommandoer

Kommandoer du bruger på serveren (ofte Ubuntu/Debian):

| Kommando | Beskrivelse |
|----------|-------------|
| `pwd` | Viser den nuværende mappe (path) |
| `ls` | Lister filer og mapper. `ls -la` viser også skjulte filer og detaljer |
| `cd <mappe>` | Skifter mappe. `cd ..` går et niveau op |
| `mkdir <navn>` | Opretter en mappe |
| `cat <fil>` | Viser indholdet af en fil |
| `nano <fil>` | Åbner filen i teksteditoren nano (nem at starte med) |
| `sudo <kommando>` | Kører kommandoen som administrator (root) |
| `systemctl status <tjeneste>` | Viser status for en systemtjeneste (fx ssh, nginx) |
| `exit` | Afbryder SSH-sessionen |

---

## SSH-sikkerhed

### Deaktivere root-login

**Root** er superbrugeren med fuld adgang. Hvis root kan logge ind med adgangskode over internettet, er det en favorit for angribere.

- Opret en almindelig bruger med `sudo`-rettigheder.
- Slå **root-login fra** i SSH-konfigurationen (`/etc/ssh/sshd_config`): `PermitRootLogin no`.
- Log herefter kun ind som den almindelige bruger og brug `sudo` når du skal have admin-rettigheder.

### Nøglebaseret adgang (key-only)

- **Adgangskoder** kan gættes, lækkes eller phishes. **SSH-nøgler** er lange, kryptografiske nøgler.
- Du har en **privat nøgle** på din pc (fx `~/.ssh/id_ed25519`) og en **offentlig nøgle** på serveren (i `~/.ssh/authorized_keys`).
- Serveren kan sættes til kun at acceptere nøglelogin: `PasswordAuthentication no`. Så er adgangskode-login slået fra.
- **Vigtigt:** Pas på den private nøgle – den må ikke deles eller lækkes. Du kan evt. sikre den med en passphrase.

---

## Systemopdateringer og pakkehantering

På Debian/Ubuntu bruges **apt** (Advanced Package Tool).

- **Opdater pakkelisten:** `sudo apt update`
- **Opgrader installerede pakker:** `sudo apt upgrade`
- **Installer en pakke:** `sudo apt install <pakkenavn>`

Sikkerhedsopdateringer leveres ofte gennem disse pakker. Regelmæssig `apt update` og `apt upgrade` lukker kendte huller og er en vigtig del af awareness og drift.

---

## Informationssikkerhed (kort)

### Trusler

- **Malware:** Skadelig software (virus, trojaner, spyware) – kan komme via downloads, mails eller sårbare services.
- **Phishing:** Forsøg på at lokke dig til at afsløre adgangskoder eller data (fx falske mails eller sider der ligner rigtige login-sider).
- **Ransomware:** Krypterer dine data og kræver løsesum for at frigive dem. Ofte via phishing eller sårbare tjenester.

Derfor er det vigtigt med stærk adgangskontrol, opdateringer og forsigtighed med links og vedhæftninger.

### Awareness-tiltag

- **Adgangskoder:** Stærke, unikke adgangskoder (eller bedre: **nøgler** som ved SSH) til vigtige systemer.
- **Tofaktorautentificering (2FA):** Ekstra trin (fx kode på telefon) så stjålne adgangskoder ikke er nok.
- **Sikkerhedsopdateringer:** Hold systemer og software opdateret (`apt upgrade`, opdateringer fra leverandører), så kendte sårbarheder lukkes.

Disse ting hører med til den daglige sikkerhedskultur – både på servere og på jeres egne maskiner.

---

## Læringsmål (opsummering)

1. Oprette forbindelse til en fjernserver via SSH og anvende grundlæggende Linux-kommandoer.
2. Konfigurere Twingate VPN og forstå, hvordan det sikrer adgang til servere.
3. Øge sikkerheden på en server ved at deaktivere root-login og anvende SSH-nøgler.
4. Redegøre for trusler (malware, phishing, ransomware) og for awareness-tiltag (adgangskoder, 2FA, sikkerhedsopdateringer).

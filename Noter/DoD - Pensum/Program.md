Valgfaget her bliver kun udbudt som online forløb. Der kan bookes lokale, givet at man vil arbejde på skolen, men jeres underviser eksistere kun online, gennem hele forløbet!

<aside>
💸

Rigtig meget af deployment og specielt på cloud-services kræver en form for betaling. Enten for et domæne, bekræfte identitet med kreditkort eller købe serverkraft. Kurset her er opbygget efter at I ikke skal have jeres kort op, men det er okay på frivillig basis selv at erhverve sig licenser, maskiner eller domæner for at få mere ud af kurset!

</aside>

# Kurset DoD – Deploy or Die

Kurset forudsætter grundlæggende forståelse for Git og hverdagsprogrammering. **Idéen er:** I har et hobbyprojekt – et spil, en hjemmeside, en API eller en full-stack applikation – og vi gennemgår, hvordan I får præcis *jeres* app ud og i luften. Der er nogle rammer og hensyn, men vi arbejder meget praktisk med sikkerhed integreret i hele forløbet. 
I helhed er der mest bare fokus på 3-ugers nørderi på tværs af programmering og infrastruktur

# Uge 24 - Opsætning af Server, VPN og generelt infrastruktur med sikkerhed!

## Dag 1 (8. juni) - **SSH og Grundlæggende Sikkerhed**

- Få egen server (DigitalOcean/AWS/Azure) - Vi bruger Datacenter maskinerne med Twingate
- SSH setup og Twingate VPN
- Grundlæggende Linux kommandoer
- SSH sikkerhed (disable root, key-only)
- System updates og pakke management
- **Informationssikkerhed:** Trusler – malware, phishing, ransomware. Awareness: adgangskoder vs. nøgler, sikkerhedsopdateringer.
- **Mål**: Eleverne kan logge ind på deres server og har grundlæggende sikkerhed

**:learning-motives: Dagens læringsmål**

1. Jeg kan oprette forbindelse til en fjernserver via SSH og anvende grundlæggende Linux-kommandoer
2. Jeg kan konfigurere Twingate VPN og forstå, hvordan det sikrer adgang til servere
3. Jeg kan øge sikkerheden på en server ved at deaktivere root-login og anvende SSH-nøgler
4. Jeg kan redegøre for trusler som malware, phishing og ransomware, og for awareness-tiltag (fx adgangskoder, tofaktorautentificering, sikkerhedsopdateringer)
- :theory-icon: Dagens teori → [[Dag-01-SSH-og-sikkerhed]]

## Dag 2 (9. juni) - **Domæne & DNS + Firewall**

- Køb domæne (eller brug subdomain)
- DNS konfiguration (A, CNAME records)
- Cloudflare setup
- UFW/iptables konfiguration
- **Informationssikkerhed** NIS2 og CRA – formål og anvendelse i virksomheden.
- **Mål**: Domæne peger på deres server og firewall er konfigureret

**:learning-motives: Dagens læringsmål**

1. Jeg kan konfigurere DNS-records (A, CNAME) og forbinde et domæne til en server
2. Jeg kan opsætte og teste en firewall med UFW eller iptables
3. Jeg kan bruge Cloudflare til at beskytte og administrere trafik til mit domæne
4. Jeg kan redegøre for de grundlæggende principper i NIS2 og CRA's formål og anvendelse i virksomheden
- :theory-icon: Dagens teori → [[Dag-02-Domæne-DNS-og-Firewall]]

## Dag 3 (10. juni) - **Database Setup med Docker**

- Docker installation – både **Docker Desktop** (lokalt) og **Docker på Linux** (server)
- Database container (PostgreSQL/MySQL)
- Database konfiguration og connection
- **Mål**: Database kører i container

**:learning-motives: Dagens læringsmål**

1. Jeg kan installere Docker og køre en container med en database (PostgreSQL, MySQL eller alternativ)
2. Jeg kan konfigurere adgang og forbindelser til databasen fra eksterne services
3. Jeg kan forklare fordelene ved at køre databaser i containere frem for direkte på serveren
- :theory-icon: Dagens teori → [[Dag-03-Database-Setup-med-Docker]]

## Dag 4 (11. juni) - **Web Server Setup (Nginx) + HTTPS & SSL**

- Nginx installation og konfiguration
- Virtual hosts setup
- Static file serving
- Let's Encrypt certifikat
- Auto-renewal setup
- HTTP → HTTPS redirect
- **Mål**: "Hello World" hjemmeside kører og sikre med HTTPS

**:learning-motives: Dagens læringsmål**

1. Jeg kan installere og konfigurere Nginx til at servere statiske filer via en virtuel host
2. Jeg kan udstede og aktivere et Let's Encrypt-certifikat med auto-fornyelse
3. Jeg kan tvinge HTTP-trafik over til HTTPS og forklare, hvorfor det er vigtigt
- :theory-icon: Dagens teori → [[Dag-04-Nginx-og-HTTPS]]

## Dag 5 (12. juni) - **Release & Noter | Loadbalance, Reverse Proxy og API Gateway**

- Test af komplet setup
- Dokumentation af processen
- Reflektion over læring
- Forberedelse til uge 2
- **Mål**: Eleverne har et fungerende setup og har reflekteret over processen

**:learning-motives: Dagens læringsmål**

1. Jeg kan dokumentere hele opsætningsprocessen fra server til HTTPS i et teknisk overblik
2. Jeg kan identificere de vigtigste sikkerhedsforbedringer, vi har implementeret
3. Jeg kan forklare, hvilke dele af forløbet jeg fandt mest udfordrende – og hvorfor
- :theory-icon: Dagens teori → [[Dag-05-Release-og-noter]]

# Uge 25 - **Containerization & CI/CD med Dokploy**

## Dag 6 (15. juni) - **Docker Grundlæggende**

- Docker installation
- Dockerfile skrivning
- Container build og run
- **Mål**: Simpel app i container

:learning-motives: **Dagens læringsmål**

1. Jeg kan installere Docker på en server og verificere, at det fungerer korrekt
2. Jeg kan skrive og bygge en Dockerfile til en simpel applikation
3. Jeg kan forklare forskellen på en image og en container, og hvordan de hænger sammen
- :theory-icon: Dagens teori → [[Dag-06-Docker-grundlæggende]]

## Dag 7 (16. juni) - **Docker Compose & Multi-container**

- Docker Compose setup
- Database + app container
- Environment variables
- **Mål**: Full-stack app i containers

:learning-motives: **Dagens læringsmål**

1. Jeg kan skrive en docker-compose.yml, der starter både en app og en database
2. Jeg kan bruge environment variables til at styre opsætning på tværs af containere
3. Jeg kan forklare, hvordan Docker Compose gør det nemmere at arbejde med flere services
- :theory-icon: Dagens teori → [[Dag-07-Docker-Compose]]

## Dag 8 (17. juni) - **Dokploy Installation, Setup & GitHub Integration**

- Volume mapping for database
- Data persistence setup
- Backup strategier
- **Mål**: Data overlever container restarts

:learning-motives: **Dagens læringsmål**

1. Jeg kan installere og konfigurere Dokploy på en server
2. Jeg kan forbinde et GitHub-repository med Dokploy og opsætte webhook
3. Jeg kan demonstrere, at et Git push udløser automatisk deployment via Dokploy
- :theory-icon: Dagens teori → [[Dag-08-Dokploy-og-GitHub]]

<aside>
<img src="notion://custom_emoji/78111fd7-5d55-4196-af1c-1918b8dd24a0/156dab5c-a237-805b-bb85-007af00f7c80" alt="notion://custom_emoji/78111fd7-5d55-4196-af1c-1918b8dd24a0/156dab5c-a237-805b-bb85-007af00f7c80" width="40px" />

H6’erne skal til svendeprøve i dag - derfor har I en selvstændig dag.

</aside>

## Dag 9 (18. juni) - **Docker Volumes, Data Persistence og Kubernetes**

- Dokploy installation på server
- Web interface konfiguration
- Git repository forbindelse
- Deploy app via Dokploy interface
- GitHub webhook setup
- Automated deployment ved push
- **Mål**: Dokploy er klar til deployment, Push til GitHub = automatisk deploy via Dokploy

:learning-motives: **Dagens læringsmål**

1. Jeg kan oprette volumes i Docker og forbinde dem til en container
2. Jeg kan sikre, at data i databasen overlever en genstart af containeren
3. Jeg kan forklare forskellen på bind mounts og volumes i praksis
4. Jeg forstår idéen med Docker Swarm og [Kubernetes](https://www.notion.so/Kubernetes-2c26819363c04f2eb1d93483304355e1?pvs=21) (k3s)
- :theory-icon: Dagens teori → [[Dag-09-Volumes-Dokploy-og-Kubernetes]]. Demo med K3s og volumes: [[Proxi-demo]]

## Dag 10 (19. juni) - **Monitoring & Logging med Dokploy**

- Dokploy's built-in monitoring
- Application logging via Dokploy
- Uptime monitoring (UptimeKhana)
- **Mål**: Overvågning af live app gennem Dokploy

:learning-motives: **Dagens læringsmål**

1. Jeg kan aktivere og bruge monitorering i Dokploy til at se status på mine apps
2. Jeg kan finde og forstå logs for min applikation i Dokploy
3. Jeg kan forklare, hvorfor monitorering og logging er vigtigt i drift af applikationer
- :theory-icon: Dagens teori → [[Dag-10-Monitoring-og-Logging]]

---

# Uge 26 - **Moderne Sikkerhed & CTF Challenge**

## Dag 11 (22. juni) - **OWASP Top 10 & Modern Security Headers**

- OWASP Top 10 (2021) - moderne version
- Security headers (CSP, HSTS, X-Frame-Options)
- Input validation og sanitization
- **Mål**: Moderne sikker kode praksis

:learning-motives: **Dagens læringsmål**

1. Jeg kan nævne og forklare flere af OWASP Top 10-sårbarhederne (2021)
2. Jeg kan implementere moderne sikkerheds-headers som CSP, HSTS og X-Frame-Options
3. Jeg kan identificere usikker inputhåndtering og forklare, hvordan det kan undgås
- :theory-icon: Dagens teori → [[Dag-11-OWASP-og-sikkerhed]]

## Dag 12 (23. juni) - **Container Security & Secrets Management**

- Docker security best practices
- Environment variables vs secrets
- Container scanning (Trivy, Snyk)
- **Mål**: Sikre containers og secrets

:learning-motives: **Dagens læringsmål**

1. Jeg kan gennemgå sikkerheds-praksis for Docker-containere (brugere, netværk, images)
2. Jeg kan forklare forskellen på environment variables og secrets – og hvornår man bruger hvad
3. Jeg kan scanne et Docker-image for kendte sårbarheder med fx Trivy eller Snyk
- :theory-icon: Dagens teori → [[Dag-12-Container-Security]]

## Dag 13 (24. juni) - **CTF Challenge - "Hack en app"**

- **Informationssikkerhed:** Etiske principper i arbejdet med data- og it-sikkerhed.
- **Mål**: Praktisk sikkerhedstestning gennem CTF

:learning-motives: **Dagens læringsmål**

1. Jeg kan bruge teknikker fra OWASP til at identificere sårbarheder i en applikation
2. Jeg kan dokumentere og forklare, hvordan en sikkerhedsbrist blev udnyttet
3. Jeg kan samarbejde i en gruppe om at analysere og angribe en applikation etisk og målrettet
4. Jeg kan redegøre for etiske principper i arbejdet med data- og it-sikkerhed
- :theory-icon: Dagens teori → [[Dag-13-CTF]]

## Dag 14 (25. juni) - **Monitoring & Incident Response / A/F**

- Security monitoring med Dokploy
- Log analysis og alerting
- Incident response plan
- **Informationssikkerhed:** Risikovurdering i konkrete hverdagssituationer.
- **Mål**: Overvågning og håndtering af sikkerhedsbegivenheder

:learning-motives: **Dagens læringsmål**

1. Jeg kan bruge logs og monitorering til at opdage unormal aktivitet eller fejl i systemet
2. Jeg kan forklare, hvad en incident response plan er, og hvorfor det er vigtigt
3. Jeg kan opstille en simpel plan for hvordan man reagerer på et sikkerhedsbrud
4. Jeg kan på et grundlæggende niveau indtænke risikovurdering i løsningen af konkrete hverdagssituationer
- :theory-icon: Dagens teori → [[Dag-14-Incident-Response]]

## Dag 15 (26. juni) - **Aflevering/fremlæggelse**

:learning-motives: **Dagens læringsmål**

1. Jeg kan samle og præsentere dokumentation for hele projektets infrastruktur og drift
2. Jeg kan forklare vores vigtigste tekniske beslutninger og reflektere over dem
3. Jeg kan præsentere vores løsning klart, teknisk og relevant – både det der virkede og det der ikke gjorde
- :theory-icon: Dagens note → [[Dag-15-Aflevering]] (ingen teori – aflevering)

## **Aflevering – Deployment Projekt**

### **Formål**

I har i grupper arbejdet med at deploye et projekt til en rigtig server med fokus på infrastruktur, sikkerhed, CI/CD og drift. Afleveringen handler ikke kun om at vise, hvad I *fik til at virke* – men også om, hvad I lærte undervejs.

---

## ✍️ **Indholdskrav (uanset format)**

Alle grupper skal besvare de samme spørgsmål – *uanset* om I afleverer som rapport, video eller fremlæggelse:

1. **Projektbeskrivelse:**
    - Hvad har I forsøgt at bygge/deploye?
    - Hvilken tech stack brugte I?
2. **Infrastruktur og Deployment:**
    - Hvordan er det sat op? (Server, domæne, HTTPS, etc.)
    - Brugte I Docker, Nginx, database?
3. **CI/CD Pipeline:**
    - Hvordan deployer I? (Dokploy, GitHub Actions, manuelt)
    - Brug af versionstyring, branches, automatisering?
    - Indblik i projekt-styring med DevOps, GH-Projects eller lign.
4. **Sikkerhed:**
    - Hvilke tiltag tog I? (SSH, firewall, SSL, OWASP, secrets)
5. **Monitoring og Drift:**
    - Hvordan holder I øje med at jeres løsning kører?
    - Brug af logs, uptime-tools, fejlhåndtering?
6. **Læring og Refleksion:**
    - Hvad gik godt? Hvad gik skævt?
    - Hvad har I lært – teknisk og samarbejdsmæssigt?

---

## 📦 **Afleveringsformater (vælg én)**

### 📝 **1. Rapport (PDF / Google Docs)**

En skriftlig beskrivelse af jeres projekt og process, max 6 sider (ekskl. billeder). Altså 14.400 tegn med mellemrum. Opgaven her minder mest om en produktrapport til jeres svendeprøve, så det kan være god træning til den tid!

**Krav:**

- Strukturér rapporten efter de 6 punkter
- Gerne med screenshots, shell output, GitHub links osv.

📥 **Afleveres via Teams som en PDF**

🕓 **Deadline**: 26. juni kl. 23:59

---

### 🎥 **2. Videoaflevering (max 10 minutter)**

En kort screencast hvor I **viser og forklarer** jeres løsning og hvordan den fungerer. Ingen krav om webcam – kun lyd og skærm er fint. Alle gruppe medlemmer skal være med og sige noget af projektet. Om I sidder i et opkald og optager eller tager final-cut ud og klipper sammen er op til jer, men det skal sendes som en fil!

**Krav:**

- Følg de 6 punkter mundtligt
- Vis jeres opsætning, GitHub repo, terminal, app m.m.
- Hold det konkret og fokuseret

📥 **Sendes på teams som en MP4**

🕓 **Deadline**: 26. juni kl. 23:59

---

### 🗣️ **3. Mundtlig fremlæggelse (grupper)**

I fremlægger jeres projekt **live** online på 10 minutter + 5 min spørgsmål. Fremlæggelsen er som standart åben for alle, men ved særlige årsager, kan det godt gøres kun med underviser og gruppen!

**Krav:**

- Kort præsentation efter de 6 punkter
- Vis evt. dele af jeres løsning (demo, repo, terminal)
- Alle i gruppen skal være med og alle siger noget

📥 **Tilmeld jer en tid via skema (kommer i uge 25)**

🕓 **Afvikles: 26. juni**

---

## 🧠 **Vurderingskriterier**

Det handler ikke om hvor “færdigt” det hele er, men om:

- Forståelse af **infrastruktur og deployment**
- Refleksion over **valg, fejl og løsninger**
- Evne til at **dokumentere og forklare** tekniske processer

---
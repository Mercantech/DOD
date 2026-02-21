---
tags:
  - dod
  - cicd
---

# Dag 5 – Release & Noter | Loadbalance, Reverse Proxy og API Gateway

> Teori til Dag 5 (12. juni). Se [[Program]] for dagens mål og plan.

---

## Reverse proxy

En **reverse proxy** er en server der modtager klienters forespørgsler og sender dem videre til en eller flere **backends** (web servere, applikationer, API’er). Klienten taler kun med proxyen; den ved ikke hvem der rent faktisk serverer indholdet.

### Hvad bruges det til?

- **Ét indgangspunkt:** Flere backends (fx statisk fil-server, app på port 3000, API på port 8080) kan siddes bag én adresse og ét domæne. Proxyen vælger hvem der skal have request ud fra path, host header osv.
- **SSL-terminering:** Klienten bruger HTTPS mod proxyen; proxyen kan tale HTTP internt til backends (eller igen HTTPS). Certifikatet og krypteringen håndteres ét sted – på proxyen.
- **Skjule backend:** Backends behøver ikke eksponere porte udad; kun proxyen er synlig. Det begrænser angrebsfladen og giver mulighed for firewall-regler kun mod proxyen.
- **Caching og komprimering:** Proxyen (fx Nginx) kan cache svar og komprimere indhold, så backends bliver mindre belastet og svartiden falder.

### Nginx som reverse proxy (eksempel)

```nginx
location /api/ {
    proxy_pass http://localhost:3000/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

- `proxy_pass` – hvem der skal have requesten (her app på 3000).
- **Headers:** Backend får ofte brug for at vide den oprindelige host, klient-IP og om requesten kom ind over HTTPS (`X-Forwarded-Proto`), fx til redirects og logging.

---

## Load balancing

**Load balancing** betyder at fordele indgående trafik på **flere backend-instanser**, så ingen enkelt server bliver flaskehals. Reverse proxyen (fx Nginx) kan samtidig være load balancer ved at pege på en **upstream** med flere servere.

### Algoritmer (kort)

| Algoritme | Beskrivelse |
|-----------|-------------|
| **Round-robin** | Fordeler request efter tur på hver server. Simpel og ofte standard. |
| **Least connections** | Sender til den server der har færrest aktive forbindelser. God når forbindelser holder længe. |
| **IP hash** | Samme klient-IP sendes altid til samme server. Kan bruges til session-stickyness (uden dedikeret session-store). |

### Nginx upstream (eksempel)

```nginx
upstream app_backend {
    least_conn;
    server 127.0.0.1:3000;
    server 127.0.0.1:3001;
    server 127.0.0.1:3002;
}

server {
    location / {
        proxy_pass http://app_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

- **Health checks:** I produktion vil man ofte tjekke at backends er raske (Nginx Plus eller andre værktøjer; ellers fjernes en server manuelt fra upstream ved fejl). Uden health check kan Nginx stadig sende trafik til en nedlagt server indtil den fejler.

### Hvorfor load balance?

- **Skalering:** Flere app-instanser bag én adresse; mere trafik kan håndteres.
- **Tilgængelighed:** Hvis én instans går ned, kan de andre stadig servere (når der er health check eller manuel fjernelse).
- I jeres forløb møder I det igen når I kører flere containere eller bruger Dokploy/Kubernetes – der er det ofte netværket/orchestratoren der round-robin’er til pods.

---

## API Gateway

Et **API gateway** er et **indgangspunkt** for API-kald: klienter kalder ét endpoint (gatewayen), og gatewayen ruter videre til de rigtige backend-tjenester, og kan på vejen håndtere auth, rate limiting, logging og transformation.

### Typiske opgaver

- **Routing:** Fx `/users` → user-service, `/orders` → order-service. Én base-URL for klienten, flere backends bagved.
- **Autentificering og autorisation:** Validering af API-nøgler, JWT eller OAuth; kun gyldige kald når videre.
- **Rate limiting:** Begrænse antal kald per bruger/IP for at undgå misbrug og overbelastning.
- **Logging og metrikker:** Central logging af alle API-kald, så I kan fejlsøge og overvåge.
- **Transformation:** Omskrivning af headers, aggregation af flere backend-kald til ét svar (BFF-mønster).

### Nginx som enkel gateway

Nginx kan bruge **location**-blokke og **proxy_pass** til at rute forskellige paths til forskellige backends – det er en **letvægts** API gateway. Dedikerede produkter (Kong, AWS API Gateway, Azure API Management, Traefik med middleware) tilbyder mere: indbygget rate limiting, auth-plugins, dashboard, OpenAPI-import osv.

**Eksempel – routing efter path:**
```nginx
location /api/v1/users {
    proxy_pass http://user-service:3000;
    # ... headers
}
location /api/v1/orders {
    proxy_pass http://order-service:3001;
    # ... headers
}
```

---

## Dokumentation og teknisk overblik

At **dokumentere** opsætningen (server → DNS → firewall → database → Nginx → HTTPS) gør det nemmere at genbruge, fejlsøge og overlevere. Et teknisk overblik behøver ikke være langt – det skal beskrive **hvad** I har og **hvordan** det hænger sammen.

- **Komponenter:** Hvilke tjenester kører hvor (OS, Nginx, Docker, database, app). Evt. portliste.
- **Flow:** Hvordan kommer en bruger fra domænet til jeres app? (DNS → server → firewall → Nginx → HTTPS → backend.)
- **Konfiguration:** Hvor ligger vigtige filer (Nginx sites, certifikater, env)? Ikke nødvendigvis hele indholdet, men stier og formål.
- **Sikkerhed:** Kort over tiltag (SSH key-only, firewall, HTTPS, evt. Cloudflare). Det understøtter både refleksion og afleveringskrav på Dag 15.

---

## Refleksion og sikkerhedsforbedringer

Læringsmålene beder om at **identificere de vigtigste sikkerhedsforbedringer** og **forklare hvad der var mest udfordrende**. Det er nyttigt at tænke i konkrete kategorier:

- **Adgang:** SSH (nøgler, disable root), firewall (kun nødvendige porte), VPN/Twingate.
- **Trafik og data:** HTTPS, Let’s Encrypt, evt. Cloudflare som proxy.
- **Tjenester:** Database kun tilgængelig internt eller via begrænsede porte; app kun bag Nginx.
- **Opdateringer og secrets:** System updates (apt), stærke passwords/hemmeligheder, ingen credentials i kode.

At reflektere over **hvad der var sværest** (DNS? Certbot? Docker-netværk?) giver indsigt i hvor I skal dykke dybere eller øve mere – og det kan ind i jeres aflevering og fremtidige projekter.

---

## Læringsmål (opsummering)

1. Dokumentere hele opsætningsprocessen fra server til HTTPS i et teknisk overblik.
2. Identificere de vigtigste sikkerhedsforbedringer, I har implementeret.
3. Forklare, hvilke dele af forløbet I fandt mest udfordrende – og hvorfor.

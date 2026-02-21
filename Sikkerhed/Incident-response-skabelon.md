---
tags:
  - dod
  - sikkerhed
  - sikkerhed/incident
---

# Incident response – skabelon

> **Dybere end dagens teori:** Faser og simpel plan-skabelon. Dag-note: [[../Noter/DoD - Pensum/Dag-14-Incident-Response]]. Monitoring: [[../Noter/DoD - Pensum/Dag-10-Monitoring-og-Logging]].

---

## Faser i incident response

| Fase | Kort indhold |
|------|--------------|
| **1. Detect** | Opdage at noget er galt – via monitoring, logs, brugerrapporter eller alerts. |
| **2. Contain** | Begrænse skaden: stop kompromitteret service, luk hul, bloker IP, skift credentials. |
| **3. Eradicate** | Fjerne årsagen: patch sårbarhed, fjern malware, ret fejlkonfiguration. |
| **4. Recover** | Få systemet sikkert i drift igen; verificer at angrebet ikke gentager sig. |
| **5. Post-incident** | Dokumenter hvad der skete og hvad I lærte; opdater planen. |

---

## Simpel plan-skabelon til jeres gruppe

1. **Definition:** Hvad tæller som incident? (fx app nede, mistanke om uautoriseret adgang, synlige fejl der lækker data.)
2. **Opdagelse:** Hvor kigger I? (Dokploy status og Logs, Uptime Kuma, brugerhenvendelser.)
3. **Første skridt:** Hvem gør hvad? (én tjekker logs, én kan stoppe/redeploy containeren, én noterer tidslinje.)
4. **Inddæmning:** Hvad gør I med det samme? (stop app, skift adgangskoder, luk firewall til IP.)
5. **Dokumentation:** Hvor gemmer I noter om hvad der skete og hvad I gjorde?
6. **Efterfølgende:** Hvordan følger I op? (ret sårbarhed, opdater dependencies, gennemgå planen.)

En kort, fælles plan gør at I reagerer struktureret i stedet for ad hoc. Se Dag 14 for risikovurdering og sikkerhedsmonitoring med Dokploy.

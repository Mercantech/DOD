---
tags:
  - dod
  - cicd
  - cicd/dokploy
---

# Dokploy – volumes og monitoring

> **Dybere end dagens teori:** Volumes til data persistence og monitoring/logs i Dokploy. Dag-noter: [[../Noter/DoD - Pensum/Dag-09-Volumes-Dokploy-og-Kubernetes]], [[../Noter/DoD - Pensum/Dag-10-Monitoring-og-Logging]]. Docker volumes: [[../docker/Volumes-og-data]].

---

## Volumes i Dokploy

- For **database** (Postgres, MySQL) skal data ligge i et **volume** – ellers forsvinder de ved container-genstart eller ny deploy. I Dokploy konfigurerer I typisk **volume mapping**: hvilken host-sti eller named volume der skal mountes til hvilken sti i containeren (fx `/var/lib/postgresql/data`).
- **Named volumes** (som i [[../docker/Volumes-og-data]]) overlever genstart; **bind mounts** mapper en konkret mappe på serveren. Brug named volumes til database-data i produktion.

Backup af database kan sættes op manuelt (dump til fil) eller via scripts/Dokploy efter behov.

---

## Monitoring og logs

- **Status:** I Dokploy’s oversigt ser I om containere kører (Running), er stoppet eller i CrashLoop. **Ressourcer** (CPU/RAM) vises ofte per container.
- **Logs:** Under hver app findes **Logs** – build-logs (output fra build) og **runtime/container-logs** (det appen og containeren skriver til stdout/stderr). Brug dem til fejlsøgning når noget crasher eller opfører sig mærkeligt.
- **Uptime:** Ekstern overvågning (fx Uptime Kuma) kan tjekke om jeres offentlige URL svarer – uafhængigt af Dokploy. Se Dag-note [[../Noter/DoD - Pensum/Dag-10-Monitoring-og-Logging]].

Sikkerhedsmonitoring og incident response bygger videre på disse logs – [[../Noter/DoD - Pensum/Dag-14-Incident-Response]].

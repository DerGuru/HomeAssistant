# Potenzial – Analyse & Verbesserungsvorschläge

Analysiert am 2026-08-17 gegen die Live-Instanz (HA Core 2026.8.2, HA Green) via MCP
sowie die Workspace-Dateien. Jeder Punkt nennt **Fund**, **Vorschlag** und **Warum besser**.
Reihenfolge = grob nach Aufwand/Nutzen. Am Ende stehen bewusst auch die **Stärken**, damit
klar ist, was *nicht* angefasst werden sollte.

---

## P0 – Konkrete Bugs / Fehlklassifikation (zuerst)

### 1. Grid-Sensor-Referenz — ✅ ERLEDIGT (2026-08-17)
- **Fund:** Die Einspeisebremse nutzte `sensor.hausenergie_netzbezug` — existiert nicht. Realer Sensor: `sensor.hausgesamtenergie_power` (Shelly EM, Anzeigename bereits „Netzbezug", Vorzeichen: positiv=Bezug, negativ=Einspeisung).
- **Wirkung des Bugs:** `float(0)`-Default → `strong_export` nie `true` → Einspeisebremse war **still tot** (auch in Produktion, in beiden Helfern).
- **Fix:** Referenz in **R Target** + **L Target** (Live-Helfer) und im Draft `TargetSolar.yaml` auf `sensor.hausgesamtenergie_power` korrigiert. Verifiziert: beide Sensoren rendern (r/l_target), Bremse wieder scharf.
- **Kein Rename:** Den Shelly-Sensor NICHT umbenennen — Consumer `HomeActualPower` + `Summe Haus und Heizung` würden brechen; Rename verlagert den Bug nur.

### 2. Zwei divergierende Kopien — (Blueprint/Dedup offen)
- **Fund:** `sensor.r_target`/`sensor.l_target` = zwei Template-Helfer (.storage), byte-identisch bis auf `currentSide`-Swap. `TargetSolar.yaml` (Repo-Root, NICHT eingebunden) = 1:1-Kopie des R-Helfers, reiner Draft/Backup.
- **Warum relevant:** Der Grid-Bug steckte in **zwei** Kopien → Fix musste doppelt gemacht werden. Argument für Parametrisierung (siehe P2).
- **Vorschlag:** Draft klar als Backup kennzeichnen; mittelfristig Konstanten in Helfer auslagern (P2.9), damit Tuning nicht doppelt driftet.

### 3. Tote / halb-deaktivierte Automationen
- **Fund:**
  - `Ding Dong` (`1779097838351`): Trigger vorhanden, `actions: []` → macht nichts.
  - `Büro OG Fenster auf bei offener Tür unter 15C` (`1736946120721`): die `numeric_state`-Bedingung (<15 °C) ist `enabled: false`, der komplette TTS-`repeat`-Block ist `enabled: false`, ein `delay` ebenso. Übrig bleibt nur die Handy-Notification – die Außentemperatur-Bedingung im Namen greift also gar nicht.
- **Vorschlag:** Entscheiden: aktivieren, entfernen oder mit Kommentar als „bewusst pausiert" markieren. Bei dauerhaftem Deaktivieren die Automation im Entity-Registry disablen statt Blöcke einzeln `enabled: false` zu lassen.
- **Warum besser:** Halb-neutralisierte Regeln verschleiern die tatsächliche Wirkung, führen zu stillen No-Ops und sind ein Risiko, sobald jemand sie „reaktiviert" ohne den Kontext zu kennen.
- **Status (2026-08-17):** ✅ `Büro OG Fenster` umbenannt zu „Büro OG Fenster auf bei offener Tür" (kein „15C" mehr) + device_id→entity_id; beide Blöcke bleiben auf Nutzerwunsch bewusst `enabled: false` drin. ✅ `Ding Dong` vom Nutzer gelöscht (live nicht mehr vorhanden, Repo synced, 38→37 Automationen).

---

## P1 – Robustheit / HA-Best-Practices

### 4. `device_id` statt `entity_id` in UI-erstellten Automationen — ✅ ERLEDIGT (2026-08-17)
- **Fund (Auswahl):**
  - `Büro OG Fenster` – `device`-Trigger + `is_open`-`device`-Conditions mit Hex-`device_id`/`entity_id`.
  - `SaugenEG` – Button-Press über `device_id` + Hex-`entity_id`.
  - `Roborock Return To Base` – `vacuum.dock` über `device_id`.
  - `Zitrone gießen` – `humidity`-`device`-Trigger + `is_humidity`-`device`-Condition.
  - `HeizungsBoost` / `HeizungsBoost`-Rückstellung – `number.set_value` über `device_id`.
  - `Schlafzimmer` (`1776798325469`) – ZHA-`device`-Trigger + `light.toggle` auf `device_id`.
- **Vorschlag:** Auf `entity_id` umstellen (bei ZHA-Buttons bevorzugt `event`-Trigger mit `device_ieee`, wie ihr es in `templates/*ButtonEvents.yaml` bereits vorbildlich macht).
- **Warum besser:** `device_id` bricht, sobald ein Gerät neu gepairt/ersetzt wird (neue ID). `entity_id` ist stabil, lesbar und durchsuchbar (`grep`). Die kryptischen Hex-IDs machen die YAML zudem unlesbar und nicht diff-freundlich.
- **Status (2026-08-17):** 8 Automationen live umgestellt (Büro OG Fenster, Fenster offen b. Abschließen, Roborock RTB, BüroEG Licht An/Aus, Zitrone gießen, HeizungsBoost, Auto bewegt sich). HeizungsBoost zusätzlich `wait_template`→`wait_for_trigger` (mit Guard). #7 `Licht – Schlafzimmer (Shortcut)` ✅ auf das Haus-Pattern umgebaut: neue Trigger-Template-Event-Entity `event.schlafzimmer_shortcut` (`templates/SchlafzimmerShortcutButtonEvents.yaml`, mappt Cluster-6-`command`→`single/double/hold/release`), Automation triggert jetzt via `event.received` — Funktion erweitert (single=toggle, hold=zirkuläres Dimmen über `brightness_step_pct`-Dreieckwelle, release=Stop via `mode: restart`, double=1%↔100%). **Getestet ✅** (Cluster-Fix: on/off=Cluster 6, move/stop=Cluster 8 → Template filtert nur `device_ieee`). `target_device` in TTS-Scripts bleibt (legitimer Device-Selector).

### 5. ~~Deprecated `behavior: any` (2026.7)~~ — KEIN Problem (Fehlalarm)
- **Fund:** `Garten – Alle Sprenger nacheinander` nutzt in der `valve.is_open`-**Condition** `options: {behavior: any, for: "00:00:00"}`.
- **Korrektur (2026-08-17):** Die Umbenennung `any`/`last` → `each`/`all` betrifft **nur Trigger**. Bei **Conditions** bleibt `any` (Default) / `all` unverändert gültig (Skill-Referenz `automation-patterns.md#purpose-specific-...`). Verifiziert: Repairs = **0 Issues** auf Core 2026.8.2. → **Kein Deprecation-Risiko, nichts zu tun.**
- **Optional (kosmetisch, niedrige Prio):** `options`-Block entfernbar — `any` ist Default, `for: 00:00:00` ist No-op. Nur mitnehmen, wenn wir ohnehin an der Automation arbeiten.

### 6. Webhooks — ✅ ERLEDIGT (2026-08-17): alle 5 live entfernt
- **Fund:** 5 Webhooks, ALLE `local_only: true`: `esstisch`, `SaugenEG`, `Flurlicht`, `Wohnzimmerdeckenlicht`, `Treppenlicht` — alle mit `GET` (meist auch `HEAD`).
- **Relativierung:** Wegen `local_only: true` ist das Prefetch/Crawler-Risiko **gering** (extern nicht erreichbar). Die Restgefahr ist lokales Link-Prefetching.
- **Vorschlag (mit Vorsicht):** NICHT blind GET strippen — `esstisch` wird laut Kommentar „von Fritz" aufgerufen; wenn der Aufrufer GET nutzt, bricht der Taster. Erst Aufrufer ermitteln, dann Aufrufer + Webhook gemeinsam auf POST.
- **Warum überhaupt:** POST ist semantisch korrekt für zustandsändernde Aktionen; GET-Endpunkte sind prinzipiell leichter versehentlich auslösbar.
- **Status:** Alle 5 Automationen live gelöscht — der Fritz-DECT-440 → Fritzbox → HA-Pfad existiert nicht mehr, und alle hatten nur den Webhook als Trigger.

---

## P2 – Duplikation → Blueprints (Wartbarkeit)

### 7. Vier fast identische Heizkreis-Raum-Automationen — Blueprint erstellt
- **Fund:** `Arbeitszimmer EG`, `Arbeitszimmer OG`, `Kinderzimmer`, `Schlafzimmer` (Heizkreis) sind bis auf **drei** Werte identisch (Fenster-`binary_sensor`, `climate`-Thermostat-Attribut-Trigger, `zbmini_entity`). Alle: HA-Start + Fenster + Thermostat-Sollwert → 300 ms Delay → `script.heizkreisventilsteuerung`.
- **Status:** ✅ ERLEDIGT (2026-08-17) — Blueprint `blueprints/automation/heizkreis_raumsteuerung.yaml` deployed; alle 4 Automationen live per Config-API auf `use_blueprint` migriert (Kategorie erhalten, alle `on`). entity_ids inzwischen angeglichen: EG=`automation.arbeitszimmer_eg`, Schlafzimmer-Heizkreis=`automation.heizkreis_schlafzimmer` (siehe P3.11).
- **Warum besser:** Single Source of Truth – ein Bugfix/Feature wirkt für alle Räume; ein neuer Raum ist eine Instanz statt Copy-Paste. Reduziert die Fehlerfläche (aktuell muss jede Änderung 4× gepflegt werden).

### 8. Zwei identische „Anker Set L/R Target"-Automationen — ✅ ERLEDIGT (2026-08-17)
- **Fund:** `Anker Set L Target` und `Anker Set R Target` unterscheiden sich nur im Seiten-Präfix (`l_`/`r_`). Beide ~60 Zeilen `choose`-Logik.
- **Vorschlag:** Als Blueprint mit Input „Seite" (Sensoren/Switch/Number als Inputs) oder als eine Automation mit `trigger`-Variablen. `TargetSolar.yaml` ist mit `currentSide`/`otherSide` ohnehin schon seiten-parametrisiert – die Automationen können demselben Muster folgen.
- **Warum besser:** Gleiche Duplikations-Argumente wie oben; die Solar-Regelung ist sicherheits-/energetisch relevant, da will man Logik nicht doppelt driften lassen.
- **Status:** Blueprint `blueprints/automation/anker_solarbank_output.yaml` (4 Entity-Inputs); beide Automationen live migriert, `state: on`, Kategorie erhalten. Repo-Kopie vorhanden.

### 9. Konstanten aus `TargetSolar.yaml` in Helfer auslagern — ✅ ERLEDIGT (2026-08-17)
- **Fund:** Tuning-Parameter (`pv_boost`, `export_limit`, `min/max_output`, `min_soc`, `fill_small_remainder`, `cover_low_demand`) sind als Jinja-`{% set %}` hart im Template.
- **Vorschlag:** Die Stellschrauben als `input_number`/`input_boolean`-Helfer anlegen und im Template referenzieren.
- **Warum besser:** Live-Tuning per Dashboard ohne Datei-Edit + Template-Reload; kein Redeploy nur um `pv_boost` von 1.0 auf 1.5 zu setzen. Entspricht dem HA-Prinzip „Werte in Helfer, nicht hardcoden".
- **Status:** step/export_limit/pv_boost → `input_number.solar_precision_factor` / `solar_export_limit` / `solar_pv_steering_factor`; fill_small_remainder/cover_low_demand → `input_boolean.prefer_solar_power_on_gap` / `prefer_solar_power_on_low_demand` (alle Area Energie Management). `min_output`/`max_output`/`min_soc` bleiben bewusst hart (unveränderliche Grenzen). r/l_target vor/nach identisch (170/160).

### 10. Drei strukturgleiche Zigbee-Button-Template-Dateien
- **Fund:** `templates/Oberflurschalter…`, `…Treppenschalter…`, `…Wohnzimmerschalter…ButtonEvents.yaml` sind bis auf `device_ieee`/Namen identisch. `W100AutomationTemplate.yaml` = **bewusste Vorlage** des Nutzers zum Kopieren, wenn ein Taster etwas auf den HomePods ausgeben soll (leere `sequence: []` sind Absicht, KEIN toter Code).
- **Vorschlag:** Muster beibehalten (siehe Stärken). Optional die Automations-Seite über ein Blueprint erzeugen; die Template-Event-Entities bleiben.
- **Warum besser:** Neue Wandschalter = ein Blueprint-Aufruf statt drei Blöcke kopieren und `device_ieee` von Hand ersetzen (fehleranfällig).

---

## P3 – Kleinere Hygiene

### 11. Mehrfach vergebene / mehrdeutige Aliase
- **Fund:** `Schlafzimmer` existiert mehrfach (Heizkreis-Steuerung **und** ZHA-Remote-Toggle); dazu generische Namen wie `Bad OG`.
- **Vorschlag:** Eindeutige, präfixierte Aliase (z. B. `Heizkreis – Schlafzimmer`, `Licht – Schlafzimmer Remote`).
- **Warum besser:** Logbook, Traces und die Automations-Übersicht werden eindeutig; man kann Regeln zuverlässig referenzieren.
- **Status:** ✅ ERLEDIGT (2026-08-17) — 26 Aliase per Config-API (`python_transform`, nur `alias`) auf Schema `Bereich – Detail` umbenannt: Präfixe `Heizkreis`/`Licht`/`Heizung`/`Solar`/`Garten`. Kollision aufgelöst. Repo `automations.yaml` re-synced.
- **entity_id-Angleichung** ✅ ERLEDIGT (2026-08-17) — Impact-Analyse ergab **0 Referenzen** (Automationen/Skripte/Szenen/Helfer/Dashboards). Per `ha_set_entity` umbenannt: `new_automation_2`→`automation.arbeitszimmer_eg`, `schlafzimmer_2`→`automation.heizkreis_schlafzimmer`, `schlafzimmer_3`→`automation.licht_schlafzimmer_shortcut`. Alte IDs 404, neue `on`. (entity_id steht in der Registry, nicht in `automations.yaml` → kein Repo-Change.)

### 12. Dynamische Service-Namen per Template
- **Fund:** `Licht – Schlafzimmer Sync` baute `light.turn_{{ states(...) }}` / `switch.turn_{{ states(...) }}`.
- **Analyse (2026-08-17):** `turn_unavailable` konnte in der Praxis NICHT passieren — die Automation-Guard `{{ trigger.to_state.state in ['on','off'] }}` und der Umstand, dass der Template die auslösende Entity liest, garantieren `on`/`off`. Einzige Theorie-Lücke: winziges Race, falls das Gerät zwischen Trigger und Ausführung `unavailable` wird (Live-`states()`-Read). Kein Performance-Thema (Template-Render ~0,1–0,5 ms, << Zigbee-I/O).
- **Status:** ✅ ERLEDIGT (2026-08-17, Option 2) — Service-Strings auf `light.turn_{{ trigger.to_state.state }}` / `switch.turn_{{ trigger.to_state.state }}` umgestellt (Snapshot zum Trigger-Zeitpunkt statt Live-Read). Schließt das Race vollständig; minimaler 2-Zeilen-Diff. Repo synced, Automation `on`. Hinweis: Service-Name bleibt getemplatet → Best-Practice-Linter warnt weiter (bewusst akzeptiert, reales Risiko = 0). Voller `if/then/else`-Umbau war Option 3, nicht gewählt.


---

## Stärken – bewusst NICHT anfassen

- **Heizkreis-Script-Architektur** (`scripts.yaml`): Dispatcher + `area_id()`/`area_entities()`-Auflösung + `response_variable` (`any_window_open`) sind sauber, nativ und DRY. Sehr gut.
- **Zigbee-Buttons → Event-Entities** (`templates/*ButtonEvents.yaml`): `zha_event` mit persistentem `device_ieee` in stabile `event.*`-Entities zu wandeln und Automationen auf `event.received` triggern zu lassen, ist genau die empfohlene Vorgehensweise. Vorbildlich.
- **`Legionellenprogramm Warmwasser`**: klar strukturiert, `wait_template` + Timeout + sauberes Zurücksetzen der Sollwerte.
- **Garten-Automationen**: nutzen native `numeric_state`/`valve.is_open`-Conditions und Bewässerung über einen generischen Kreis-Runner (`bewasserung_kreis_ausfuhren`) – gute Wiederverwendung.

---

## Vorgeschlagene Reihenfolge

1. ~~**P0.1/P0.2** – Solar-Netzbezugs-Sensor fixen~~ ✅ erledigt 2026-08-17 (beide Helfer + Draft korrigiert, Bremse wieder scharf).
2. **P0.3** – ✅ `Büro OG Fenster` erledigt; ✅ `Ding Dong` gelöscht.
3. ~~**P1.5** – `behavior: any` migrieren~~ ✅ geklärt 2026-08-17: Fehlalarm (nur Trigger deprecated, nicht Conditions); Repairs=0. Optional kosmetischer Cleanup offen.
4. ~~**P1.4/P1.6** – `device_id`→`entity_id`, Webhooks~~ ✅ erledigt (P1.4 inkl. #7 ZHA-Remote; alle 5 Webhooks entfernt).
5. ~~**P2.7/P2.8** – Blueprints für Heizkreis-Räume und Anker-Targets~~ ✅ erledigt 2026-08-17.
6. **P2.9** ✅ Konstanten→Helfer erledigt. **P3.11** ✅ Aliase umbenannt (2026-08-17); **P3.12** (dynamische Service-Namen) offen.

> Hinweis: Änderungen an Automationen/Skripten laufen am robustesten über die HA-Config-API
> (validiert beim Schreiben) statt über direkte YAML-Edits. Vor Umbenennungen/Refactorings gilt
> die Impact-Analyse aus `references/safe-refactoring.md` (Consumer prüfen), damit Dashboards,
> Skripte und Config-Entry-Gruppen nicht still brechen.

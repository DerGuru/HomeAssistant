# Chat-Export: Smarter Stellmotor für Fußbodenheizungsventile

**User:** gibt es Stellmotoren für Fußbodenventile, also Fußbodenheizungsventile, die auf eine bestimmte Öffnung festgestellt werden können?

**Assistant:** Ja. Für Fußbodenheizungsverteiler gibt es neben den üblichen thermischen „Auf/Zu“-Stellantrieben auch motorische bzw. modulierende Stellantriebe, die eine definierte Zwischenstellung halten können.

Die üblichen 230-V- oder 24-V-Thermoantriebe, die man auf vielen Heizkreisverteilern sieht, sind dafür allerdings ungeeignet: Die sind im Prinzip langsam „0 oder 100 %“. Mit PWM kann man zwar eine mittlere Heizleistung erzeugen, aber das Ventil steht dabei nicht zuverlässig beispielsweise auf exakt 37 %.

Was du suchst, läuft typischerweise unter Begriffen wie „proportionaler Stellantrieb“, „modulierender Stellantrieb“ oder „0–10-V-Stellantrieb“. Je nach Modell bekommt er z. B. ein 0–10-V-Signal:

0 V → geschlossen  
5 V → etwa 50 % Hub  
10 V → vollständig geöffnet

Der Motor fährt auf diese Position und hält sie dort. Es gibt außerdem Varianten mit 3-Punkt-Ansteuerung („Auf / Stop / Zu“) oder mit Busanbindung, etwa KNX oder Modbus.

Für eine Fußbodenheizung ist dabei ein Detail wichtig: „50 % Ventilhub“ bedeutet nicht unbedingt „50 % Wasserdurchfluss“. Ventilkennlinie, Differenzdruck und hydraulischer Abgleich spielen da stark hinein.

Wenn du das für deine Tecalor-/Home-Assistant-Regelung im Sinn hast, wäre ein 24-V-Stellantrieb mit 0–10 V vermutlich die sauberste Variante. Dann könnte HA tatsächlich beispielsweise „Heizkreis Wohnzimmer = 42 % geöffnet“ vorgeben, statt mit Ein/Aus-Zyklen zu arbeiten.

---

**User:** Ich suche was, dass sich wie ein Shutter steuern lässt. Also Z.B. mit einem Shelly 2 PM.

**Assistant:** Ja — dann suchst du ziemlich konkret einen **3-Punkt-Stellantrieb mit Auf/Zu-Richtung**, also elektrisch eher wie einen Rollladenmotor als wie einen klassischen FBH-Thermoantrieb.

Das Prinzip wäre:

- Leitung 1 bestromen → Ventil fährt auf
- Leitung 2 bestromen → Ventil fährt zu
- keine Leitung bestromt → Motor bleibt auf der aktuellen Position stehen

Genau das kann ein Shelly 2PM im Cover-/Shutter-Modus grundsätzlich gut abbilden: zwei gegeneinander verriegelte Ausgänge für die beiden Fahrtrichtungen und Positionssteuerung über die kalibrierte Laufzeit.

Für dich wäre also ein **230-V-3-Punkt-Stellantrieb** besonders interessant. Dann wäre beispielsweise:

`O1 → AUF`  
`O2 → ZU`  
`N → Neutralleiter`

und der Shelly behandelt das Ganze praktisch wie einen sehr langsamen Rollladen.

Der große Unterschied zum normalen thermischen FBH-Antrieb ist, dass du damit tatsächlich sagen könntest:

> Wohnzimmer 37 %

und der Antrieb fährt ungefähr auf 37 % Hub und bleibt dort, ohne ständig Energie zum Halten der Stellung zu brauchen.

Wichtig ist allerdings die mechanische Seite: Du brauchst einen Antrieb, der auf deine Ventile am Heizkreisverteiler passt, typischerweise z. B. **M30 × 1,5**, und ausdrücklich **3-Punkt / floating / open-close** unterstützt. Nicht jeder motorische 0–10-V-Antrieb kann das.

---

**User:** Genau das suche ich

**Assistant:** Ja — und der Oventrop ist ziemlich genau das, was du beschrieben hast:

Der **Oventrop Aktor M 3P H, Art.-Nr. 1012729** ist elektromotorisch, 230 V, hat einen echten **3‑Punkt-Eingang** und einen **M30×1,5-Anschluss**. Stellweg sind 4 mm, Stellzeit ca. 22 s/mm, also rund 88 Sekunden über den vollen Hub.

Elektrisch passt das Prinzip sehr gut zu einem Shelly 2PM im Cover-Modus:

`N → blau / gemeinsamer N`  
`O1 → braun → eine Fahrtrichtung`  
`O2 → grau → andere Fahrtrichtung`

Der Antrieb bekommt also je nach Richtung Phase auf einen der beiden Steuereingänge. Ohne Ansteuerung bleibt er auf seiner Position stehen.

Damit solltest du nach Kalibrierung tatsächlich so etwas bekommen wie:

**Shelly Cover position = 30 % → Ventilhub ≈ 30 %**

Das ist natürlich zunächst Hubposition, nicht exakt 30 % Volumenstrom. Aber für eine kontinuierliche Regelung einer FBH ist das schon eine erheblich bessere Stellgröße als zeitproportionales Ein-/Ausschalten.

Der Nachteil: **Der Antrieb kostet ungefähr 150–160 € pro Heizkreis.**

---

**User:** Ja bitte suchen

**Assistant:** Das Ergebnis ist leider ziemlich eindeutig: Unter etwa 100 € findet man kaum echte 230-V-3-Punkt-Antriebe mit M30×1,5. Viele Angebote für 10–50 € nennen sich zwar „motorisch“ oder „Regelantrieb“, sind elektrisch aber weiterhin nur NC/NO und damit für die Shelly-Positionsfahrt ungeeignet.

Ein interessanter Kandidat ist der **Siemens SSA31.1**. Das ist ein elektromotorischer 230-V-3-Punkt-Antrieb mit M30×1,5, 100 N Stellkraft und 2,5/5 mm Hub.

Der zweite saubere Kandidat bleibt der **Oventrop Aktor M 3P H** mit 230 V, M30×1,5, 150 N und echter Floating-/3-Punkt-Steuerung.

Weitere passende Geräte sind der **IMI Heimeier EMO 3/230** und der **Danfoss AMV 150**, allerdings ebenfalls nicht günstig.

Die günstigen 10–45-€-Antriebe kann man praktisch alle streichen; sie sind meistens thermisch bzw. NC/NO.

Ein alternativer Weg wäre 24-V-3-Punkt-Antriebe plus Relais oder eine DIY-Lösung.

---

**User:** Wenn ich das mit einem PID Ventil in HA steuern möchte. Macht es dann Sinn?

**Assistant:** Ja, grundsätzlich schon — aber mit einer wichtigen Einschränkung: Für einen PID-Regler in Home Assistant ist ein positionsfähiges Ventil sogar deutlich sinnvoller als ein normales thermisches Auf/Zu-Ventil.

Der PID-Regler liefert typischerweise eine Stellgröße von 0–100 %. Mit einem echten 3-Punkt-Motorantrieb könntest du diese Stellgröße direkt als Ventilposition interpretieren:

30 % PID-Ausgang → Ventil auf etwa 30 % Hub  
65 % → etwa 65 % Hub  
100 % → ganz offen

Für eine Fußbodenheizung ist die Strecke extrem träge. Der PID darf deshalb nicht aggressiv eingestellt sein. Praktisch landet man häufig eher bei einem sehr langsamen PI-Regler.

Zweitens ist Ventilstellung nicht gleich Heizleistung. Bei 50 % Ventilhub bekommst du nicht zwingend 50 % Volumenstrom. Das ist aber kein grundsätzliches Problem, weil der Regler über die Rückkopplung seinen Arbeitspunkt findet.

Mit einem Shelly 2PM als `cover` könntest du die PID-Ausgabe auf `cover.set_cover_position` legen.

---

**User:** Ich habe sowohl Vorlauf als auch Rücklauf direkt von der Heizung gemessen

**Assistant:** Dann wird die Regelung deutlich interessanter, weil du zusätzlich den thermischen Zustand der Anlage kennst.

Mit Vorlauf und Rücklauf kannst du die Spreizung

\[
\Delta T = T_\text{Vorlauf} - T_\text{Rücklauf}
\]

mit einbeziehen.

Für die eigentliche Raumregelung würde ich trotzdem nicht alles in einen einzigen PID werfen. Sinnvoller ist eine Kaskade:

`Raum-Soll/Ist → langsamer PI → gewünschte Ventilposition`

Vorlauf/Rücklauf dienen als zusätzliche Begrenzung oder Plausibilisierung.

Wichtig ist außerdem, **Integrator-Windup** zu vermeiden. Wenn gerade keine Wärme verfügbar ist, sollte der I-Anteil nicht stundenlang weiter auf 100 % hochlaufen.

---

**User:** Und dann kommt als weiterer Haken hinzu, dass die Heizung keinen Pufferspeicher hat und mindestens 10l Durchlauf möchte

**Assistant:** Ja, genau. Damit wird aus einer reinen Raumregelung ein hydraulisch gekoppeltes System.

Wenn die Wärmepumpe **mindestens 10 l/min Volumenstrom** braucht und kein Pufferspeicher hydraulisch entkoppelt, dürfen die Raumregler niemals unabhängig voneinander alle Ventile weit schließen.

Die Summe der Ventilstellungen braucht eine übergeordnete Nebenbedingung.

Sinnvoll wäre:

`Raum-PI → gewünschte Ventilöffnung`

und darüber:

`Hydraulik-Manager → korrigiert alle Ventile so, dass Mindestdurchfluss erhalten bleibt`

Eine echte Volumenstrommessung wäre dafür sehr wertvoll. Alternativ könnten geeignete Referenzkreise immer ausreichend offen bleiben.

---

**User:** In den Ventilen ist eine Volumenskala... voll offen sind 2,2l

**Assistant:** Das hilft sehr. Wenn **ein Kreis voll offen ca. 2,2 l/min** liefert, brauchst du für 10 l/min hydraulisch ungefähr das Äquivalent von **fünf vollständig geöffneten Kreisen**:

\[
10 / 2{,}2 \approx 4{,}55
\]

Als erste Näherung könntest du also fordern:

\[
\sum \text{Ventilpositionen} \ge 455\%
\]

wenn alle Kreise identisch wären.

Aber Ventilposition und Volumenstrom sind nicht linear. Genau da ist deine Volumenskala nützlich. Du könntest eine Kennlinie aufnehmen, z. B.:

`100 % → 2,2 l/min`  
`75 % → ?`  
`50 % → ?`  
`25 % → ?`

Dann kann HA statt Prozentwerten einen geschätzten Volumenstrom berechnen.

---

**User:** Und das nur, weil es keinen Pufferspeicher gibt :( Soll ja auch Vorteile haben, aber der Nachteil ist immens

**Assistant:** Ja, genau das ist der Trade-off bei einer direkt angebundenen Wärmepumpe ohne Pufferspeicher.

Vorteile: weniger Speicherverlust, keine zusätzliche Pumpe, geringere Vorlauftemperaturen möglich, oft besserer COP.

Nachteil: Die Fußbodenheizung selbst wird zum hydraulischen Puffer. Einzelraumregelung und Mindestvolumenstrom können gegeneinander arbeiten.

Drei Strategien wären:

1. einige große Heizkreise immer offen lassen,
2. modulierende Ventile plus zentrale Mindestdurchflusslogik,
3. hydraulische Entkopplung nachrüsten.

Für deine HA-Idee ist Variante 2 technisch elegant.

---

**User:** nur die Kosten sind echt hoch.... gibts da nichts als DIY?

**Assistant:** Ja, DIY ist wahrscheinlich sinnvoll.

Die Lösung wäre:

`M30×1,5 Adapter → kleine Spindel → Stepper → Ventilstift`

Ein kleiner Stepper mit Spindel, ESP32 und Treiber könnte die Position direkt anfahren.

Preislich könnte man ungefähr bei **15–30 € pro Ventil** landen statt 150 €.

Eine Alternative wäre ein 12/24-V-Getriebemotor mit Endschaltern. Technisch sauberer wäre aber ein Stepper.

---

**User:** Wenn da ein ESP32 dran ist, brauche ich eh ein USBC Netzteil entweder von 24V oder von 230V gibts die Stepper auch mit USB Strom?

**Assistant:** Ja, **5-V-Stepper gibt es**, zum Beispiel den 28BYJ-48. Der wäre für einen ersten Versuch interessant, ist aber mechanisch eher knapp und hat Kunststoffgetriebe.

Für einen richtigen kleinen Stepper wäre sauberer:

`230 V → gemeinsames 12/24-V-Netzteil`

und daraus:

`12/24 V → Steppertreiber → Stepper`  
`12/24 V → Buck → 5 V → ESP32`

Dann braucht nicht jeder ESP ein eigenes USB-Netzteil.

---

**User:** ich würde das gerne als gesamtkonstruktionen behandeln... also ein immer nur einen stepper mit allem, was er braucht, wenn man das gut macht, kann man das vielleicht sogar verkaufen

**Assistant:** Dann sollte das als eigenständiger **Smart Proportional Actuator** gedacht werden:

**M30×1,5 anschrauben → Versorgung anschließen → Funk einrichten → kalibriert sich → Home Assistant sieht ein Ventil 0–100 %.**

Hardware ungefähr:

`Versorgung → ESP32 → Stepper-Treiber → kleiner Stepper → Spindel → federnder Ventilstößel`

Wichtig wären automatische Kalibrierung, persistente Speicherung und lokale Funktion ohne Cloud.

---

**User:** dann leiber gleich einen richtigen stepper nehmen

**Assistant:** Ja. Für einen ernsthaften Prototypen würde ich direkt einen **bipolaren Stepper** nehmen, z. B. NEMA 8 oder NEMA 11, zusammen mit einem TMC2209.

Mit einer feinen Spindel kann der Motor klein bleiben. Die Bewegung darf langsam sein, weil die FBH ohnehin träge ist.

Ein federnder Druckstößel wäre sinnvoll, damit mechanische Anschläge nicht brutal gegen das Ventil drücken.

---

**User:** mach mir mal einen Plan. Was brache ich alles und wie muss es zusammengesetzt werden

**Assistant:** Zielarchitektur:

```text
             24 V DC
                │
        ┌───────┴────────┐
        │ Ventilantrieb  │
        │                │
        │  DC/DC 3,3 V   │
        │      │         │
        │  ESP32-C3      │
        │      │ UART    │
        │   TMC2209      │
        │      │         │
        │ NEMA-11        │
        │      │         │
        │ Gewindespindel │
        │      │         │
        │ Druckstößel    │
        └──────┬─────────┘
               │
            M30×1,5
               │
          FBH-Ventil
```

Mechanik:

```text
Stepper
  │
Motorwelle
  ▼
Kupplung
  │
Spindel
  │
bewegliche Spindelmutter
  │
federnder Stößel
  │
Ventilstift
```

Für V1: NEMA 11, etwa 0,08–0,12 Nm, feine Spindel um 0,5–1 mm Steigung.

Die Spindelmutter wird axial geführt, sodass sie sich nicht mitdreht.

Ein federnder Stößel dient als Kraftbegrenzung und Toleranzausgleich.

M30×1,5 unten als austauschbarer Adapter.

Elektronik:

- ESP32
- TMC2209
- 24 V Eingang
- Buck-Regler
- Hall-Sensor
- Status-LED
- Taster

Selbstkalibrierung:

1. vollständig zurückfahren,
2. Referenz finden,
3. Richtung Ventil fahren,
4. Kontakt erkennen,
5. bis zum geschlossenen Anschlag fahren,
6. Hub speichern.

Für V1 erst Mechanik, dann Positionierung, dann Hydraulik, dann HA, dann PID/Mindestdurchfluss.

---

**User:** Im ESP sollten dann noch die etsprechenden Durchflüsse bei der jeweiligen Ventilöffnung hinterlegt werden können. Am besten aus HA heraus

**Assistant:** Ja. Das würde ich als festen Bestandteil des Aktors vorsehen.

Im ESP könnte eine Kennlinie liegen:

| Ventilöffnung | Durchfluss |
|---:|---:|
| 0 % | 0,00 l/min |
| 10 % | 0,05 l/min |
| 20 % | 0,20 l/min |
| … | … |
| 100 % | 2,20 l/min |

Zwischen den Stützstellen interpoliert der ESP.

Noch besser: Der Aktor kann in beide Richtungen rechnen.

HA sagt entweder:

`Ventilposition = 47 %`

oder besser:

`Soll-Durchfluss = 0,85 l/min`

Der ESP sucht dazu selbst die passende Ventilposition.

Kalibrierwerte können als `number`-Entities in HA erscheinen und persistent im ESP gespeichert werden.

---

**User:** Und dann rechnet man in HA in Litern Durchfluss und der ESP übersetzt es dann in die entsprechende Position

**Assistant:** Genau. Das ist die sauberste Architektur.

HA arbeitet mit:

`Soll-Durchfluss = 0,9 l/min`

Der ESP kennt seine Kennlinie und übersetzt intern:

`0,9 l/min → 42 % Ventilöffnung`

Damit bleibt die Heizlogik in HA hydraulisch verständlich.

---

**User:** Die Ventil-Position ist dann nur noch Anzeige in HA

**Assistant:** Genau.

Primäre Stellgröße in HA:

`number.wohnzimmer_soll_durchfluss = 1,2 l/min`

Der ESP übersetzt das intern in die nötige Position.

Die Ventilposition ist nur Telemetrie:

`sensor.wohnzimmer_ventilposition = 47 %`

---

**User:** Und dann kommt nach dem WLAN einrichten und mit HA verbinden eine Kalibrierung

**Assistant:** Genau. Erststart:

1. Strom an.
2. Funk einrichten.
3. Gerät in HA einbinden.
4. Aktor ist zunächst „nicht kalibriert“.
5. mechanische Kalibrierung.
6. hydraulische Kalibrierung.
7. Kennlinie persistent speichern.

Die hydraulische Kalibrierung kann geführt in HA erfolgen: Ventil fährt auf definierte Position, Nutzer liest den Durchfluss ab und trägt ihn ein.

---

**User:** Gibts das auch als Zibgee?

**Assistant:** Ja. Zigbee ist für das Konzept sogar sehr attraktiv.

Statt ESP32-C3 könnte man einen **ESP32-C6** nehmen. Der unterstützt IEEE 802.15.4 und damit Zigbee/Thread.

Der Aktor wäre dann z. B.:

`HA Soll-Durchfluss → Zigbee → Aktor → Kennlinie → Stepperposition`

24-V-versorgte Geräte könnten als Zigbee Router arbeiten.

Für Spezialwerte wie `target_flow` wären herstellerspezifische Zigbee-Attribute nötig.

---

**User:** das gibt es für Zigbee fertig?

**Assistant:** Teilweise, aber nicht in genau dieser Form.

Es gibt fertige Zigbee-Thermostat-/FBH-Aktoren, aber die günstigen sind meist nur smartes Auf/Zu.

Proportionale 0–10-V-Antriebe gibt es ebenfalls, aber meist ohne Zigbee.

Die Kombination:

**M30×1,5 + echter proportionaler Motor/Stepper + Zigbee + frei anfahrbare Position + direkter Durchflusssollwert**

ist nicht als übliches Standardprodukt von der Stange verbreitet.

---

**User:** Okay ... dann mal eine Einkaufsliste mit Zigbee

**Assistant:** Für einen ersten Zigbee-Prototypen:

| Teil | Empfehlung |
|---|---|
| MCU/Funk | ESP32-C6-DevKitM-1 |
| Steppertreiber | TMC2209 |
| Stepper | NEMA 11, ca. 0,08–0,12 Nm |
| Spindel | ca. 5 mm, 0,5–1 mm Steigung |
| Spindelmutter | passend |
| Kupplung | Motorwelle → Spindel |
| Druckfeder | für axialen Federweg |
| Druckstößel | Stahl/Messing |
| Hall-Sensor | Referenzposition |
| Magnet | Neodym |
| Buck-Wandler | 24 → 5 V |
| Netzteil | 24 V DC |
| M30×1,5-Aufnahme | Ventilmontage |
| Gehäuse | 3D-Druck |

Elektrisch:

```text
24 V
 ├── TMC2209 ── NEMA11
 │
 └── Buck 24→5 V ── ESP32-C6
                       │
                       ├── STEP
                       ├── DIR
                       ├── ENABLE
                       ├── UART
                       └── Hall
```

---

**User:** Und Zigbee + Matter/Thread? Wobei ich mir mit Matter wahrscheinlich realtiv viel eintrete

**Assistant:** Der ESP32-C6 ist hardwareseitig geeignet für Zigbee und Thread/Matter.

Ich würde aber für V1 nur Zigbee implementieren.

Matter bringt zusätzlichen Aufwand: Commissioning, Fabrics, Zertifikate, Device Types, Cluster, Interoperabilität und Zertifizierung.

Für unser spezielles `target_flow`-Modell ist Zigbee mit herstellerspezifischen Attributen deutlich unkomplizierter.

Hardware kann trotzdem so gewählt werden, dass später eine Matter/Thread-Firmware möglich ist.

---

**User:** Okay ... dann noch mal die Einkaufsliste für Zigbee

**Assistant:** Kern-BOM:

- ESP32-C6-DevKitM-1
- TMC2209
- NEMA 11 0,08–0,12 Nm
- feine Spindel 0,5–1 mm Lead
- Spindelmutter
- Wellenkupplung
- Druckfeder
- Ventilstößel
- Hall-Sensor + Magnet
- 24→5-V-Buck
- 24-V-Netzteil
- M30×1,5-Aufnahme
- 3D-Druck-Gehäuse
- Kleinteile

---

**User:** ja bitte

**Assistant:** Konkrete V1-BOM:

- ESP32-C6-DevKitM-1-N4
- BIGTREETECH TMC2209 v1.3
- Joy-it NEMA11-02, 0,12 Nm
- 24→5-V-Buck
- A3144 Hall-Sensor
- 5→5-mm-Wellenkupplung
- Tr5×1 bzw. 5-mm-Spindel mit ca. 1 mm Lead
- passende Mutter
- Druckfeder
- M30×1,5-Aufnahme
- 24-V-Netzteil

Für den Prototypen ist NEMA11 bewusst überdimensioniert. Später kann kleiner optimiert werden.

---

**User:** geht esphome über zigbee?

**Assistant:** Ja. ESPHome hat inzwischen native Zigbee-Unterstützung für entsprechende ESP32-Varianten wie C6/H2.

Für unser Gerät können Standard-Entities direkt exponiert werden. Für Spezialwerte wie Kalibriertabelle und Durchflusssollwert wird wahrscheinlich Custom-Code oder eine eigene Zigbee-Abbildung nötig.

---

**User:** zha

**Assistant:** Für dich würde ich klar **ZHA** anpeilen.

Strategie:

`ZHA + Standard-Zigbee-Cluster wo möglich`

und herstellerspezifische Attribute nur dort, wo nötig.

Zum Beispiel:

- `valve_position`
- `target_flow`
- `estimated_flow`
- `calibration_state`
- Kalibrierpunkte

Komplexere proprietäre Attribute können über einen **ZHA Quirk / Device Handler** in HA-Entities übersetzt werden.

---

**User:** Naja... man kann dafür vielleicht sogar eine eigene Integration bauen? Geht das auch mit Zigbee?

**Assistant:** Ja.

Die Funk-/Geräteebene bleibt bei **ZHA**. Eine eigene Home-Assistant-Integration kann darüber Komfortfunktionen bereitstellen.

Architektur:

```text
Smart Actuator
      │
    Zigbee
      │
     ZHA
      │
   ZHA Quirk
      │
Home-Assistant-Entities
      │
eigene "Smart FBH"-Integration
```

Die Integration könnte Kalibrierassistent, Kennlinienprüfung, Gruppenübersicht und Komfortfunktionen bereitstellen.

---

**User:** Naja... das Setup sollte dann über die Integration laufen... klar kann man auch dran vorbei arbeiten, aber es macht die Sache einfacher.
Alternativ kann man das Setup über WLAN und eine WebPage machen, dann kommt aber noch ein WebServer auf den ESP

**Assistant:** Ich würde den Einrichtungsweg komplett in Home Assistant verlagern und den Aktor selbst bewusst klein halten.

Der ESP macht lokal:

- Motorsteuerung
- Sicherheitslogik
- persistente Kalibrierwerte
- Kennlinie l/min → Position
- Zigbee

Die HA-Integration macht:

- Onboarding
- mechanische Kalibrierung starten
- hydraulische Kalibrierung
- Messwerte prüfen
- Kennlinie berechnen
- Kennlinie in den Aktor schreiben

Damit braucht der Aktor keinen Webserver.

---

**User:** Kann man bei der Integration den quirk mit installieren lassen?

**Assistant:** Ja, grundsätzlich.

Eine Custom Integration kann beim Setup prüfen, ob der benötigte Quirk vorhanden ist, und ihn in einen Custom-Quirk-Pfad legen. Langfristig wäre es sauberer, den Quirk upstream in `zha-device-handlers` zu bekommen.

Für Entwicklung/Early Adopter wäre ein Flow denkbar:

`Integration installieren → Quirk bereitstellen → Neustart → Aktor anlernen → Kalibrierassistent`

---

**User:** Genau darum geht es. Komfort Funktionen und Kalibrierung. Mehr muss die Integration gar nicht mitbringen. Oder siehst du da noch mehr?

**Assistant:** Ich würde sie bewusst schlank halten.

Sinnvolle Aufgaben:

- geführtes Onboarding
- mechanische Kalibrierung
- hydraulische Kalibrierung
- Plausibilitätsprüfung
- Kennlinie berechnen/glätten
- Heizkreis benennen
- Soll-Durchfluss bereitstellen
- Ventilposition und geschätzten Durchfluss anzeigen
- Re-Kalibrierung
- Diagnose
- optional Gruppenübersicht

PID, Mindestdurchflusslogik und Heizungsstrategie würde ich nicht in die Geräteintegration packen.

---

**User:** Wie kann ich den maximalen Hub des Ventils herausbekommen? Federkontakt am Stösel?

**Assistant:** Ja. Ein Federkontakt am Stößel ist dafür sehr sinnvoll.

Ablauf:

1. Aktor fährt zurück und findet Referenz.
2. Er fährt Richtung Ventil.
3. Sobald der federnde Stößel Kontakt bekommt, wird der offene Endpunkt erkannt.
4. Weiterfahren.
5. Wenn der Ventilstift nicht weiter kann, steigt die Federkompression.
6. Das ist der geschlossene Endpunkt.
7. Differenz der Schritte = tatsächlicher Ventilhub.

Ein linearer Hall-Sensor wäre dafür eine elegante kontaktlose Variante.

---

**User:** Oder zwei Federn. Eine kleine, die offen ist, wenn noch kein Kontakt ist. Bei Kontakt drückt sie sich zusammen und schließt Strom -> Maximal offen erkannt. Zweite Feder stärker, schließt wenn der stösel nicht weiter kommt. -> vollständiges schließen des Ventils erkannt.

Schritte dazwischen 0-100%, zurück dann die Kalibrierung zu Öffnungsgrad und Durchfluss. In 5% Happen (oder reichen 10er Schritte?)

**Assistant:** Ja — die Zwei-Feder-Idee ist für einen echten Aktor sogar sehr interessant.

Mechanisch:

```text
Stepper / Spindel
       │
       ▼
   Hauptschlitten
       │
   [Feder 2]      ← deutlich stärker
       │
   Zwischenstößel
       │
   [Feder 1]      ← sehr weich
       │
       ▼
   Ventilstift
```

Ablauf:

1. Stößel fährt frei.
2. Stößel berührt Ventilstift.
3. Feder 1 komprimiert sich und Kontakt 1 schaltet.
4. Das ist **100 % offen**.
5. Weiterfahren.
6. Ventil bewegt sich.
7. Ventil erreicht Sitz.
8. Feder 2 komprimiert sich.
9. Kontakt 2 schaltet.
10. Das ist **0 % offen**.

Alles dazwischen wird über die Schrittzahl auf 0–100 % normiert.

Die Federn selbst würde ich nicht als elektrische Kontaktflächen verwenden, sondern mit Mikroschaltern oder Hall-Sensoren erfassen.

Für die hydraulische Kalibrierung würde ich **10-%-Schritte als Standard** nehmen. Das sind 11 Messpunkte. 5-%-Schritte würde ich optional als Feinkalibrierung anbieten.

Noch besser wäre adaptive Kalibrierung: erst 10 %, dann zusätzliche 5-%-Messpunkte nur in stark nichtlinearen Bereichen.

Wichtig: Die Kennlinie `Ventilöffnung → l/min` hängt auch vom Differenzdruck des Systems ab. Für die harte Mindestdurchflussgrenze sollte deshalb Sicherheitsreserve eingeplant werden.

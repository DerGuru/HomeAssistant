# Setup
Wir haben eine Fussbodenheizung mit zwei zusätzlichen Bad-Wand-Heizkörpern und fahren einen Heiz- und einen Absenkbetrieb. 
Die Heizung ist innengeführt über die Wohnküche und damit auch die beiden Flure im EG und OG, da hier alles offen ist.

## Räume
Alle Räume haben Fussbodenheizung.
| Etage | Raumname | Größe in m²| Durchgang offen | verbunden mit (Etage - Raum) | Durchfluss l/min | dauerhaft offen |
|-------|----------|------------|-------|------------------------------|------------------|-----------------|
| EG    | Flur     | 11,34 | ja | OG - Flur | 0,75  | ja |
| EG    | Bad      | 5,28 | nein | EG - Flur | 4 | ja |
| EG    | Büro     | 8,79 | ja | EG - Flur | 1,0 | nein |
| EG    | Wohnzimmer/-küche | 44,92 | ja | EG - Flur | 4 | ja |
| OG    | Flur     | 7,35 | ja | EG - Flur | 0 | nein |
| OG    | Bad      | 12,89 | nein | OG - Flur | 4 | ja |
| OG    | Kinderzimmer | 14,50 | nein | OG - Flur | 4 | nein |
| OG    | Büro     | 12,43 | nein | OG - Flur | 4 | nein |
| OG    | Schlafzimmer + Ankleide | 21,47 (13,78 + 7,69) | ja | Schlafzimmer ↔ Ankleide (Mauerdurchbruch) | 3 (2 + 1) | nein |

## Die Heizung
Es ist eine Tecalor TTF 7 cool (Baujahr 2012/2013)  mit einer FEK verbaut, die in der Wohnküche angebracht ist.\
Wir haben keinen Pufferspeicher - dadurch muss immer ein Mindestdurchfluss gegeben sein. Laut Datenblatt sind das 0,64 m³/h ≈ 10,67 l/min (Wasserseite). Dieser Wert enthält bereits einen Sicherheitspuffer – solange er nicht unterschritten wird, ist alles in Ordnung. Laut einem Tecalor-Techniker funktionieren 8 l/min noch als absolutes Minimum. 

Gekühlt wird nur passiv (ohne Verdichter), dort ist der Mindestdurchfluss unkritisch. Im ungünstigsten Fall im Kühlbetrieb (Bad OG zu, alle Thermostat-Räume wegen offener Fenster zu): 8,75 l/min – knapp über dem absoluten Minimum, hat im Sommer 2026 problemlos funktioniert. \
Folgende Räume sind dauerhaft offen: 
- EG - Bad
- EG - Wohnzimmer mit Wohnküche
- EG - Flur
- OG - Bad (beim heizen, im Kühlbetrieb geschlossen)

Die übrigen Räume (Büro EG, Kinderzimmer, Büro OG, Schlafzimmer + Ankleide) werden über Thermostate gesteuert. Die Umschaltung zwischen Heiz- und Kühlbetrieb läuft automatisch über Home Assistant (siehe [Smart Home](#smart-home)). Im Kühlbetrieb wird nur das Bad OG geschlossen, das Bad EG bleibt offen.

### Technische Spezifikationen
#### Wärmepumpe 
| Merkmal | Ausprägung |
|-|-|
| Kältemittel | R410A |
| PS (HD) | 4,3 MPa |
| Wärmequelle | Sole (B) |

#### Volumina und Drücke
| Merkmal | Sole | Wasser |
| ------- | ---- | --------------- |
| Volumenstrom (min) | 1,9m³/h | 0,64m³/h |
| Ext. stat. Druckdifferenz | 600 hPa | 350 hPa |
| Zulässiger Überdruck | 0,3 MPa | 0,3MPa |
| Einsatzgrenze (min) | -5 °C| 15 °C | 
| Einsatzgrenze (max) | 20 °C | 60 °C |

| Merkmal | Wärmeleistung (kW) | Leistungsaufnahme (kW) | Leistungszahl (COP) |
|-|-|-|-|
| Betriebspunkt | B 0 | B 0 | B 0 |
| Vorlauf W35   | 7,40 | 1,68 | 4,39 |
| Vorlauf W55 | 6,47 | 2,68 | 2,41 |

| Merkmal | Anschluss | Absicherung | Leistungsaufnahme (max) |
|-|-|-|-|
| Verdichter | 3/PE~ 400V 50 Hz | 3x 16 A | 3 kW |
| Zusatzheizung (DHC) | 3/N/PE~ 400V 50Hz  | 3x 16 A | 8,8 kW |
| Steuerung | 1/N/PE~ 230V 50 Hz | 1x 16 A | 0,5 kW |
| Anlaufstrom / LRA | 25 A / 38 A |  
| Schutzart | IP 20 |

#### Zusatzheizung (DHC)
| Anschlussleistung | K5 | K6 | K7 |  |  | 
|-|-|-|-|-|-|
| 2,6 kW | L1 |    |    | N | PE |
| 3,0 kW |    | L2 |    | N | PE |
| 3,2 kW |    |    | L3 | N | PE |
| 5,6 kW | L1 | L2 |    | N | PE |
| 5,8 kW | L1 |    | L3 | N | PE |
| 6,2 kW |    | L2 | L3 | N | PE |
| 8,8 kW | L1 | L2 | L3 | N | PE |

#### Warmwasserspeicher
| Merkmal | Ausprägung |
|-|-|
| Nenninhalt | 175 l |
| Zulässiger Betriebsüberdruck | 1 MPa |
| Prüfüberdruck | 1,5 MPa |
| Zulässige Betriebstemperatur | 95 °C |
| Wärmetauscher-Fläche | 2,1 m² |
| Bereitschaftsenerieverluste | 1,9 kWh / 24 h |
| Behälterwektstoff | St em |

## Prämisse: 
Ich bin faul und möchte so wenig wie möglich an der Heizung etwas einstellen müssen.

## Zielbild: 
1. Morgens und Abends ein warmes Bad mit einem warmen Fussboden.
2. Morgens und Abends heisses Wasser zum Duschen / für ein Vollbad.
3. Tagsüber einen Temperturkorridor von 21,5 °C - 23,5 °C, morgens und abends gerne ein wenig wärmer.
4. Ich versuche eine Automatikeinstellung zu finden, die man im Idealfall nie wieder anfassen muss. Ich verzichte dafür auf ein wenig Heizeffizienz und benötige mehr Strom.

## Sonstiges
Montags bis freitags wird das Bad im OG ab 7:45 Uhr für die Morgentoilette unserer Tochter (geb. 18.04.2021)  - also Waschen, anziehen, Zähneputzen - benutzt.\
Ich dusche dann in der Regel erst zwischen 09:00 - 09:30.\
Am Wochenende ist es schwerer einschätzbar. Aber normalerweise wird sich im Bad nicht vor 9:00 Uhr aus-/umgezogen - wenn man vorher nur mal eben auf Toilette muss, muss der Boden und der Raum noch nicht so warm sein.

# Einstellungen an der Heizung und an der FEK

## Heizen
Der Heizbetrieb ist dafür da, um die Bäder vor dem duschen oder Baden am Morgen oder Abend noch mal hochzuheizen.\
Ausserdem fröstelt man abends schneller und morgens friere ich IMMER, wenn ich aus dem Bett komme.

### Zieltemperaturen
Heizbetrieb: 22,5 °C\
Absenkbetrieb: 22,0 °C

### Regelzeiten für den Heizbetrieb
#### Mo - Fr 
1. 6:00 - 9:00 
2. 17:30 - 21:00

#### Sa & So
1. 6:00-11:00
2. 17:30-21:00

## Warmwasser
Wir duschen in der Regel morgens zwischen 9:00 und 10:00 Uhr.\
Am Abend duscht unsere Tochter noch mal kurz gegen 20:00 - 21:00 und eventuell lässt sich meine Frau mal ein Vollbad ein. Insbesondere im Winter macht sie das gerne mal.

Hier ist der Heizbetrieb quasi ein Ersatz für die Anti-Legionellen-Funktion der Heizung, da ich es täglich weder nötig noch sinnvoll noch bezahlbar finde. Die einzige sinnvolle automatisierte Möglichkeit bleibt deshalb das wöchentliche WW-Heizfenster am Montagmorgen (siehe Regelzeiten) - in dem hoffentlich niemand Wasser nimmt.

Wir haben keine Zirkulation im WW-Kreis. Wenn der Hahn geöffnet wird, dann läuft erst mal einen Moment kaltes Wasser.

### Sollwerte
Der WW-Sollwert wird **dynamisch aus Home Assistant** gesetzt (Details unter „Sollwert-Steuerung über Home Assistant“). Aktuell **~50 °C im Betrieb mit 6 K Hysterese** (reheizt ab ~44 °C).

### Regelzeiten (FEK)
Mo 03:00 - 4:30

### Sollwert-Steuerung über Home Assistant
Seit August 2026 gibt es eine zusätzliche Steuerungsebene in Home Assistant, die die **Sollwerte** der Warmwasserbereitung dynamisch anpasst – die FEK-Zeitfenster selbst (siehe Regelzeiten) bleiben unverändert bestehen.

#### Indirektion über zwei Helfer

Statt Automationen direkt auf die drei Sollwert-Entities (`number.heizung_speichersolltemp`, `number.heizung_ww_komf_temp`, `number.heizung_ww_eco_temp`) schreiben zu lassen, gibt es zwei `input_number`-Helfer:

- **`input_number.default_water_temp`** („Default Water Temp“): der manuell gepflegte Normalwert (Startwert 46 °C, aktuell ~50 °C).
- **`input_number.currently_set_water_temp`** („Currently Set Water Temp“): der gerade aktive Sollwert.

Eine einzige Automation (`Heizung – WW-Solltemperatur übernehmen`) beobachtet `currently_set_water_temp` und überträgt jede Änderung per `number.set_value` auf alle drei realen Entities. Das ist die **einzige** Stelle, die die drei Hardware-Entities noch direkt anfasst – alle anderen Automationen/Skripte schreiben nur noch den Helferwert.

Beide Helfer sind auf **35–60 °C** begrenzt (Schnittmenge der drei Ziel-Entities; `heizung_speichersolltemp` hat ein hartes Minimum von 35 °C, das Home Assistant beim Überschreiten mit einem Fehler quittiert statt den Wert still zu kappen).

#### Anwesenheitssteuerung

Die Automation `Heizung – Warmwasser Anwesenheit` reagiert auf die Presence-Gruppe `group.alleda` (Anzeigename „JemandDa“, technische ID unverändert `group.alleda`):

- **Niemand da** (Gruppe → `off`): `currently_set_water_temp` wird auf **35 °C** gesetzt.
- **Jemand da** (Gruppe → `on`): `currently_set_water_temp` wird auf den Wert von `default_water_temp` zurückgesetzt.

#### Legionellenprogramm

`script.legionellenprogramm_warmwasser` hebt `currently_set_water_temp` auf `LegioTemp + LegioHyst` (aktuell 59 + 1 = 60 °C), wartet bis der Speicher (`sensor.heizung_speicheristtemp`) mindestens 59 °C erreicht (Timeout 1 h), hält danach 30 Minuten und setzt `currently_set_water_temp` anschließend wieder auf `default_water_temp` zurück. Das Skript hat **aktuell keinen automatischen Trigger** (keine Automation ruft es auf) – es muss manuell gestartet werden (z. B. über ein Dashboard oder die Skript-Übersicht).

## Einstellungen an der FEK
### Heizkurve 
0,30

Damit kamen wir gut durch zwei Winter. Der Wert sollte also ausreichend sein. Falls der Boden nicht warm genug wird, kann ich den immer noch auf 0,40 erhöhen. Ursprünglich stand der mal auf 0,60. 

### Fachmann
#### Korrektur
-0,3 
Dieser Wert ist empirisch ermittelt worden, indem die Anzeige auf dem FEK-Display mit unterschiedlichen anderen Thermostaten im gleichen Raum gemittelt verglichen wurde.

#### Raumeinfluss
01

## Einstellungen im Menü Inbetriebnahme

Ziel ist hier auch gewesen, dass ich es einmal einstelle und dann hoffentlich NIE WIEDER anfassen muss.

### Kühlbetrieb
ein
#### Fläche
ein
#### Raum soll 
23,0 °C
#### Vorlauf 
15 °C
#### Hysterese
1,0 °C 
Enger Korridor von 22-23 °C.
#### Dynamik
10

### Sommerbetrieb 
ein
#### Gebäudeart
1
#### Außentemperatur
20 °C

### Pumpen Zyklen
aus

### Dauerlauf Pumpe 
ein

### Rücklauf Max 
50 °C

### Vorlauf Max Heizung 
60 °C

### Druck HD Bar
38,5 bar 

Der Druck wurde von einem Tecalor Techniker empfohlen und *sollte* nicht übeschritten werden. Ein Test zeigte, dass die erreichbaren Temperaturen auch bei 40 bar kaum höher werden. Also kann man im Sinne des Sicherheitspuffers und der Langlebigkeit den Wert auch niedrig halten.

### Frostschutz
4 °C.

### Grenze Heizung 
aus

### Bivalenz Heizung
-20 °C

### Grenze WW
aus

### Bivalenz WW
40 °C 

Bewusst so eingestellt. Der Wert ist laut Handbuch eine **Außentemperatur** (Bereich -20 °C bis 30 °C, Werkseinstellung -20 °C): darunter schaltet die Zusatzheizung (DHC) bei der Warmwasserbereitung lastabhängig zu. Mit 40 °C ist das also **immer** der Fall.

Grund: Komfort beim Vollbad. Wegen der Stillstandzeit (20 min) kann der Verdichter während eines langen Wasserbezugs nicht sofort wieder anlaufen – ohne Zusatzheizung kam am Ende des Vollbads nur noch lauwarmes Wasser. Hier tausche ich bewusst Geld gegen Komfort (und Frieden).

Gemessen (Oktober 2026): Jede WW-Ladung schaltet die DHC-Stufen 1 → 2 → 3 im 2-Minuten-Takt zu, der Verdichter läuft nur die ersten ~4–13 Minuten mit, danach heizt allein die DHC mit ~9 kW. Mehrkosten gegenüber reinem Verdichterbetrieb grob 600–900 kWh/Jahr (~20 €/Monat).

Nachverfolgung in Home Assistant über `sensor.wp_energie_warmwasser`, `sensor.wp_energie_heizen`, `sensor.wp_energie_standby` und `sensor.wp_energie_heizstab_aktiv` (seit 16.10.2026).

### WW-ECO
aus 

### WW Hysterese 
6 °C
Darf kühlen bis 44 °C, bevor neu geheizt wird. Das ist so, damit die Heizung effizient arbeiten kann, länger läuft und nicht ständig ein- bzw. ausschaltet.

### Warmwasserkorrektur 
3 °C

### Anti Legionellen
aus

### Regler Dynamik 
30

### Stillstand Zeit
20

### Einphasig
OFF


# Smart Home

Durch den hydraulischen Abgleich werden die Regler im EG praktisch nicht mehr benötigt.  
Die Heizung fährt dort einfach „durch“, alle Kreise außer dem Arbeitszimmer EG sind dauerhaft offen.

Im OG (Bad OG, Schlafzimmer + Ankleide, Arbeitszimmer OG, Kinderzimmer) und im Arbeitszimmer EG schaltet je ein Sonoff-Zigbee-Relais (ZBMINI-R2) den Stellmotor des Heizkreises.  
Die Stellmotoren für die Ventile arbeiten nach dem Prinzip: **Strom = Ventil offen**.

---

## Heiz-/Kühlerkennung

Ein ESP32 mit einem CAN-Bus Shield liest den im Heiz- oder Kühlbetrieb direkt aus der Heizung aus und stellt die Daten über ESPHOME dem Homeassistant zur Verfügung.

Kühlen wird dabei aber nur aktiviert, wenn tatsächlich kaltes Wasser in den Wärmetauscher fließt.
Statt dessen verwende ich zusätzlich die Zieltemperatur (SOLL) des Rücklaufs für die Umschaltlogik des Heiz-/Kühlbetriebs der Ventile.

In Home Assistant gibt es dafür einen Template-Sensor mit zwei Zuständen:

- `"Cooling"` – Kühlbetrieb  
- `"Heating"` – Heizbetrieb  

### Template-Sensor `sensor.heizungsbetriebsmodus`

Grundprinzip: Lässt sich Heizen/Kühlen gerade nicht sauber bestimmen – Warmwasserbereitung läuft (`binary_sensor.heizung_warmwasserbereitung`) oder der Programmschalter steht auf `Warmwasser`/`Bereitschaft`/`Notbetrieb` –, hält der Sensor seinen letzten Wert (Fallback `Heating`, „im Zweifel heizen“). Sonst wird er frisch aus Kühlbetrieb-Signal und Rücklauf-Soll berechnet.

```YAML
{% set p = states('select.heizung_programmschalter') %}
{% set kein_kuehlen = p in ['Warmwasser', 'Bereitschaft', 'Notbetrieb'] %}
{% set ww_aktiv = is_state('binary_sensor.heizung_warmwasserbereitung', 'on') %}
{% if kein_kuehlen or ww_aktiv %}
  {{ this.state if this.state not in ['unknown','unavailable',none] else 'Heating' }}
{% else %}
  {% set kuehlbetrieb = is_state('binary_sensor.heizung_kuehlbetrieb', 'on') %}
  {% set ruecklauf_soll = states('sensor.heizung_ruecklaufsolltemp') | float(99) %}
  {% if kuehlbetrieb or ruecklauf_soll <= 6 %}
    Cooling
  {% else %}
    Heating
  {% endif %}
{% endif %}
```

Der Fallback `ruecklauf_soll <= 6` hält den Kühlbetrieb stabil, wenn `kuehlbetrieb` kurz auf `off` geht, der Rücklauf-Soll aber bei ~5 °C bleibt – sonst würden die Ventile hin- und herschalten.

---

## Automatische Umschaltung Heizen/Kühlen (OG + Arbeitszimmer EG)

Im EG läuft nur das **Arbeitszimmer EG** nicht hydraulisch „fix“ mit – es wird genauso gesteuert wie die OG-Räume.

Insgesamt sind fünf **SONOFF ZIGBEE RELAIS** (ZBMINI-R2) verbaut, die die Stellmotoren für:

- Bad OG  
- Schlafzimmer OG  + Ankleide  
- Arbeitszimmer OG  
- Kinderzimmer OG  
- Arbeitszimmer EG  

entsprechend dem **Heizungsbetriebsmodus** und den jeweiligen Raumthermostaten schalten.

### Fixierung der Thermostate auf **Kühlmodus!**
Die Motorsteuerung der Raumthermostate aus den Zimmern sind jeweils mit dem Eingang (S) des zugehörigen Smartrelais verbunden. Im Heizbetrieb geschieht das als Normal OFF -> Thermostat meldet Bedarf und das Relais gibt den Bedarf weiter an den Stellmotor.

Im Kühlbetrieb werden die Relais **detached** geschaltet, und die Stellmotoren auf dauerhaft an geschaltet.

Es gibt noch eine Fensterschaltung, die bei geöffnetem Fenster im Heizmodus das Thermostat auf ausschaltet. Der eingebaute Frostwächter des Thermostat meldet bei <= 5°C Bedarf. Im Kühlmodus wird bei geöffnetem Fenster das Ventil geschlossen (der Strom zum Stellmotor wird abgeschaltet) um einen Schimmelschutz zu gewährleisten.

### Bad OG

Das Bad im OG soll **immer eher warm** sein. Im Kühlbetrieb soll es deshalb **nicht aktiv gekühlt** werden.

| Modus  | Ventilstellung |
|--------|----------------|
| Heizen | offen          |
| Kühlen | geschlossen    |

---

### Schlafzimmer + Ankleide (begehbarer Kleiderschrank)

Die beiden Räume (Schlafzimmer + Ankleide) sind durch einen Mauerdurchbruch verbunden.  
In Schritt 1 wurden die beiden Thermostate auf **einen gemeinsamen Kreis** zusammengelegt.

Ziel:

- Schlafzimmer soll eher kühl, aber nicht zu kalt sein.  
- Die Ankleide hängt an derselben Logik, weil die Räume verbunden sind.  

---

### Arbeitszimmer OG

Das Arbeitszimmer soll vom Thermostat im Heizbetrieb auf einer Zieltemperatur gehalten werden.

---

### Kinderzimmer

Das Kinderzimmer soll vom Thermostat im Heizbetrieb auf einer Zieltemperatur gehalten werden.

---

### Arbeitszimmer EG

Das Arbeitszimmer EG soll vom Thermostat im Heizbetrieb auf einer Zieltemperatur gehalten werden.

---

## Automationen (Überblick)

### Zentraler Dispatcher (`script.heizkreisventilsteuerung`)

Statt Logik in jeder Raum-Automation zu duplizieren, gibt es einen zentralen Dispatcher, der pro Raum mit dem jeweiligen ZBMINI-Switch aufgerufen wird:

- wertet `sensor.heizungsbetriebsmodus` aus und ruft je nach Modus ein Sub-Skript auf:
  - **Heizbetrieb** (`heizkreisventilsteuerung_heating`): prüft per `any_window_open`, ob im Raum ein Fenster offen ist; wenn ja wird das Thermostat per `climate.set_hvac_mode` auf `off` gestellt, sonst auf `heat`.
  - **Kühlbetrieb** (`heizkreisventilsteuerung_cooling`): schließt das Ventil (Relais aus), wenn ein Fenster durchgehend länger als 5 Minuten offen ist (Schimmelschutz), sonst bleibt/wird das Relais eingeschaltet.
- Kein Rohsignal-Handling mehr über einen L/N-Kontakt – die Thermostate sind reguläre `climate`-Entities (Zigbee, eigener ZHA-Quirk).

### Raum-Automationen (Blueprint)

Arbeitszimmer EG/OG, Kinderzimmer und Schlafzimmer sind Instanzen von `blueprints/automation/heizkreis_raumsteuerung.yaml` und rufen darüber den Dispatcher mit dem raumspezifischen ZBMINI-Switch auf. Trigger je Instanz:

- Home Assistant Start
- Änderung des Fenstersensors
- Änderung des Thermostat-**Sollwerts** (Attribut `temperature`)

Eine Änderung des Heizungsbetriebsmodus selbst triggert die Raum-Automationen NICHT direkt – das übernimmt die folgende Automation.

### Umschaltung bei Moduswechsel (`Heizung – Heizen/Kühlen umschalten`)

Wechselt `sensor.heizungsbetriebsmodus`, schaltet diese Automation das Bad-OG-Relais direkt und ruft danach `script.setheizkreisventilebetriebsmodus` auf. Dieses Skript setzt für alle anderen Raumventile (Gruppe `switch.heizkreisventile`) den Grundzustand (Detach + Relais + `climate.set_hvac_mode`) passend zum neuen Modus und stößt anschließend je Raum erneut den Dispatcher an (für die Fenster-Feinlogik).

### Start-Synchronisation (`Heizung – HA-Start Sync`)

Beim Hochfahren von Home Assistant wartet diese Automation (max. 15 Minuten) bis Vor-/Rücklauf-Sensoren und alle Heizkreis-Relais verfügbar sind, bevor sie den initialen Zustand setzt (Bad OG direkt, alle anderen über `setheizkreisventilebetriebsmodus`). Bei Timeout wird ein Fehler ins System-Log geschrieben und die Automation bricht ab.

### Automation Bad OG

Das Bad OG hat weiterhin eine eigene, vereinfachte Automation (kein Thermostat, richtet sich nur nach dem Heizungsmodus):

- Trigger: Änderung des Heizungsbetriebsmodus, Änderung des eigenen Relais-Status, Home Assistant Start
- Im **Heizbetrieb** wird das Ventil geöffnet, im **Kühlbetrieb** bleibt/wird es geschlossen
- **Einzige Stelle**, die jede Entscheidung zusätzlich ins Logbook schreibt (`logbook.log`) – die übrigen Räume loggen nicht.

## Programmschalter-Automatik (Warmwasser ↔ Programm)

`select.heizung_programmschalter` wird zentral über ein Skript und eine Automation gesteuert, um Heizbetrieb bei warmem Wetter oder offener Terrassentür zu vermeiden. Das ersetzt seit 16.09.2026 fünf frühere Einzelautomationen, die sich gegenseitig in die Quere kamen.

### Skript `script.heizung_programmziel_bestimmen`

Bestimmt aus dem aktuellen Zustand, wie der Programmschalter stehen soll. Die erste zutreffende Regel gewinnt:

| # | Bedingung | Ziel |
|---|-----------|------|
| 1 | Terrassentür offen + `Heating` + Verdichter aus | `Warmwasser` |
| 2 | Außentemperatur < Kalt-Schwelle + `Heating` + Terrassentür zu | `Programm` |
| 3 | Außentemperatur > Warm-Schwelle + nicht `Cooling` + Terrassentür zu | `Warmwasser` |
| – | sonst | `Programm` |

- Schwellwerte als Helfer, ohne Skript-Änderung anpassbar: `input_number.heizung_aussentemp_kalt_schwelle` (aktuell 21 °C) und `input_number.heizung_aussentemp_warm_schwelle` (aktuell 22 °C).
- Regel 1 wartet, bis der Verdichter steht – ein laufender Heizzyklus wird nicht abgebrochen.
- Die Regeln hängen nur von Tür, Außentemperatur, Heizungsbetriebsmodus und Verdichter ab, nicht vom aktuellen Wert des Programmschalters. Dadurch ist das Ergebnis unabhängig davon, wie oft oder in welcher Reihenfolge das Skript läuft.

### Automation `Heizung – Programmschalter zentral steuern`

Ruft bei jedem Trigger nur das Skript auf (Modus `queued`):

- Änderung von `sensor.heizung_aussentemp_gerundet` – Außentemperatur auf 0,5 °C gerundet, damit nicht jeder kleine Messwertsprung neu bewertet wird. Das Skript prüft die Schwellen weiterhin mit dem ungerundeten `sensor.heizung_aussentemp`.
- Terrassentür auf / zu
- Verdichter aus

**Wichtig:** `sensor.heizungsbetriebsmodus` darf hier nur als Bedingung verwendet werden, nie als Trigger. Der Programmschalter ist ein Eingang dieses Sensors – ein Trigger würde einen Regelkreis erzeugen (daher kam früher das Hin- und Herschalten im Sekundentakt).

## Automatisierungs Ziel
- mehr Sensoren an allen Fenstern und Türen erlauben gezielte automatische Abschaltung der Räume, wenn Fenster oder Türen offen sind.

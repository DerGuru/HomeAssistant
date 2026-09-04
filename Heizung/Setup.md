# Setup
Wir haben eine Fussbodenheizung mit zwei zusätzlichen Bad-Wand-Heizkörpern und fahren einen Heiz- und einen Absenkbetrieb. 
Die Heizung ist innengeführt über die Wohnküche und damit auch die beiden Flure im EG und OG, da hier alles offen ist.

## Räume
Alle Räume haben Fussbodenheizung.
| Etage | Raumname | Größe in m²| Durchgang offen | verbunden mit (Etage - Raum) | Durchfluss l/min | dauerhaft offen |
|-------|----------|------------|-------|------------------------------|------------------|-----------------|
| EG    | Flur     | 11,34 | ja | OG - Flur | 1,0  | ja |
| EG    | Bad      | 5,28 | nein | EG - Flur | 3,6 | ja |
| EG    | Büro     | 8,79 | ja | EG - Flur | 1,0 | ja |
| EG    | Wohnzimmer/-küche | 44,92 | ja | EG - Flur | 5,2 | ja |
| OG    | Flur     | 7,35 | ja | EG - Flur | 0 | nein |
| OG    | Bad      | 12,89 | nein | OG - Flur | 3,5 | ja |
| OG    | Kinderzimmer | 14,50 | nein | OG - Flur | 3,0 | nein |
| OG    | Büro     | 12,43 | nein | OG - Flur | 3,0 | nein |
| OG    | Schlafzimmer | 13,78 | ja | OG - Ankleide | 2,0 | nein |
| OG    | Ankleide | 7,69 | ja | OG - Schlafzimmer | 1,5 | nein |

## Die Heizung
Es ist eine Tecalor TTF 7 cool (Baujahr 2012/2013)  mit einer FEK verbaut, die in der Wohnküche angebracht ist.\
Wir haben keinen Pufferspeicher - dadurch muss immer ein Mindestdurchfluss gegeben sein. \
Ich habe deshalb einen hydraulischen Abgleich mit den folgenden Räumen vorgenommen: 
- EG - Bad
- EG - Büro
- EG - Wohnzimmer mit Wohnküche
- EG - Flur
- OG - Bad 

Die anderen Räume im OG werden über Thermostate gesteuert, die noch manuell zwischen Kühlbetrieb und Heizbetrieb geschaltet werden müssen. Das wird ein Smart Home Projekt, dass noch aussteht, weil ich im Sommer die Bäder schließen möchte und dafür die anderen Räume im OG dauerhaft öffnen will.

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
Die Heizung fährt dort einfach „durch“, alle Kreise sind dauerhaft offen.

Das Shelly für die Heiz-/Kühlerkennung übernimmt zusätzlich eine manuelle Schaltfunktion für das Arbeitszimmer im EG. So kann der Raum bei Bedarf komplett aus dem Heiz-/Kühlbetrieb genommen werden – z. B. wenn er mal als Gästezimmer dient.

Im OG werden vier Shelly verwendet, um zwischen Heiz- und Kühlbetrieb umzuschalten.  
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

```YAML
{% set p = states('select.heizung_programmschalter') %}
{% set kein_kuehlen = p in ['Warmwasser', 'Bereitschaft', 'Notbetrieb'] %}
{% set kuehlbetrieb = is_state('binary_sensor.heizung_kuehlbetrieb', 'on') %}
{% set ruecklauf_soll = states('sensor.heizung_ruecklaufsolltemp') | float(99) %}

{% if kein_kuehlen %}
  Heating
{% elif kuehlbetrieb or ruecklauf_soll <= 6 %}
  Cooling
{% else %}
  Heating
{% endif %}
```

---

## Automatische UmSchaltung Arbeitszimmer EG

Im EG gibt es noch einen einzigen verbleibenden Stellmotor, der nicht hydraulisch „fix“ mitläuft: das **Arbeitszimmer EG**. Der Stellmotor wird über ein Smart Relais geschaltet, an dessen Input ein Moes Zigbee Thermostat hängt.

## Automatische Umschaltung Heizen/Kühlen im OG

Im OG sind vier **SONOF ZIGBEE RELAIS** verbaut, die die Stellmotoren für:

- Bad OG  
- Schlafzimmer OG  + Ankleide  
- Arbeitszimmer OG  
- Kinderzimmer OG  

und im EG ist ein **SONOF ZIGBEE RELAIS** verbaut, das den Stellmotor für das Arbeitszimmer EG

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

Zusätzlich zur Heizkreis-Ventilsteuerung gibt es vier Automationen, die `select.heizung_programmschalter` zwischen `Programm` und `Warmwasser` hin- und herschalten, um Heizbetrieb bei warmem Wetter oder offener Terrassentür zu vermeiden:

- **`Heizung – Warm nur Warmwasser`**: schaltet auf `Warmwasser`, wenn `sensor.heizung_aussentemp` über 22 °C steigt (während der Programmschalter im Heizbetrieb ist).
- **`Heizung – Kühl aktiviert Heizkreise`**: schaltet zurück auf `Programm`, wenn `sensor.heizung_aussentemp` unter 21 °C fällt.
- **`Heizung – Terrassentür offen -> Warmwasser`** / **`Heizung – Terrassentür geschlossen -> Programm`**: dieselbe Umschaltung, ausgelöst durch `binary_sensor.terassentur` statt durch die Außentemperatur (mit Rücksicht auf den laufenden Verdichter, `binary_sensor.heizung_verdichter`).

**Bekannte Einschränkung (Stand 2026-08-27):** Diese vier Automationen prüfen historisch gewachsen teils `sensor.heizungsbetriebsmodus` statt direkt `select.heizung_programmschalter`. Da der Programmschalter-Zustand `Warmwasser` in `sensor.heizungsbetriebsmodus` immer als `Heating` klassifiziert wird (siehe Template oben), kann der Sensor den Zustand `Cooling` nicht mehr erreichen, sobald einmal auf `Warmwasser` geschaltet wurde – ein darauf wartender Rück-Umschalt-Zweig wäre totes Gleis. Ein Rewrite (Gate direkt auf `select.heizung_programmschalter` statt auf `sensor.heizungsbetriebsmodus`) ist geplant, aber noch nicht umgesetzt.

## Automatisierungs Ziel
- mehr Sensoren an allen Fenstern und Türen erlauben gezielte automatische Abschaltung der Räume, wenn Fenster oder Türen offen sind.

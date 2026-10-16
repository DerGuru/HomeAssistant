# Raumregelung der Fußbodenheizung mit Home Assistant

Stand: 16. Oktober 2026

## 1. Ziel

Die Heizkreise sollen künftig bedarfsgerecht in Zwischenstellungen betrieben werden, statt ausschließlich vollständig offen oder geschlossen zu sein. Langfristig sollen sich möglichst stabile Ventilstellungen und Raumtemperaturen einstellen.

Dabei soll jeder Raum den benötigten Durchfluss erhalten. Das Wohnzimmer wird aktuell eher zu warm, während die oberen Zimmer wegen der geringen Dämmung zum ungeheizten Dachboden mehr Wärme benötigen.

**11 l/min Gesamtdurchfluss sind die vorgesehene Untergrenze für den Heizbetrieb, kein anzustrebender Maximal- oder Sollwert.** Bei höherem Wärmebedarf darf mehr Wasser fließen. Diese Grenze ist die Arbeitsvorgabe des Projekts; eine Herstellerprüfung war nicht Bestandteil des Chats.

Die Wärmepumpe soll weiterhin ihre eigene Betriebs- und Schutzregelung übernehmen. Home Assistant übernimmt die Wärmeverteilung zwischen den Räumen.

## 2. Ausgangslage

- Wärmepumpe: **Tecalor TTF 7 cool**, Fußbodenheizung ohne Pufferspeicher.
- Zentrale Steuerung und Historie: **Home Assistant**, derzeit ZHA für Zigbee.
- Bisher thermische Auf/Zu-Stellantriebe mit verzögertem Öffnen und Schließen.
- Abstand der Ventile am Verteiler: **55 mm Mitte–Mitte**.
- Geplant: bei vollständig geöffneten Stellventilen die geregelten Kreise möglichst auf **tatsächlich gemessene 2,5 l/min** einregulieren. Voraussetzung ist, dass die Hydraulik dies zulässt.
- **Bad OG und Bad EG bleiben ungeregelt.** Ihre offenen Kreise tragen zum Gesamtdurchfluss bei; separate Rücklauffühler sind dort zunächst nicht vorgesehen.

### Geregelte Räume und Messstellen

| Raum | Heizkreise | Geplante Rücklauffühler |
|---|---:|---:|
| Schlafzimmer | 1 | 1 |
| Kinderzimmer | 2 | 2 |
| Büro OG | 2 | 2 |
| Wohnzimmer | 4 | 4 |
| Büro EG | 1 | 1 |
| Flur | 1 | 1 |
| **Gesamt** | **11** | **11** |

Vorgesehen sind **sechs Raumregler**, nicht elf voneinander unabhängige Raumthermostate. Die einzelnen Rücklaufmessungen helfen, Unterschiede zwischen den Kreisen eines Raums zu erkennen und deren Verteilung gegebenenfalls anzupassen.

## 3. Hardware

### Temperaturerfassung: vorhanden beziehungsweise vorgesehen

- **2 × Shelly The Pill**.
- Entsprechende **DS18B20-Temperaturfühler**.
- Zusätzlich **5 Sensorkabel/Fühleranschlüsse am Add-on eines Shelly 1PM**, nach der beschriebenen Planung.
- Die genaue Zuordnung der 13 Sensoren zu den drei Erfassungsgeräten wird bei der Installation festgelegt.
- Bereits vorhanden: Raumtemperatur- und Fenstersensoren sowie Temperatur- und Betriebsdaten der Wärmepumpe.

Die Rücklauffühler kommen an die einzelnen Rohre **vor deren Zusammenführung im Verteiler**. Gleiche Montagebedingungen, guter Kontakt und Dämmung über Sensor und Rohr sollen vergleichbare Messwerte ermöglichen. Plaste/Gummi-Rohre führen zu einer gewissen thermischen Trägheit und Messabweichung.

Die Fühler messen zunächst die Rohroberfläche. Bei Durchfluss ist diese eine Näherung für die Wassertemperatur, mit Messabweichung und Verzögerung. Bei geschlossenem Kreis beschreibt der Fühler die Temperatur des stehenden Wassers und des Rohrs, nicht die eines zurückströmenden Wasserstroms.

### Positionierbare Ventilantriebe: Testkandidat

**Sonoff TRV Gen2, Modell TRV-ZBT**:

- Zigbee, vorgesehen zur Einbindung über ZHA.
- Maße: **50 × 50 × 82,9 mm**. Bei 55 mm Achsabstand bleiben rechnerisch 5 mm zwischen den Gehäusen.
- Anschluss **M30 × 1,5**; tatsächliche Eignung bezüglich Ventilhub, Schließmaß und Befestigung am FBH-Verteiler muss geprüft werden.
- Versorgung: **2 × AA-Alkaline, insgesamt 3 V**.
- Optionaler Netzbetrieb über einen geeigneten **3-V-Batterie-Eliminator mit AA-Dummys**. Noch nicht ausgewählt oder am Gerät bestätigt; Ausgangsstrom für Motoranlauf und Kabeldurchführung sind zu prüfen.

Der ältere **TRVZB** ist mit 59,4 mm Breite für direkte Montage nebeneinander bei 55 mm Abstand zu breit. Erfahrungen und Firmwareangaben des älteren Modells dürfen nicht pauschal auf den Gen2 übertragen werden.

### ZHA-Quirk

Die Datei **`sonoff_trv_zbt_fbh.py`** wurde erstellt. Sie stellt bereit:

- Heating valve opening: 0–100 %.
- Idle valve opening: 0–100 %.
- Adaptive mode, Betriebsmodus, Fenstererkennung und Kindersicherung.
- Kalibrierungstaste und Kalibrierungsstatus.

Die Protokolldaten stammen aus dem offenen ZHA-Quirk-Vorschlag #5234. Lokal wurden Import, Werteprüfung und Zigbee-Schreibbefehle geprüft. **Diese Variante wurde noch nicht am echten Gerät getestet.**

Für erste Positionsversuche:

1. Betriebsmodus "Manual" einstellen.
2. Adaptive mode und interne Fenstererkennung ausschalten.
3. Kindersicherung zunächst ausgeschaltet lassen.
4. Heating und Idle valve opening auf denselben Wert setzen, beispielsweise **30/30**.

Beide Gen2-Parameter beschreiben laut Dokumentation Öffnungsgrade. 

**Gleiche Heiz-/Ruhewerte als Positionsvorgabe sind ein zu prüfender Ansatz.** Es handelt sich nicht um einen nachgewiesenen nativen Positionsmodus; Schutzfunktionen oder andere Firmwarezustände können Vorrang haben. Angezeigte Prozentwerte sind keine unabhängige Messung der mechanischen Position.

## 4. Regelkonzept

### Wärmepumpe: zentrale Temperaturbereitstellung

Geplant ist, den **Raumeinfluss der FEK auf 0** zu setzen, damit ein bereits warmes Referenzzimmer die zentrale Temperaturvorgabe nicht reduziert, während oben noch Wärmebedarf besteht.

Außentemperatur und Heizkurve bestimmen weiterhin den Heizwasser-Sollwert. Raumeinfluss 0 allein stellt weder eine konstante Rücklauftemperatur noch automatisch eine reine Rücklaufregelung ein; die konkrete WPM-Konfiguration ist vorher zu prüfen.

Die Heizkurve soll so niedrig wie möglich bleiben, aber die oberen Zimmer bei ausreichend geöffneten Kreisen versorgen können. Bleiben diese trotz ausreichendem Durchfluss und offenen Ventilen zu kalt, kann ein Raum-PID fehlende Heizleistung nicht ersetzen. Die Heizkurve müsste dann erhöht werden.

### Raumregler: gewünschter Durchfluss

Jeder Raum erhält ein PID-Thermostat/Regler. Dessen Ausgang soll vorzugsweise ein **gewünschter Raumdurchfluss in l/min** sein, der bei mehreren Kreisen auf diese verteilt wird. Die konkrete Aufteilung wird festgelegt; ein Raum mit vier Kreisen darf nicht versehentlich wie ein einzelner Kreis behandelt werden.

- **P:** reagiert auf die aktuelle Abweichung zwischen Soll- und Raumtemperatur.
- **I:** korrigiert anhaltende Abweichungen und hält den für den Raum nötigen dauerhaften Ausgangswert.
- **D:** kann bei steigender Raumtemperatur frühzeitig bremsen und Überschwingen reduzieren. Er erkennt jedoch nur den gemessenen Trend, nicht direkt die im Estrich gespeicherte Wärme.

Die PID-Regler sollen anhand der Messdaten verglichen werden. Ein D-Anteil ist weder grundsätzlich notwendig noch grundsätzlich ungeeignet. Falls verwendet, soll er auf der gefilterten Isttemperatur arbeiten, um Messrauschen und Ausschläge durch Sollwertsprünge zu begrenzen.

Bei offenen Fenstern wird die normale Raumregelung ausgesetzt beziehungsweise passend begrenzt. Der I-Anteil darf währenddessen nicht ungebremst Heizbedarf aufbauen. Auch bei Eingriffen der Mindestdurchflusslogik muss die Integratorbehandlung berücksichtigt werden (**Anti-Windup**).

### Mindestdurchfluss: gemeinsame Koordination

Eine übergeordnete Logik koordiniert die Raumwünsche und berücksichtigt den Beitrag der beiden ungeregelten Bäder.

- Im Heizbetrieb sollen mindestens **11 l/min tatsächlich gemessener Gesamtdurchfluss** vorhanden sein.
- Die Summe der Kennlinienwerte ist nur eine Schätzung und ersetzt diese Messung nicht.
- Muss zusätzlicher Durchfluss freigegeben werden, sollen bevorzugt Räume mit verbleibendem Wärmebedarf genutzt werden.
- Offene Fenster oben sind ein wichtiger Sonderfall. Gleichzeitig drosselnde Raumregler können ebenfalls einen Eingriff erfordern.
- Gibt es insgesamt zu wenig Wärmebedarf, entsteht ein Zielkonflikt zwischen Raumkomfort und benötigtem Durchfluss. Ein PID beseitigt diesen Konflikt nicht.

Stabile Ventilstellungen garantieren keinen dauerlaufenden Verdichter: Auch das Verhältnis zwischen Wärmepumpenleistung und Gebäude-Wärmebedarf bestimmt das Takten.

## 5. Durchfluss auf Ventilöffnung abbilden

Eine Tabelle soll den gewünschten Durchfluss auf eine Öffnung in Prozent abbilden. Zwischen Messpunkten wird linear interpoliert.

Vorgehen:

1. Bei vollständig geöffneten Stellventilen möglichst alle geregelten Kreise auf gemessene 2,5 l/min einregulieren.
2. Unter dokumentierten Pumpen- und Anlagenbedingungen Messpunkte für unterschiedliche Öffnungen aufnehmen.
3. Zunächst **eine gemeinsame Kennlinie** verwenden, da gleiche Ventile und gleiche Vollöffnungsdurchflüsse vorgesehen sind.
4. An unterschiedlichen Kreisen Zwischenstellungen vergleichen.
5. Individuelle Kennlinien nur bei praktisch relevanten Abweichungen ergänzen.

Die gemeinsame Kennlinie ist eine Näherung. Andere Ventilstellungen und Pumpenbedingungen verändern den Durchfluss bei gleicher Öffnung; dieser hydraulische Effekt besteht bereits heute.

Im Chat wurde ein HA-Skriptbeispiel mit Rückgabe per `stop` und `response_variable` gezeigt. Es liefert ein Dictionary, etwa `{"opening_pct": 40}`. Der Aufrufer verwendet direkt `script.<name>`, nicht `script.turn_on`.

**Die damaligen Tabellenwerte waren frei erfundene Beispiele, keine Kalibrierung.** Außerhalb des Messbereichs soll begrenzt und nicht unkontrolliert extrapoliert werden.

## 6. Verdichterstart und Stellgeschwindigkeit

Beim Drosseln des Wohnzimmers wurde beobachtet, dass die Vorlauftemperatur schnell auf über 40 °C stieg und der Verdichter nach ungefähr 30 Sekunden wieder ausging. Die genaue Abschaltbedingung wurde nicht ermittelt; daraus folgt keine fest zugesicherte Durchflussüberwachungsfrist.

Die Idee ist, das Wohnzimmer bei Bedarf in Verdichterpausen zu schließen und zum Heiztakt wieder genügend Durchfluss freizugeben.

**Ziel für eine reaktive Öffnung: etwa 10 Sekunden vom tatsächlichen Verdichterstart bis zum ausreichenden Gesamtdurchfluss.** 20 Sekunden wären gegenüber der beobachteten Abschaltung bereits knapp.

Zur Gesamtzeit gehören:

- Aktualisierung des Verdichterstatus in HA.
- Ausführung der Automation und Zigbee-Übertragung.
- Reaktion des Antriebs und ausreichende Ventilöffnung.
- Aufbau des benötigten Durchflusses.

Eine belastbare vollständige Stellzeit des TRV-ZBT wurde nicht gefunden. Die tatsächliche Zeit muss am Gerät gemessen werden. Ein Test soll zunächst erfolgen, während andere Kreise ohnehin ausreichend Durchfluss sicherstellen.

Falls ein verlässliches Signal vor dem Verdichterstart existiert, etwa ein ausreichend früher Pumpenstart, kann es für das Öffnen genutzt werden. Ob die Anlage dies bietet, ist noch zu prüfen.

Langfristig sollen bereits ausreichend viele Kreise in stabilen Zwischenstellungen offen sein, sodass schnelles zusätzliches Öffnen ein Sonderfall wird.

## 7. Messdaten und Parameterbestimmung

Verfügbar beziehungsweise vorgesehen sind:

| Größe | Umfang / Einschränkung |
|---|---|
| Raumtemperatur und Sollwert | Pro Raum |
| Außentemperatur | Gemeinsam |
| Fensterzustände | Über Fenstersensoren |
| Ventil-Schaltzeiten | Bisher Auf/Zu-Befehl; thermische Aktorverzögerung berücksichtigen |
| Durchfluss je Kreis | Bisher eingestellter Offen-Wert, keine kontinuierliche Einzelmessung |
| Verdichterstatus | Zentral |
| Vor- und Rücklauftemperatur | Zentral von der Wärmepumpe |
| Rücklauftemperaturen der geregelten Kreise | Künftig über elf Anlegefühler |
| Tatsächlicher Gesamtdurchfluss | Für die übergeordnete Begrenzung verwenden; Signal und Aktualisierungsrate prüfen |

Aus mehreren Tagen bis Wochen können Verzögerung, Erwärmung, Abkühlung und Nachheizen der Räume abgeschätzt werden. Wichtig sind ausreichend unterschiedliche Betriebszustände und gemeinsame Zeitstempel.

Die vorhandene Auf/Zu-Historie kann bereits für einfache thermische Modelle genutzt werden. Sie belegt jedoch noch nicht die Wirkung verschiedener motorischer Zwischenstellungen.

Die Verzögerung der alten thermischen Aktoren muss von der Trägheit von Boden und Raum getrennt werden. Andernfalls würde die neue Regelung auf einer nicht mehr vorhandenen Aktorverzögerung abgestimmt.

Die zentrale Vorlauftemperatur ist eine Näherung für die Versorgung der Kreise. Transportverzögerung und Verluste bis zum Verteiler bleiben zu berücksichtigen. Mit Rücklauffühlern und geschätztem Einzeldurchfluss lässt sich die Wärmeabgabe näherungsweise untersuchen, aber nicht als präzise Wärmemengenmessung behandeln.

Ergebnis der Auswertung sollen **begründete Startparameter mit ausgewiesener Unsicherheit** sein. Die Parameter müssen zur konkreten PID-Implementierung, ihren Einheiten und ihrer Abtastzeit passen. Prüfung zunächst an einem separaten Historienabschnitt, danach im realen Betrieb.

## 8. Praktisches Vorgehen

1. **Sensoren vorbereiten:** Eindeutig beschriften und unter gleichen Temperaturbedingungen vergleichen; Offsets möglichst im späteren Betriebsbereich bestimmen.
2. **Sensoren montieren:** Elf Rückläufe einheitlich bestücken, Messstellen dämmen und Sensoren den Kreisen in HA zuordnen.
3. **Ausgangszustand aufzeichnen:** Bestehende Regelung dokumentieren und zunächst unverändert Daten sammeln. Prüfen, ob die Historie die benötigte Auflösung und Aufbewahrungsdauer bietet.
4. **Einen TRV-ZBT erproben:** Mechanische Eignung, ZHA-Quirk, Zwischenstellungen, vollständiges Schließen, Funkzuverlässigkeit und Reaktionszeit prüfen.
5. **Kennlinie messen:** Öffnungswerte gegen tatsächliche Durchflussanzeige aufnehmen; Hin- und Rückweg vergleichen, um Hysterese oder Positionsverlust zu erkennen.
6. **Historie auswerten:** Raumdynamik modellieren und geeignete PI/PID-Startwerte sowie Filterung und Integratorgrenzen bestimmen.
7. **Schrittweise umstellen:** Zunächst einen Raum regeln. Währenddessen ausreichenden Gesamtdurchfluss über die übrigen Kreise sicherstellen.
8. **Gemeinsame Logik ergänzen:** Mindestdurchfluss, Fensterzustände, Verdichterstart und Verhalten bei fehlenden Messwerten oder nicht erreichbaren Aktoren festlegen.
9. **Weitere Räume übernehmen:** Unterschiede prüfen und nur dort individuelle Kennlinien oder Parameter ergänzen, wo sie tatsächlich nötig sind.
10. **Im Betrieb nachstellen:** Raumtemperaturschwankungen, Ventilbewegungen, Gesamtdurchfluss und Verdichterlaufzeiten gemeinsam bewerten.

## 9. Offene Punkte und Grenzen

- TRV-ZBT am FBH-Ventil mechanisch passend?
- Gleiche Heiz-/Ruheöffnungswerte tatsächlich dauerhaft wirksam?
- Ausreichend schnelle Reaktion inklusive HA-Meldeverzögerung?
- Reproduzierbare Zwischenstellungen und vollständiger Ventilschluss über viele Zyklen?
- Geeigneter 3-V-Netzadapter und mögliche Kabelführung?
- Konkrete PI/PID-Implementierung in HA noch auszuwählen.
- Verhalten bei Sensor-/Funk-/HA-Ausfall sowie bei widersprüchlichen Raumwünschen noch festzulegen.
- Beim Gen2 wurde ein Nutzerbericht zu Erreichbarkeitsproblemen und blockierter Motorbewegung bei Kindersicherung unter Firmware 1.1.0 gefunden. Das ist kein Nachweis, dass jedes Gerät betroffen ist, aber beim Einzelgerätetest zu berücksichtigen.
- Die diskutierten Kalibrierungsverluste und die Gegenmaßnahme „voll öffnen, dann schließen“ stammen hauptsächlich vom älteren TRVZB. Nicht ohne Prüfung als Gen2-Verhalten oder automatische Routine übernehmen.

## 10. Referenzen aus der Recherche

- Sonoff TRV-ZBT: https://sonoff.tech/products/sonoff-trv-gen2-zigbee-thermostatic-radiator-valve-trv-zbt
- Gen2-Zigbee-Parameter: https://www.zigbee2mqtt.io/devices/TRV-ZBT.html
- ZHA-Quirk-Vorschlag: https://github.com/zigpy/zha-device-handlers/pull/5234
- Gen2-Fehlerbericht Firmware 1.1.0: https://github.com/Koenkk/zigbee2mqtt/issues/33291
- HA-Skripte mit Rückgabewert: https://www.home-assistant.io/building-blocks/stop/
- Shelly Plus Add-on: https://www.shelly.com/de/products/shelly-plus-add-on

Diese Zusammenfassung beschreibt den besprochenen Plan und die bisherigen Rechercheergebnisse. Sie dokumentiert noch keine abgeschlossene Installation oder am Gesamtsystem validierte Regelung.

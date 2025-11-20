import pyperclip



#model = "DSOX2002A"



def getPrompt(model: str) -> str:
    pr =  f"""Du bist ein Fachexperte für die Analyse von Oszilloskop-Datenblättern und die Extraktion technischer Daten.

    AUFGABE:
    Analysiere das bereitgestellte PDF-Dokument. Deine Aufgabe ist es, die technischen Spezifikationen **ausschließlich** für das Modell **{model}** zu extrahieren.

    Halte dich für die Ausgabe **strikt** an das vorgegebene JSON-Schema.


WICHTIGE SCHLAGWORTE UND KONTEXT FÜR DIE ERKENNUNG UND ANALYSE!

- Modell: Ist im Prompt angegeben
- Bandbreite: Suche nach "Bandbreite", "bandwidth", "MHz", "GHz", oft in Tabellen oder technischen Daten     
- Anzahl Kanäle: Suche nach "Kanäle", "channels", "2-Kanal", "4-Kanal", oft im Titel oder Überschrift        
- Samplerate: Suche nach "Abtastrate", "Sample rate", "Sa/s", "GSa/s", "MSa/s"
- Speichertiefe: Suche nach "Speicher", "memory depth", "Mpts", "kpts", "Sample"
- Triggerarten: Suche nach "Edge", "Pulse width", "Video", "Pulse Runt", "Rise&Fall", "Timeout", "Alternate", "Event-Delay", "Time-Delay", und weiterem; Triggerarten, nicht Triggermode; ignoriere optionale Triggerarten; Manuell, Auto oder ähnliche sind keine Triggerarten; Versuche Triggerarten wie in der Liste widerzugeben und veränder diese wenn sinnvoll nicht.
- Vertikale Auflösung: Suche nach "Auflösung", "resolution", "Bit", "8-bit", "12-bit"
- Digitalkanäle: Suche nach "digital", "Logic", "MSO"
- Bildschirmgröße: Suche nach "Display", "Bildschirm", "Zoll", "cm", "inch"
- Bildschirmtyp: Suche nach "Touchscreen", "TFT", "LCD", "Farb", "color"
- Schnittstellen: Suche nach "USB", "LAN", "WLAN", "GPIB", "VGA", "HDMI", "DP", ... oft unter "Connectivity", fasse ähnliche Schnittstellen wie z.B: USB 2.0, USB 3.0, ... in ein generisches Keyword zusammen und ignoriere die Version(USB), ...
- Serielle Busse: Suche nach "I2C", "SPI", "CAN", "LIN", "UART", "RS", ... oft unter "Triggering & Decode"; jeder neue Bus, soll ein extra Value in der Liste sein
- Signalerfassungsrate: Suche nach "waveform", "wfms/s", "update rate", "Erfassungsrate"
- Segmentierbarer Speicher: Suche nach "segmented", "history", "sequence"
- Funktionsgenerator: Suche nach "Arbitrary", "Waveform Generator", "AWG", "Function Generator"
- DVM: Suche nach "Digital Voltmeter", "DVM", "Multimeter-Funktion"
- Counter: Suche nach "Frequency Counter", "Zähler", "Counter"
- Besonderheiten: Suche nach "Features", "Highlights", "Besonderheiten", spezielle Funktionen, Bandbreitenupgrade nachträglich möglich
- Abmessungen: Suche nach "Abmessungen", "dimensions", "L x B x H", "W x H x D", "in", "mm"
WICHTIG - UMRECHNUNG DER REIHENFOLGE:      Verschiedene Konventionen in Datenblättern:   * W x H x D (Width x Height x Depth) - üblich im Englischen   * B x H x T (Breite x Höhe x Tiefe) - üblich im Deutschen   * L x B x H (Länge x Breite x Höhe) - gewünschtes Ausgabeformat      Umrechnungstabelle:   * Länge (L) = Depth (D) = Tiefe (T) = Tiefe von vorne nach hinten   * Breite (B) = Width (W) = Breite von links nach rechts   * Höhe (H) = Height (H) = Höhe von unten nach oben      IMMER in L x B x H konvertieren:   - Wenn Quelle "W x H x D" zeigt → umordnen zu [D, W, H] für L x B x H   - Wenn Quelle "B x H x T" zeigt → umordnen zu [T, B, H] für L x B x H   - Wenn Quelle bereits "L x B x H" zeigt → direkt übernehmen [L, B, H]   - Wenn Quelle "Width x Height x Depth" zeigt → [Depth, Width, Height]      Eselsbrücke für Oszilloskope/Tischgeräte:   - Länge (L) = Tiefe = wie weit steht es auf dem Tisch (oft kleinster Wert)   - Breite (B) = Breite = wie breit ist die Front (oft größter horizontaler Wert)   - Höhe (H) = Höhe = wie hoch stapelbar (vertikaler Wert)      Beispiele:   * "381 x 204 x 142 mm (W x H x D)" → [142, 381, 204] in L x B x H   * "15 x 8 x 5.6 inch (W x H x D)" → erst zu mm konvertieren, dann [142, 381, 204]   * "350 x 180 x 125 mm (B x H x T)" → [125, 350, 180] in L x B x H
- Gewicht: Suche nach "Gewicht", "weight", "kg", "g".
- Garantie: Suche nach "Garantie", "warranty", "Jahre", "years"
- Artikelnummer: Suche nach "Order No", "Bestellnummer", "Part Number", "P/N"


    ANWEISUNGEN FÜR DIE EXTRAKTION:

    1.  **Fokus auf ein Modell:** Finde die Daten **nur** für das Modell `{model}`. Das resultierende JSON-Array darf **genau ein** Objekt enthalten, nämlich das für dieses spezifische Modell.
    2.  **Vollständigkeit pro Feld: ** Konvertiere Value erst, sodass es zum key `unit` aus der dir gegebene JSON passt! Für jeden gefundenen Wert (z.B. "Bandbreite"), fülle alle zugehörigen Felder im Schema (`value`, `unit`, `source_page`, `source_region`, `confidence`).
    3.  **`source_region`:** Verwende für `source_region` den **exakten Textausschnitt** (Snippet) aus dem PDF, der den Wert belegt, um die Herkunft nachzuvollziehen.
    4.  **Fehlende Werte:** Wenn ein Wert für `{model}` im Dokument **eindeutig nicht gefunden** wird:     
        * Setze `value` auf `null`.
        * Setze `confidence` auf `"low"`.
        * Setze `source_region` auf `"Nicht gefunden"`.
        * Setze `source_page` ebenfalls auf `null` (wie es das Schema erlaubt).
    5. Überprüfe noch einmal ob die Daten in der erstellten JSON den Daten in der PDF entsprechen. WICHTIG: passt die Abmessungen : L x B x H. Passt du Konvertierung in das deutsche Format.
""" + """
    WICHTIG:
    Deine Antwort darf **ausschließlich** den validen JSON-Code enthalten, ohne jeglichen vorangestellten oder nachfolgenden Text (kein "Here is the JSON:" oder Ähnliches).
    json schema: {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "Modell": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["string", "null"]},
                            "source_page": {"type": ["integer", "null"]},
                            "source_region": {"type": ["string", "null"]},
                            "confidence": {"type": ["string", "null"], "enum": ["high", "medium", "low", "null"]}
                        }
                    },
                    "Bandbreite": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["array", "null"], "items": {"type": "string"}},
                            "unit": {"type": ["string", "null"], "enum": ["MHz", "null"]},
                            "source_page": {"type": ["integer", "null"]},
                            "source_region": {"type": ["string", "null"]},
                            "confidence": {"type": ["string", "null"], "enum": ["high", "medium", "low", "null"]}
                        }
                    },
                    "Anzahl Kanäle": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["integer", "null"]},
                            "source_page": {"type": ["integer", "null"]},
                            "source_region": {"type": ["string", "null"]},
                            "confidence": {"type": ["string", "null"], "enum": ["high", "medium", "low", "null"]}
                        }
                    },
                    "Samplerate": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"], "enum": ["GSa/s", "null"]},
                            "source_page": {"type": ["integer", "null"]},
                            "source_region": {"type": ["string", "null"]},
                            "confidence": {"type": ["string", "null"], "enum": ["high", "medium", "low", "null"]}
                        }
                    },
                    "Speichertiefe": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"], "enum": ["Mpts", "null"]},
                            "source_page": {"type": ["integer", "null"]},
                            "source_region": {"type": ["string", "null"]},
                            "confidence": {"type": ["string", "null"], "enum": ["high", "medium", "low", "null"]}
                        }
                    },
                    "Triggerarten": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["array", "null"], "items": {"type": "string"}},
                            "source_page": {"type": ["integer", "null"]},
                            "source_region": {"type": ["string", "null"]},
                            "confidence": {"type": ["string", "null"], "enum": ["high", "medium", "low", "null"]}
                        }
                    },
                    "Vertikale Auflösung": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"], "enum": ["bit", "null"]},
                            "source_page": {"type": ["integer", "null"]},
                            "source_region": {"type": ["string", "null"]},
                            "confidence": {"type": ["string", "null"], "enum": ["high", "medium", "low", "null"]}
                        }
                    },
                    "Anzahl Digitalkanäle": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["integer", "null"]},
                            "source_page": {"type": ["integer", "null"]},
                            "source_region": {"type": ["string", "null"]},
                            "confidence": {"type": ["string", "null"], "enum": ["high", "medium", "low", "null"]}
                        }
                    },
                    "Bildschirmgröße": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"], "enum": ["cm", "null"]},
                            "source_page": {"type": ["integer", "null"]},
                            "source_region": {"type": ["string", "null"]},
                            "confidence": {"type": ["string", "null"], "enum": ["high", "medium", "low", "null"]}
                        }
                    },
                    "Bildschirmtyp": {
                        "type": "object",
                        "properties": {
                            "pixel": {
                                "type": "object",
                                "properties": {
                                    "value": {"type": ["array", "null"], "items": {"type": "integer"}},
                                    "unit": {"type": ["string", "null"], "enum": ["pixels", "null"]},
                                    "source_page": {"type": ["integer", "null"]},
                                    "source_region": {"type": ["string", "null"]},
                                    "confidence": {"type": ["string", "null"], "enum": ["high", "medium", "low", "null"]}
                                }
                            },
                            "screen_type": {
                                "type": "object",
                                "properties": {
                                    "value": {"type": ["string", "null"]},
                                    "source_page": {"type": ["integer", "null"]},
                                    "source_region": {"type": ["string", "null"]},
                                    "confidence": {"type": ["string", "null"], "enum": ["high", "medium", "low", "null"]}
                                }
                            }
                        }
                    },
                    "Schnittstellen": {
                        "type": "object",
                        "properties": {
                            "relevant_interfaces": {
                                "type": "object",
                                "properties": {
                                    "value": {"type": ["array", "null"], "items": {"type": "string"}},
                                    "source_page": {"type": ["integer", "null"]},
                                    "source_region": {"type": ["string", "null"]},
                                    "confidence": {"type": ["string", "null"], "enum": ["high", "medium", "low", "null"]}
                                }
                            },
                            "optionale_interfaces": {
                                "type": "object",
                                "properties": {
                                    "value": {"type": ["array", "null"], "items": {"type": "string"}},
                                    "source_page": {"type": ["integer", "null"]},
                                    "source_region": {"type": ["string", "null"]},
                                    "confidence": {"type": ["string", "null"], "enum": ["high", "medium", "low", "null"]}
                                }
                            }
                        }
                    },  
                    "unterstützende serielle Busse": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["array", "null"], "items": {"type": "string"}},
                            "source_page": {"type": ["integer", "null"]},
                            "source_region": {"type": ["string", "null"]},
                            "confidence": {"type": ["string", "null"], "enum": ["high", "medium", "low", "null"]}
                        }
                    },
                    "Signalerfassungsrate": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"], "enum": ["wfms/s", "null"]},
                            "source_page": {"type": ["integer", "null"]},
                            "source_region": {"type": ["string", "null"]},
                            "confidence": {"type": ["string", "null"], "enum": ["high", "medium", "low", "null"]}
                        }
                    },
                    "segmentierbarer Speicher": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["string", "null"], "enum": ["Yes", "No", "Optional", "null"]},
                            "source_page": {"type": ["integer", "null"]},
                            "source_region": {"type": ["string", "null"]},
                            "confidence": {"type": ["string", "null"], "enum": ["high", "medium", "low", "null"]}
                        }
                    },
                    "Funktionsgenerator": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["string", "null"], "enum": ["Yes", "No", "Optional", "null"]},
                            "source_page": {"type": ["integer", "null"]},
                            "source_region": {"type": ["string", "null"]},
                            "confidence": {"type": ["string", "null"], "enum": ["high", "medium", "low", "null"]}
                        }
                    },
                    "DVM": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["string", "null"], "enum": ["Yes", "No", "Optional", "null"]},
                            "source_page": {"type": ["integer", "null"]},
                            "source_region": {"type": ["string", "null"]},
                            "confidence": {"type": ["string", "null"], "enum": ["high", "medium", "low", "null"]}
                        }
                    },
                    "Counter": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["string", "null"], "enum": ["Yes", "No", "Optional", "null"]},
                            "source_page": {"type": ["integer", "null"]},
                            "source_region": {"type": ["string", "null"]},
                            "confidence": {"type": ["string", "null"], "enum": ["high", "medium", "low", "null"]}
                        }
                    },
                    "Besonderheiten": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["string", "null"]},
                            "source_page": {"type": ["integer", "null"]},
                            "source_region": {"type": ["string", "null"]},
                            "confidence": {"type": ["string", "null"], "enum": ["high", "medium", "low", "null"]}
                        }
                    },
                    "Abmessungen (L x B x H) (mm)": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["array", "null"], "items": {"type": "number"}},
                            "unit": {"type": "string", "enum": ["mm"]},
                            "source_page": {"type": ["integer", "null"]},
                            "source_region": {"type": ["string", "null"]},
                            "confidence": {"type": ["string", "null"], "enum": ["high", "medium", "low", "null"]}
                        }
                    },
                    "Gewicht (kg)": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"], "enum": ["kg", "null"]},
                            "source_page": {"type": ["integer", "null"]},
                            "source_region": {"type": ["string", "null"]},
                            "confidence": {"type": ["string", "null"], "enum": ["high", "medium", "low", "null"]}
                        }
                    },
                    "Garantie (Jahre)": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"], "enum": ["Jahre", "null"]},
                            "source_page": {"type": ["integer", "null"]},
                            "source_region": {"type": ["string", "null"]},
                            "confidence": {"type": ["string", "null"], "enum": ["high", "medium", "low", "null"]}
                        }
                    },
                    "Artikelnummer": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["string", "null"]},
                            "source_page": {"type": ["integer", "null"]},
                            "source_region": {"type": ["string", "null"]},
                            "confidence": {"type": ["string", "null"], "enum": ["high", "medium", "low", "null"]}
                        }
                    }
                }
            }
        }"""
    pyperclip.copy(pr)
    return pr
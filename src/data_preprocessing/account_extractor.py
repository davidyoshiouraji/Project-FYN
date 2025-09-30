# Kontrollieren ob alle Überschriften und Posten passen
# In Bilanz und GuV einteilen
# Grobere Kontenübersicht erstellen, also 1000 bis 2000 und so weiter
# Code sinnvoll strukturieren
# Testen



import pandas as pd
import re
from typing import List, Tuple

def extract_datev_accounts() -> List[Tuple[str, str]]:
    """
    Extract all account numbers and descriptions from DATEV SKR 03
    Returns list of tuples: (account_number, german_description)
    """
    
    accounts = [
        ("0005", "Rückständige fällige Einzahlungen auf Geschäftsanteile"),
        ("0010", "Entgeltlich erworbene Konzessionen, gewerbliche Schutzrechte und ähnliche Rechte und Werte sowie Lizenzen an solchen Rechten und Werten"),
        ("0015", "Konzessionen"),
        ("0020", "Gewerbliche Schutzrechte"),
        ("0025", "Ähnliche Rechte und Werte"),
        ("0027", "EDV-Software"),
        ("0030", "Lizenzen an gewerblichen Schutzrechten und ähnlichen Rechten und Werten"),
        ("0035", "Geschäfts- oder Firmenwert"),
        ("0038", "Anzahlungen auf Geschäfts- oder Firmenwert"),
        ("0039", "Geleistete Anzahlungen auf immaterielle Vermögensgegenstände"),
        ("0043", "Selbst geschaffene immaterielle Vermögensgegenstände"),
        ("0044", "EDV-Software"),
        ("0045", "Lizenzen und Franchiseverträge"),
        ("0046", "Konzessionen und gewerbliche Schutzrechte"),
        ("0047", "Rezepte, Verfahren, Prototypen"),
        ("0048", "Immaterielle Vermögensgegenstände in Entwicklung"),
        
        ("0050", "Grundstücke, grundstücksgleiche Rechte und Bauten einschließlich der Bauten auf fremden Grundstücken"),
        ("0059", "Grundstücksanteil des häuslichen Arbeitszimmers"),
        ("0060", "Grundstücksgleiche Rechte ohne Bauten"),
        ("0065", "Unbebaute Grundstücke"),
        ("0070", "Grundstücksgleiche Rechte (Erbbaurecht, Dauerwohnrecht, unbebaute Grundstücke)"),
        ("0075", "Grundstücke mit Substanzverzehr"),
        ("0079", "Anzahlungen auf Grund und Boden"),
        ("0080", "Bauten auf eigenen Grundstücken und grundstücksgleichen Rechten"),
        ("0085", "Grundstückswerte eigener bebauter Grundstücke"),
        ("0090", "Geschäftsbauten"),
        ("0100", "Fabrikbauten"),
        ("0110", "Garagen"),
        ("0111", "Außenanlagen für Geschäfts-, Fabrik- und andere Bauten"),
        ("0112", "Hof- und Wegebefestigungen"),
        ("0113", "Einrichtungen für Geschäfts-, Fabrik- und andere Bauten"),
        ("0115", "Andere Bauten"),
        ("0120", "Geschäfts-, Fabrik- und andere Bauten im Bau auf eigenen Grundstücken"),
        ("0129", "Anzahlungen auf Geschäfts-, Fabrik- und andere Bauten auf eigenen Grundstücken"),
        ("0140", "Wohnbauten"),
        ("0145", "Garagen"),
        ("0146", "Außenanlagen"),
        ("0147", "Hof- und Wegebefestigungen"),
        ("0148", "Einrichtungen für Wohnbauten"),
        ("0149", "Gebäudeteil des häuslichen Arbeitszimmers"),
        ("0150", "Wohnbauten im Bau auf eigenen Grundstücken"),
        ("0159", "Anzahlungen auf Wohnbauten auf eigenen Grundstücken"),
        ("0160", "Bauten auf fremden Grundstücken"),
        ("0165", "Geschäftsbauten"),
        ("0170", "Fabrikbauten"),
        ("0175", "Garagen"),
        ("0176", "Außenanlagen"),
        ("0177", "Hof- und Wegebefestigungen"),
        ("0178", "Einrichtungen für Geschäfts-, Fabrik-, Wohn- und andere Bauten"),
        ("0179", "Andere Bauten"),
        ("0180", "Geschäfts-, Fabrik- und andere Bauten im Bau auf fremden Grundstücken"),
        ("0189", "Anzahlungen auf Geschäfts-, Fabrik- und andere Bauten auf fremden Grundstücken"),
        ("0190", "Wohnbauten"),
        ("0191", "Garagen"),
        ("0192", "Außenanlagen"),
        ("0193", "Hof- und Wegebefestigungen"),
        ("0194", "Einrichtungen für Wohnbauten"),
        ("0195", "Wohnbauten im Bau auf fremden Grundstücken"),
        ("0199", "Anzahlungen auf Wohnbauten auf fremden Grundstücken"),
        
        ("0200", "Technische Anlagen und Maschinen"),
        ("0210", "Maschinen"),
        ("0220", "Maschinengebundene Werkzeuge"),
        ("0240", "Technische Anlagen"),
        ("0260", "Transportanlagen und Ähnliches"),
        ("0280", "Betriebsvorrichtungen"),
        ("0290", "Technische Anlagen und Maschinen im Bau"),
        ("0299", "Anzahlungen auf technische Anlagen und Maschinen"),
        
        ("0300", "Andere Anlagen, Betriebs- und Geschäftsausstattung"),
        ("0310", "Andere Anlagen"),
        ("0320", "Pkw"),
        ("0350", "Lkw"),
        ("0380", "Sonstige Transportmittel"),
        ("0400", "Betriebsausstattung"),
        ("0410", "Geschäftsausstattung"),
        ("0420", "Büroeinrichtung"),
        ("0430", "Ladeneinrichtung"),
        ("0440", "Werkzeuge"),
        ("0450", "Einbauten in fremde Grundstücke"),
        ("0460", "Gerüst- und Schalungsmaterial"),
        ("0480", "Geringwertige Wirtschaftsgüter"),
        ("0485", "Wirtschaftsgüter (Sammelposten)"),
        ("0490", "Sonstige Betriebs- und Geschäftsausstattung"),
        ("0498", "Andere Anlagen, Betriebs- und Geschäftsausstattung im Bau"),
        ("0499", "Anzahlungen auf andere Anlagen, Betriebs- und Geschäftsausstattung"),
        
        ("0500", "Anteile an verbundenen Unternehmen (Anlagevermögen)"),
        ("0501", "Anteile an verbundenen Unternehmen, Personengesellschaften"),
        ("0502", "Anteile an verbundenen Unternehmen, Kapitalgesellschaften"),
        ("0503", "Anteile an herrschender oder mehrheitlich beteiligter Gesellschaft, Kapitalgesellschaften"),
        ("0504", "Anteile an herrschender oder mehrheitlich beteiligter Gesellschaft"),
        ("0505", "Ausleihungen an verbundene Unternehmen"),
        ("0506", "Ausleihungen an verbundene Unternehmen, Personengesellschaften"),
        ("0507", "Ausleihungen an verbundene Unternehmen, Kapitalgesellschaften"),
        ("0508", "Ausleihungen an verbundene Unternehmen, Einzelunternehmen"),
        ("0509", "Anteile an herrschender oder mehrheitlich beteiligter Gesellschaft, Personengesellschaften"),
        ("0510", "Beteiligungen"),
        ("0513", "Typisch stille Beteiligungen"),
        ("0516", "Atypisch stille Beteiligungen"),
        ("0517", "Beteiligungen an Kapitalgesellschaften"),
        ("0518", "Beteiligungen an Personengesellschaften"),
        ("0519", "Beteiligung einer GmbH & Co. KG an einer Komplementär GmbH"),
        ("0520", "Ausleihungen an Unternehmen, mit denen ein Beteiligungsverhältnis besteht"),
        ("0523", "Ausleihungen an Unternehmen, mit denen ein Beteiligungsverhältnis besteht, Personengesellschaften"),
        ("0524", "Ausleihungen an Unternehmen, mit denen ein Beteiligungsverhältnis besteht, Kapitalgesellschaften"),
        ("0525", "Wertpapiere des Anlagevermögens"),
        ("0530", "Wertpapiere mit Gewinnbeteiligungsansprüchen, die dem Teileinküfteverfahren unterliegen"),
        ("0535", "Festverzinsliche Wertpapiere"),
        ("0538", "Anteile einer GmbH & Co. KG an einer Komplementär-GmbH"),
        ("0540", "Übrige sonstige Ausleihungen"),
        ("0550", "Darlehen"),
        ("0570", "Genossenschaftsanteile zum langfristigen Verbleib"),
        ("0580", "Ausleihungen an Gesellschafter"),
        ("0582", "Ausleihungen an GmbH-Gesellschafter"),
        ("0584", "Ausleihungen an persönlich haftende Gesellschafter"),
        ("0586", "Ausleihungen an Kommanditisten"),
        ("0590", "Ausleihungen an nahe stehende Personen"),
        ("0595", "Rückdeckungsansprüche aus Lebensversicherungen zum langfristigen Verbleib"),
        
        ("0600", "Anleihen nicht konvertibel"),
        ("0601", "- Restlaufzeit bis 1 Jahr"),
        ("0605", "- Restlaufzeit 1 bis 5 Jahre"),
        ("0610", "- Restlaufzeit größer 5 Jahre"),
        ("0615", "Anleihen konvertibel"),
        ("0616", "- Restlaufzeit bis 1 Jahr"),
        ("0620", "- Restlaufzeit 1 bis 5 Jahre"),
        ("0625", "- Restlaufzeit größer 5 Jahre"),
        ("0630", "Verbindlichkeiten gegenüber Kreditinstituten"),
        ("0631", "- Restlaufzeit bis 1 Jahr"),
        ("0640", "- Restlaufzeit 1 bis 5 Jahre"),
        ("0650", "- Restlaufzeit größer 5 Jahre"),
        ("0660", "Verbindlichkeiten gegenüber Kreditinstituten aus Teilzahlungsverträgen"),
        ("0661", "- Restlaufzeit bis 1 Jahr"),
        ("0670", "- Restlaufzeit 1 bis 5 Jahre"),
        ("0680", "- Restlaufzeit größer 5 Jahre"),
        ("0690", "Verbindlichkeiten gegenüber Kreditinstituten, vor Restlaufzeitdifferenzierung"),
        ("0699", "Gegenkonto 0630-0689 bei Aufteilung der Konten 0690-0698"),
        
        ("0700", "Verbindlichkeiten gegenüber verbundenen Unternehmen"),
        ("0701", "- Restlaufzeit bis 1 Jahr"),
        ("0705", "- Restlaufzeit 1 bis 5 Jahre"),
        ("0710", "- Restlaufzeit größer 5 Jahre"),
        ("0715", "Verbindlichkeiten gegenüber Unternehmen, mit denen ein Beteiligungsverhältnis besteht"),
        ("0716", "- Restlaufzeit bis 1 Jahr"),
        ("0720", "- Restlaufzeit 1 bis 5 Jahre"),
        ("0725", "- Restlaufzeit größer 5 Jahre"),
        ("0730", "Verbindlichkeiten gegenüber Gesellschaftern"),
        ("0731", "- Restlaufzeit bis 1 Jahr"),
        ("0740", "- Restlaufzeit 1 bis 5 Jahre"),
        ("0750", "- Restlaufzeit größer 5 Jahre"),
        ("0755", "Verbindlichkeiten gegenüber Gesellschaftern für offene Ausschüttungen"),
        ("0760", "Verbindlichkeiten gegenüber typisch stillen Gesellschaftern"),
        ("0761", "- Restlaufzeit bis 1 Jahr"),
        ("0764", "- Restlaufzeit 1 bis 5 Jahre"),
        ("0767", "- Restlaufzeit größer 5 Jahre"),
        ("0770", "Verbindlichkeiten gegenüber atypisch stillen Gesellschaftern"),
        ("0771", "- Restlaufzeit bis 1 Jahr"),
        ("0774", "- Restlaufzeit 1 bis 5 Jahre"),
        ("0777", "- Restlaufzeit größer 5 Jahre"),
        ("0780", "Partiarische Darlehen"),
        ("0781", "- Restlaufzeit bis 1 Jahr"),
        ("0784", "- Restlaufzeit 1 bis 5 Jahre"),
        ("0787", "- Restlaufzeit größer 5 Jahre"),
        ("0790", "Sonstige Verbindlichkeiten, vor Restlaufzeitdifferenzierung (nur Bilanzierer)"),
        ("0799", "Gegenkonto 0730-0789 und 1665-1678 und 1695-1698 bei Aufteilung der Konten 0790-0798"),
        
        ("0800", "Gezeichnetes Kapital"),
        ("0809", "Kapitalerhöhung aus Gesellschaftsmitteln"),
        ("0810", "Geschäftsguthaben der verbleibenden Mitglieder"),
        ("0811", "Geschäftsguthaben der ausscheidenden Mitglieder"),
        ("0812", "Geschäftsguthaben aus gekündigten Geschäftsanteilen"),
        ("0813", "Rückständige fällige Einzahlungen auf Geschäftsanteile, vermerkt"),
        ("0815", "Gegenkonto Rückständige fällige Einzahlungen auf Geschäftsanteile, vermerkt"),
        ("0819", "Erworbene eigene Anteile"),
        ("0839", "Nachschüsse (Forderungen, Gegenkonto 0845)"),
        ("0840", "Kapitalrücklage"),
        ("0841", "Kapitalrücklage durch Ausgabe von Anteilen über Nennbetrag"),
        ("0842", "Kapitalrücklage durch Ausgabe von Schuldverschreibungen für Wandlungsrechte und Optionsrechte zum Erwerb von Anteilen"),
        ("0843", "Kapitalrücklage durch Zuzahlungen gegen Gewährung eines Vorzugs für Anteile"),
        ("0844", "Kapitalrücklage durch andere Zuzahlungen in das Eigenkapital"),
        ("0845", "Nachschusskapital (Gegenkonto 0839)"),
        ("0846", "Gesetzliche Rücklage"),
        ("0848", "Andere Gewinnrücklagen aus dem Erwerb eigener Anteile"),
        ("0849", "Rücklage für Anteile an einem herrschenden oder mehrheitlich beteiligten Unternehmen"),
        ("0851", "Satzungsmäßige Rücklagen"),
        ("0852", "Andere Ergebnisrücklagen"),
        ("0853", "Gewinnrücklagen aus den Übergangsvorschriften BilMoG"),
        ("0854", "Gewinnrücklagen aus den Übergangsvorschriften BilMoG (Zuschreibung Sachanlagevermögen)"),
        ("0855", "Andere Gewinnrücklagen"),
        ("0856", "Eigenkapitalanteil von Wertaufholungen"),
        ("0857", "Gewinnrücklagen aus den Übergangsvorschriften BilMoG (Zuschreibung Finanzanlagevermögen)"),
        ("0858", "Gewinnrücklagen aus den Übergangsvorschriften BilMoG (Auflösung der Sonderposten mit Rücklageanteil)"),
        ("0859", "Latente Steuern (Gewinnrücklage Haben) aus erfolgsneutralen Verrechnungen"),
        ("0860", "Gewinnvortrag vor Verwendung"),
        ("0865", "Gewinnvortrag vor Verwendung (mit Aufteilung für Kapitalkontenentwicklung)"),
        ("0867", "Verlustvortrag vor Verwendung (mit Aufteilung für Kapitalkontenentwicklung)"),
        ("0868", "Verlustvortrag vor Verwendung"),
        
        ("0870", "Festkapital"),
        ("0871", "Kapital (fester Anteil, nur Einzelunternehmen)"),
        ("0880", "Variables Kapital"),
        ("0881", "Kapital (variabler Anteil, nur Einzelunternehmen)"),
        ("0890", "Gesellschafter-Darlehen"),
        ("0900", "Kommandit-Kapital"),
        ("0910", "Verlustausgleichskonto"),
        ("0920", "Gesellschafter-Darlehen"),
        
        ("0930", "Übrige andere Sonderposten"),
        ("0931", "Steuerfreie Rücklagen nach § 6b EStG"),
        ("0932", "Rücklage für Ersatzbeschaffung"),
        ("0940", "Sonderposten mit Rücklageanteil, Sonderabschreibungen"),
        ("0945", "Ausgleichsposten bei Entnahmen § 4g EStG"),
        ("0946", "Rücklage für Zuschüsse"),
        ("0947", "Sonderposten mit Rücklageanteil nach § 7g Abs. 5 EStG"),
        ("0948", "Sonderposten für Zuschüsse Dritter"),
        ("0949", "Sonderposten für Investitionszulagen"),
        
        ("0950", "Rückstellungen für Pensionen und ähnliche Verpflichtungen"),
        ("0951", "Rückstellungen für Pensionen und ähnliche Verpflichtungen zur Saldierung mit Vermögensgegenständen zum langfristigen Verbleib nach § 246 Abs. 2 HGB"),
        ("0952", "Rückstellungen für Pensionen und ähnliche Verpflichtungen gegenüber Gesellschaftern oder nahe stehenden Personen"),
        ("0953", "Rückstellungen für Direktzusagen"),
        ("0954", "Rückstellungen für Zuschussverpflichtungen für Pensionskassen und Lebensversicherungen"),
        ("0955", "Steuerrückstellungen"),
        ("0956", "Gewerbesteuerrückstellung nach § 4 Abs. 5b EStG"),
        ("0961", "Urlaubsrückstellungen"),
        ("0962", "Steuerrückstellung aus Steuerstundung (BStBK)"),
        ("0963", "Körperschaftsteuerrückstellung"),
        ("0964", "Rückstellungen für mit der Altersversorgung vergleichbare langfristige Verpflichtungen zum langfristigen Verbleib"),
        ("0965", "Rückstellungen für Personalkosten"),
        ("0966", "Rückstellungen zur Erfüllung der Aufbewahrungspflichten"),
        ("0967", "Rückstellungen für mit der Altersversorgung vergleichbare langfristige Verpflichtungen zur Saldierung mit Vermögensgegenständen zum langfristigen Verbleib nach § 246 Abs. 2 HGB"),
        ("0968", "Passive latente Steuern"),
        ("0969", "Rückstellung für latente Steuern"),
        ("0970", "Sonstige Rückstellungen"),
        ("0971", "Rückstellungen für unterlassene Aufwendungen für Instandhaltung, Nachholung in den ersten drei Monaten"),
        ("0973", "Rückstellungen für Abraum- und Abfallbeseitigung"),
        ("0974", "Rückstellungen für Gewährleistungen (Gegenkonto 4790)"),
        ("0976", "Rückstellungen für drohende Verluste aus schwebenden Geschäften"),
        ("0977", "Rückstellungen für Abschluss- und Prüfungskosten"),
        ("0978", "Aufwandsrückstellungen nach § 249 Abs. 2 HGB a. F."),
        ("0979", "Rückstellungen für Umweltschutz"),
        
        ("0980", "Aktive Rechnungsabgrenzung"),
        ("0983", "Aktive latente Steuern"),
        ("0984", "Als Aufwand berücksichtigte Zölle und Verbrauchsteuern auf Vorräte"),
        ("0985", "Als Aufwand berücksichtigte Umsatzsteuer auf Anzahlungen"),
        ("0986", "Damnum/Disagio"),
        ("0987", "Rechnungsabgrenzungsposten (Gewinnrücklage Soll) aus erfolgsneutralen Verrechnungen"),
        ("0988", "Latente Steuern (Gewinnrücklage Soll) aus erfolgsneutralen Verrechnungen"),
        ("0989", "Gesamthänderisch gebundene Rücklagen (mit Aufteilung für Kapitalkontenentwicklung)"),
        ("0990", "Passive Rechnungsabgrenzung"),
        ("0992", "Abgrenzungen unterjährig pauschal gebuchter Abschreibungen für BWA"),
        ("0996", "Pauschalwertberichtigung auf Forderungen - Restlaufzeit bis zu 1 Jahr"),
        ("0997", "- Restlaufzeit größer 1 Jahr"),
        ("0998", "Einzelwertberichtigungen auf Forderungen - Restlaufzeit bis zu 1 Jahr"),
        ("0999", "- Restlaufzeit größer 1 Jahr"),
        
        ("1000", "Kasse"),
        ("1010", "Nebenkasse 1"),
        ("1020", "Nebenkasse 2"),
        ("1100", "Bank (Postbank)"),
        ("1110", "Bank (Postbank 1)"),
        ("1120", "Bank (Postbank 2)"),
        ("1130", "Bank (Postbank 3)"),
        ("1190", "LZB-Guthaben"),
        ("1195", "Bundesbankguthaben"),
        ("1200", "Bank"),
        ("1210", "Bank 1"),
        ("1220", "Bank 2"),
        ("1230", "Bank 3"),
        ("1240", "Bank 4"),
        ("1250", "Bank 5"),
        ("1290", "Finanzmittelanlagen im Rahmen der kurzfristigen Finanzdisposition (nicht im Finanzmittelfonds enthalten)"),
        ("1295", "Verbindlichkeiten gegenüber Kreditinstituten (nicht im Finanzmittelfonds enthalten)"),
        ("1329", "Andere Wertpapiere mit unwesentlichen Wertschwankungen"),
        ("1330", "Schecks"),
        ("1340", "Anteile an verbundenen Unternehmen (Umlaufvermögen)"),
        ("1344", "Anteile an herrschender oder mit Mehrheit beteiligter Gesellschaft"),
        ("1348", "Sonstige Wertpapiere"),
        ("1349", "Wertpapieranlagen im Rahmen der kurzfristigen Finanzdisposition"),
        ("1350", "GmbH-Anteile zum kurzfristigen Verbleib"),
        ("1352", "Genossenschaftsanteile zum kurzfristigen Verbleib"),
        ("1353", "Vermögensgegenstände zur Erfüllung von mit der Altersversorgung vergleichbaren langfristigen Verpflichtungen"),
        ("1354", "Vermögensgegenstände zur Saldierung mit der Altersversorgung vergleichbaren langfristigen Verpflichtungen nach § 246 Abs. 2 HGB"),
        ("1355", "Ansprüche aus Rückdeckungsversicherungen"),
        ("1356", "Vermögensgegenstände zur Erfüllung von Pensionsrückstellungen und ähnlichen Verpflichtungen zum langfristigen Verbleib"),
        ("1357", "Vermögensgegenstände zur Saldierung mit Pensionsrückstellungen und ähnlichen Verpflichtungen zum langfristigen Verbleib nach § 246 Abs. 2 HGB"),
        ("1360", "Geldtransit"),
        ("1371", "Verrechnungskonto Gewinnermittlung § 4 Abs. 3 EStG, nicht ergebniswirksam"),
        ("1372", "Wirtschaftsgüter des Umlaufvermögens nach § 4 Abs. 3 Satz 4 EStG"),
        ("1376", "Forderungen gegen typisch stille Gesellschafter"),
        ("1377", "- Restlaufzeit bis 1 Jahr"),
        ("1378", "- Restlaufzeit größer 1 Jahr"),
        ("1380", "Überleitungskonto Kostenstelle"),
        ("1381", "Forderungen gegen GmbH-Gesellschafter"),
        ("1382", "- Restlaufzeit bis 1 Jahr"),
        ("1383", "- Restlaufzeit größer 1 Jahr"),
        ("1385", "Forderungen gegen persönlich haftende Gesellschafter"),
        ("1386", "- Restlaufzeit bis 1 Jahr"),
        ("1387", "- Restlaufzeit größer 1 Jahr"),
        ("1389", "Ansprüche aus betrieblicher Altersversorgung und Pensionsansprüche (Mitunternehmer)"),
        ("1390", "Verrechnungskonto Ist-Versteuerung"),
        ("1391", "Neutralisierung ertragswirksamer Sachverhalte für § 4 Abs. 3 EStG"),
        ("1394", "Forderungen gegen Gesellschaft/Gesamthand"),
        ("1400", "Forderungen aus Lieferungen und Leistungen"),
        ("1410", "Forderungen aus Lieferungen und Leistungen ohne Kontokorrent"),
        ("1445", "Forderungen aus Lieferungen und Leistungen zum allgemeinen Umsatzsteuersatz oder eines Kleinunternehmers (EÜR)"),
        ("1446", "Forderungen aus Lieferungen und Leistungen zum ermäßigten Umsatzsteuersatz (EÜR)"),
        ("1447", "Forderungen aus steuerfreien oder nicht steuerbaren Lieferungen und Leistungen (EÜR)"),
        ("1448", "Forderungen aus Lieferungen und Leistungen nach Durchschnittssätzen nach § 24 UStG (EÜR)"),
        ("1449", "Gegenkonto 1445-1448 bei Aufteilung der Forderungen nach Steuersätzen (EÜR)"),
        ("1450", "Forderungen nach § 11 Abs. 1 Satz 2 EStG für § 4 Abs. 3 EStG"),
        ("1451", "Forderungen aus Lieferungen und Leistungen ohne Kontokorrent - Restlaufzeit bis 1 Jahr"),
        ("1455", "- Restlaufzeit größer 1 Jahr"),
        ("1460", "Zweifelhafte Forderungen"),
        ("1461", "- Restlaufzeit bis 1 Jahr"),
        ("1465", "- Restlaufzeit größer 1 Jahr"),
        ("1470", "Forderungen aus Lieferungen und Leistungen gegen verbundene Unternehmen"),
        ("1471", "- Restlaufzeit bis 1 Jahr"),
        ("1475", "- Restlaufzeit größer 1 Jahr"),
        ("1478", "Wertberichtigungen auf Forderungen gegen verbundene Unternehmen - Restlaufzeit bis 1 Jahr"),
        ("1479", "- Restlaufzeit größer 1 Jahr"),
        ("1480", "Forderungen aus Lieferungen und Leistungen gegen Unternehmen, mit denen ein Beteiligungsverhältnis besteht"),
        ("1481", "- Restlaufzeit bis 1 Jahr"),
        ("1485", "- Restlaufzeit größer 1 Jahr"),
        ("1488", "Wertberichtigungen auf Forderungen gegen Unternehmen, mit denen ein Beteiligungsverhältnis besteht - Restlaufzeit bis 1 Jahr"),
        ("1489", "- Restlaufzeit größer 1 Jahr"),
        ("1490", "Forderungen aus Lieferungen und Leistungen gegen Gesellschafter"),
        ("1491", "- Restlaufzeit bis 1 Jahr"),
        ("1495", "- Restlaufzeit größer 1 Jahr"),
        ("1498", "Gegenkonto zu sonstigen Vermögensgegenständen bei Buchungen über Debitorenkonto"),
        ("1499", "Gegenkonto 1451-1497 bei Aufteilung Debitorenkonto"),
        
        ("1500", "Sonstige Vermögensgegenstände"),
        ("1501", "- Restlaufzeit bis 1 Jahr"),
        ("1502", "- Restlaufzeit größer 1 Jahr"),
        ("1503", "Forderungen gegen Vorstandsmitglieder und Geschäftsführer - Restlaufzeit bis 1 Jahr"),
        ("1504", "- Restlaufzeit größer 1 Jahr"),
        ("1505", "Forderungen gegen Aufsichtsrats- und Beiratsmitglieder - Restlaufzeit bis 1 Jahr"),
        ("1506", "- Restlaufzeit größer 1 Jahr"),
        ("1507", "Forderungen gegen sonstige Gesellschafter - Restlaufzeit bis 1 Jahr"),
        ("1508", "- Restlaufzeit größer 1 Jahr"),
        ("1510", "Geleistete Anzahlungen auf Vorräte"),
        ("1511", "Geleistete Anzahlungen, 7 % Vorsteuer"),
        ("1512", "Geleistete Anzahlungen, 5 % Vorsteuer"),
        ("1517", "Geleistete Anzahlungen, 16 % Vorsteuer"),
        ("1518", "Geleistete Anzahlungen, 19 % Vorsteuer"),
        ("1519", "Forderungen gegen Arbeitsgemeinschaften"),
        ("1520", "Forderungen gegenüber Krankenkassen aus Aufwendungsausgleichsgesetz"),
        ("1521", "Agenturwarenabrechnung"),
        ("1522", "Genussrechte"),
        ("1524", "Einzahlungsansprüche zu Nebenleistungen oder Zuzahlungen"),
        ("1525", "Kautionen"),
        ("1526", "- Restlaufzeit bis 1 Jahr"),
        ("1527", "- Restlaufzeit größer 1 Jahr"),
        ("1528", "Nachträglich abziehbare Vorsteuer nach § 15a Abs. 2 UStG"),
        ("1529", "Zurückzuzahlende Vorsteuer nach § 15a Abs. 2 UStG"),
        ("1530", "Forderungen gegen Personal aus Lohn- und Gehaltsabrechnung"),
        ("1531", "- Restlaufzeit bis 1 Jahr"),
        ("1537", "- Restlaufzeit größer 1 Jahr"),
        ("1539", "Umsatzsteuerforderungen frühere Jahre"),
        ("1540", "Forderungen aus Gewerbesteuerüberzahlungen"),
        ("1542", "Steuererstattungsansprüche gegenüber anderen Ländern"),
        ("1543", "Forderungen an das Finanzamt aus abgeführtem Bauabzugsbetrag"),
        ("1544", "Forderung gegenüber Bundesagentur für Arbeit"),
        ("1545", "Forderungen aus Umsatzsteuer-Vorauszahlungen"),
        ("1546", "Umsatzsteuerforderungen Vorjahr"),
        ("1547", "Forderungen aus entrichteten Verbrauchsteuern"),
        ("1548", "Vorsteuer in Folgeperiode/im Folgejahr abziehbar"),
        ("1549", "Körperschaftsteuerrückforderung"),
        ("1550", "Darlehen"),
        ("1551", "- Restlaufzeit bis 1 Jahr"),
        ("1555", "- Restlaufzeit größer 1 Jahr"),
        ("1556", "Nachträglich abziehbare Vorsteuer nach § 15a Abs. 1 UStG, bewegliche Wirtschaftsgüter"),
        ("1557", "Zurückzuzahlende Vorsteuer nach § 15a Abs. 1 UStG, bewegliche Wirtschaftsgüter"),
        ("1558", "Nachträglich abziehbare Vorsteuer nach § 15a Abs. 1 UStG, unbewegliche Wirtschaftsgüter"),
        ("1559", "Zurückzuzahlende Vorsteuer nach § 15a Abs. 1 UStG, unbewegliche Wirtschaftsgüter"),
        ("1560", "Aufzuteilende Vorsteuer"),
        ("1561", "Aufzuteilende Vorsteuer 7 %"),
        ("1562", "Aufzuteilende Vorsteuer aus innergemeinschaftlichem Erwerb"),
        ("1563", "Aufzuteilende Vorsteuer aus innergemeinschaftlichem Erwerb 19 %"),
        ("1566", "Aufzuteilende Vorsteuer 19 %"),
        ("1567", "Aufzuteilende Vorsteuer nach §§ 13a und 13b UStG"),
        ("1569", "Aufzuteilende Vorsteuer nach §§ 13a und 13b UStG 19 %"),
        ("1570", "Abziehbare Vorsteuer"),
        ("1571", "Abziehbare Vorsteuer 7 %"),
        ("1572", "Abziehbare Vorsteuer aus innergemeinschaftlichem Erwerb"),
        ("1573", "Vorsteuer aus Erwerb als letzter Abnehmer innerhalb eines Dreiecksgeschäfts"),
        ("1574", "Abziehbare Vorsteuer aus innergemeinschaftlichem Erwerb 19 %"),
        ("1576", "Abziehbare Vorsteuer 19 %"),
        ("1577", "Abziehbare Vorsteuer nach § 13b UStG 19 %"),
        ("1578", "Abziehbare Vorsteuer nach § 13b UStG"),
        ("1580", "Gegenkonto Vorsteuer § 4 Abs. 3 EStG"),
        ("1581", "Auflösung Vorsteuer aus Vorjahr § 4 Abs. 3 EStG"),
        ("1582", "Vorsteuer aus Investitionen § 4 Abs. 3 EStG"),
        ("1584", "Abziehbare Vorsteuer aus innergemeinschaftlichem Erwerb von Neufahrzeugen von Lieferanten ohne USt-Id-Nr."),
        ("1585", "Abziehbare Vorsteuer aus der Auslagerung von Gegenständen aus einem Umsatzsteuerlager"),
        ("1588", "Entstandene Einfuhrumsatzsteuer"),
        ("1590", "Durchlaufende Posten"),
        ("1592", "Fremdgeld"),
        ("1593", "Verrechnungskonto erhaltene Anzahlungen bei Buchung über Debitorenkonto"),
        ("1594", "Forderungen gegen verbundene Unternehmen"),
        ("1595", "- Restlaufzeit bis 1 Jahr"),
        ("1596", "- Restlaufzeit größer 1 Jahr"),
        ("1597", "Forderungen gegen Unternehmen, mit denen ein Beteiligungsverhältnis besteht"),
        ("1598", "- Restlaufzeit bis 1 Jahr"),
        ("1599", "- Restlaufzeit größer 1 Jahr"),
        
        ("1600", "Verbindlichkeiten aus Lieferungen und Leistungen"),
        ("1605", "Verbindlichkeiten aus Lieferungen und Leistungen zum allgemeinen Umsatzsteuersatz (EÜR)"),
        ("1606", "Verbindlichkeiten aus Lieferungen und Leistungen zum ermäßigten Umsatzsteuersatz (EÜR)"),
        ("1607", "Verbindlichkeiten aus Lieferungen und Leistungen ohne Vorsteuerabzug (EÜR)"),
        ("1609", "Gegenkonto 1605-1607 bei Aufteilung der Verbindlichkeiten nach Steuersätzen (EÜR)"),
        ("1610", "Verbindlichkeiten aus Lieferungen und Leistungen ohne Kontokorrent"),
        ("1624", "Verbindlichkeiten aus Lieferungen und Leistungen für Investitionen für § 4 Abs. 3 EStG"),
        ("1625", "Verbindlichkeiten aus Lieferungen und Leistungen ohne Kontokorrent - Restlaufzeit bis 1 Jahr"),
        ("1626", "- Restlaufzeit 1 bis 5 Jahre"),
        ("1628", "- Restlaufzeit größer 5 Jahre"),
        ("1630", "Verbindlichkeiten aus Lieferungen und Leistungen gegenüber verbundenen Unternehmen"),
        ("1631", "- Restlaufzeit bis 1 Jahr"),
        ("1635", "- Restlaufzeit 1 bis 5 Jahre"),
        ("1638", "- Restlaufzeit größer 5 Jahre"),
        ("1640", "Verbindlichkeiten aus Lieferungen und Leistungen gegenüber Unternehmen, mit denen ein Beteiligungsverhältnis besteht"),
        ("1641", "- Restlaufzeit bis 1 Jahr"),
        ("1645", "- Restlaufzeit 1 bis 5 Jahre"),
        ("1648", "- Restlaufzeit größer 5 Jahre"),
        ("1650", "Verbindlichkeiten aus Lieferungen und Leistungen gegenüber Gesellschaftern"),
        ("1651", "- Restlaufzeit bis 1 Jahr"),
        ("1655", "- Restlaufzeit 1 bis 5 Jahre"),
        ("1658", "- Restlaufzeit größer 5 Jahre"),
        ("1659", "Gegenkonto 1625-1658 bei Aufteilung Kreditorenkonto"),
        ("1665", "Verbindlichkeiten gegenüber GmbH-Gesellschaftern"),
        ("1666", "- Restlaufzeit bis 1 Jahr"),
        ("1667", "- Restlaufzeit 1 bis 5 Jahre"),
        ("1668", "- Restlaufzeit größer 5 Jahre"),
        ("1670", "Verbindlichkeiten gegenüber persönlich haftenden Gesellschaftern"),
        ("1671", "- Restlaufzeit bis 1 Jahr"),
        ("1672", "- Restlaufzeit 1 bis 5 Jahre"),
        ("1673", "- Restlaufzeit größer 5 Jahre"),
        ("1675", "Verbindlichkeiten gegenüber Kommanditisten"),
        ("1676", "- Restlaufzeit bis 1 Jahr"),
        ("1677", "- Restlaufzeit 1 bis 5 Jahre"),
        ("1678", "- Restlaufzeit größer 5 Jahre"),
        ("1691", "Verbindlichkeiten gegenüber Arbeitsgemeinschaften"),
        ("1692", "Neutralisierung aufwandswirksamer Sachverhalte für § 4 Abs. 3 EStG"),
        ("1693", "Ergebnisneutrale Sachverhalte für § 4 Abs. 3 EStG"),
        ("1695", "Verbindlichkeiten gegenüber stillen Gesellschaftern"),
        ("1696", "- Restlaufzeit bis 1 Jahr"),
        ("1697", "- Restlaufzeit 1 bis 5 Jahre"),
        ("1698", "- Restlaufzeit größer 5 Jahre"),
        
        ("1700", "Sonstige Verbindlichkeiten"),
        ("1701", "- Restlaufzeit bis 1 Jahr"),
        ("1702", "- Restlaufzeit 1 bis 5 Jahre"),
        ("1703", "- Restlaufzeit größer 5 Jahre"),
        ("1704", "Sonstige Verbindlichkeiten nach § 11 Abs. 2 Satz 2 EStG für § 4 Abs. 3 EStG"),
        ("1705", "Darlehen"),
        ("1706", "- Restlaufzeit bis 1 Jahr"),
        ("1707", "- Restlaufzeit 1 bis 5 Jahre"),
        ("1708", "- Restlaufzeit größer 5 Jahre"),
        ("1709", "Gewinnverfügungskonto stille Gesellschafter - sonstige Verbindlichkeiten"),
        
        ("1710", "Erhaltene Anzahlungen auf Bestellungen (Verbindlichkeiten)"),
        ("1711", "Erhaltene, versteuerte Anzahlungen 7 % USt (Verbindlichkeiten)"),
        ("1712", "Erhaltene, versteuerte Anzahlungen 5 % USt (Verbindlichkeiten)"),
        ("1714", "Erhaltene, versteuerte Anzahlungen 0 % USt (Verbindlichkeiten)"),
        ("1715", "Erhaltene Anzahlungen - Nachsteuer"),
        ("1717", "Erhaltene, versteuerte Anzahlungen 16 % USt (Verbindlichkeiten)"),
        ("1718", "Erhaltene, versteuerte Anzahlungen 19 % USt (Verbindlichkeiten)"),
        ("1719", "Erhaltene Anzahlungen - Restlaufzeit bis 1 Jahr"),
        ("1720", "- Restlaufzeit 1 bis 5 Jahre"),
        ("1721", "- Restlaufzeit größer 5 Jahre"),
        ("1722", "Erhaltene Anzahlungen auf Bestellungen (von Vorräten offen abgesetzt)"),
        
        ("1725", "Umsatzsteuer in Folgeperiode fällig (§§ 13 Abs. 1 Nr. 6 und 13b Abs. 2 UStG)"),
        ("1728", "Umsatzsteuer aus im anderen EU-Land steuerpflichtigen elektronischen Dienstleistungen"),
        ("1729", "Steuerzahlungen aus im anderen EU-Land steuerpflichtigen Leistungen"),
        ("1730", "Kreditkartenabrechnung"),
        ("1731", "Agenturwarenabrechnung"),
        ("1732", "Erhaltene Kautionen"),
        ("1733", "- Restlaufzeit bis 1 Jahr"),
        ("1734", "- Restlaufzeit 1 bis 5 Jahre"),
        ("1735", "- Restlaufzeit größer 5 Jahre"),
        ("1736", "Verbindlichkeiten aus Steuern und Abgaben"),
        ("1737", "- Restlaufzeit bis 1 Jahr"),
        ("1738", "- Restlaufzeit 1 bis 5 Jahre"),
        ("1739", "- Restlaufzeit größer 5 Jahre"),
        ("1740", "Verbindlichkeiten aus Lohn und Gehalt"),
        ("1741", "Verbindlichkeiten aus Lohn- und Kirchensteuer"),
        ("1742", "Verbindlichkeiten im Rahmen der sozialen Sicherheit"),
        ("1743", "- Restlaufzeit bis 1 Jahr"),
        ("1744", "- Restlaufzeit 1 bis 5 Jahre"),
        ("1745", "- Restlaufzeit größer 5 Jahre"),
        ("1746", "Verbindlichkeiten aus Einbehaltungen (KapESt und SolZ, KiSt auf KapESt) für offene Ausschüttungen"),
        ("1747", "Verbindlichkeiten für Verbrauchsteuern"),
        ("1748", "Verbindlichkeiten für Einbehaltungen von Arbeitnehmern"),
        ("1749", "Verbindlichkeiten an das Finanzamt aus abzuführendem Bauabzugsbetrag"),
        ("1750", "Verbindlichkeiten aus Vermögensbildung"),
        ("1751", "- Restlaufzeit bis 1 Jahr"),
        ("1752", "- Restlaufzeit 1 bis 5 Jahre"),
        ("1753", "- Restlaufzeit größer 5 Jahre"),
        ("1754", "Steuerzahlungen an andere Länder"),
        ("1755", "Lohn- und Gehaltsverrechnung"),
        ("1756", "Lohn- und Gehaltsverrechnung nach § 11 Abs. 2 Satz 2 EStG für § 4 Abs. 3 EStG"),
        ("1757", "Verbindlichkeiten gegenüber Gesellschaft/Gesamthand"),
        ("1758", "Sonstige Verbindlichkeiten aus genossenschaftlicher Rückvergütung"),
        ("1759", "Voraussichtliche Beitragsschuld gegenüber den Sozialversicherungsträgern"),
        
        ("1760", "Umsatzsteuer nicht fällig"),
        ("1761", "Umsatzsteuer nicht fällig 7 %"),
        ("1762", "Umsatzsteuer nicht fällig aus im Inland steuerpflichtigen EU-Lieferungen"),
        ("1764", "Umsatzsteuer nicht fällig aus im Inland steuerpflichtigen EU-Lieferungen 19 %"),
        ("1766", "Umsatzsteuer nicht fällig 19 %"),
        ("1767", "Umsatzsteuer aus im anderen EU-Land steuerpflichtigen Lieferungen"),
        ("1768", "Umsatzsteuer aus im anderen EU-Land steuerpflichtigen sonstigen Leistungen/Werklieferungen"),
        ("1769", "Umsatzsteuer aus der Auslagerung von Gegenständen aus einem Umsatzsteuerlager"),
        ("1770", "Umsatzsteuer"),
        ("1771", "Umsatzsteuer 7 %"),
        ("1772", "Umsatzsteuer aus innergemeinschaftlichem Erwerb"),
        ("1774", "Umsatzsteuer aus innergemeinschaftlichem Erwerb 19 %"),
        ("1776", "Umsatzsteuer 19 %"),
        ("1777", "Umsatzsteuer aus im Inland steuerpflichtigen EU-Lieferungen"),
        ("1778", "Umsatzsteuer aus im Inland steuerpflichtigen EU-Lieferungen 19 %"),
        ("1779", "Umsatzsteuer aus innergemeinschaftlichem Erwerb ohne Vorsteuerabzug"),
        ("1780", "Umsatzsteuer-Vorauszahlungen"),
        ("1781", "Umsatzsteuer-Vorauszahlungen 1/11"),
        ("1782", "Nachsteuer, UStVA Kz. 65"),
        ("1783", "In Rechnung unrichtig oder unberechtigt ausgewiesene Steuerbeträge, UStVA Kz. 69"),
        ("1784", "Umsatzsteuer aus innergemeinschaftlichem Erwerb von Neufahrzeugen von Lieferanten ohne Umsatzsteuer-Identifikationsnummer"),
        ("1785", "Umsatzsteuer nach § 13b UStG"),
        ("1787", "Umsatzsteuer nach § 13b UStG 19 %"),
        ("1788", "Einfuhrumsatzsteuer aufgeschoben"),
        ("1789", "Umsatzsteuer laufendes Jahr"),
        ("1790", "Umsatzsteuerverbindlichkeiten Vorjahr"),
        ("1791", "Umsatzsteuerverbindlichkeiten frühere Jahre"),
        ("1792", "Sonstige Verrechnungskonten (Interimskonten)"),
        ("1793", "Verrechnungskonto geleistete Anzahlungen bei Buchung über Kreditorenkonto"),
        ("1794", "Umsatzsteuer aus Erwerb als letzter Abnehmer innerhalb eines Dreiecksgeschäfts"),
        ("1795", "Verbindlichkeiten im Rahmen der sozialen Sicherheit für § 4 Abs. 3 EStG"),
        ("1796", "Ausgegebene Geschenkgutscheine"),
        ("1797", "Verbindlichkeiten aus Umsatzsteuer-Vorauszahlungen"),
        ("1798", "Umsatzsteuer aus im Inland steuerpflichtigen EU-Lieferungen, nur OSS"),
        
        ("1800", "Privatentnahmen allgemein"),
        ("1801", "Privatentnahmen allgemein (nur Einzelunternehmen)"),
        ("1810", "Privatsteuern"),
        ("1811", "Privatsteuern (nur Einzelunternehmen)"),
        ("1820", "Sonderausgaben beschränkt abzugsfähig"),
        ("1821", "Sonderausgaben beschränkt abzugsfähig (nur Einzelunternehmen)"),
        ("1830", "Sonderausgaben unbeschränkt abzugsfähig"),
        ("1831", "Sonderausgaben unbeschränkt abzugsfähig (nur Einzelunternehmen)"),
        ("1840", "Zuwendungen, Spenden"),
        ("1841", "Zuwendungen, Spenden (nur Einzelunternehmen)"),
        ("1850", "Außergewöhnliche Belastungen"),
        ("1851", "Außergewöhnliche Belastungen (nur Einzelunternehmen)"),
        ("1860", "Grundstücksaufwand"),
        ("1861", "Grundstücksaufwand (nur Einzelunternehmen)"),
        ("1869", "Grundstücksaufwand (Umsatzsteuerschlüssel möglich, nur Einzelunternehmen)"),
        ("1870", "Grundstücksertrag"),
        ("1871", "Grundstücksertrag (nur Einzelunternehmen)"),
        ("1879", "Grundstücksertrag (Umsatzsteuerschlüssel möglich, nur Einzelunternehmen)"),
        ("1880", "Unentgeltliche Wertabgaben"),
        ("1881", "Unentgeltliche Wertabgaben (nur Einzelunternehmen)"),
        ("1890", "Privateinlagen"),
        ("1891", "Privateinlagen (nur Einzelunternehmen)"),
        
        ("2100", "Zinsen und ähnliche Aufwendungen"),
        ("2102", "Steuerlich nicht abzugsfähige andere Nebenleistungen zu Steuern § 4 Abs. 5b EStG"),
        ("2103", "Steuerlich abzugsfähige andere Nebenleistungen zu Steuern"),
        ("2104", "Steuerlich nicht abzugsfähige andere Nebenleistungen zu Steuern"),
        ("2105", "Zinsaufwendungen § 233a AO nicht abzugsfähig"),
        ("2107", "Zinsaufwendungen § 233a AO abzugsfähig"),
        ("2108", "Zinsaufwendungen §§ 234 bis 237 AO nicht abzugsfähig"),
        ("2109", "Zinsaufwendungen an verbundene Unternehmen"),
        ("2110", "Zinsaufwendungen für kurzfristige Verbindlichkeiten"),
        ("2111", "Zinsaufwendungen §§ 234 bis 237 AO abzugsfähig"),
        ("2113", "Nicht abzugsfähige Schuldzinsen nach § 4 Abs. 4a EStG (Hinzurechnungsbetrag)"),
        ("2114", "Zinsen für Gesellschafterdarlehen"),
        ("2115", "Zinsen und ähnliche Aufwendungen §§ 3 Nr. 40 und 3c EStG bzw. § 8b Abs. 1 und 4 KStG"),
        ("2116", "Zinsen und ähnliche Aufwendungen an verbundene Unternehmen §§ 3 Nr. 40 und 3c EStG bzw. § 8b Abs. 1 KStG"),
        ("2117", "Zinsen an Gesellschafter mit einer Beteiligung von mehr als 25 % bzw. diesen nahe stehende Personen"),
        ("2118", "Zinsen auf Kontokorrentkonten"),
        ("2119", "Zinsaufwendungen für kurzfristige Verbindlichkeiten an verbundene Unternehmen"),
        ("2120", "Zinsaufwendungen für langfristige Verbindlichkeiten"),
        ("2123", "Abschreibungen auf ein Agio oder Disagio/Damnum zur Finanzierung"),
        ("2124", "Abschreibungen auf ein Agio oder Disagio/Damnum zur Finanzierung des Anlagevermögens"),
        ("2125", "Zinsaufwendungen für Gebäude, die zum Betriebsvermögen gehören"),
        ("2126", "Zinsen zur Finanzierung des Anlagevermögens"),
        ("2127", "Renten und dauernde Lasten"),
        ("2128", "Zinsaufwendungen für Kapitalüberlassung durch Mitunternehmer § 15 EStG (mit Sonderbetriebseinnahme korrespondierend)"),
        ("2129", "Zinsaufwendungen für langfristige Verbindlichkeiten an verbundene Unternehmen"),
        ("2140", "Zinsähnliche Aufwendungen"),
        ("2141", "Kreditprovisionen und Verwaltungskostenbeiträge"),
        ("2142", "Zinsanteil der Zuführungen zu Pensionsrückstellungen"),
        ("2143", "Zinsaufwendungen aus der Abzinsung von Verbindlichkeiten"),
        ("2144", "Zinsaufwendungen aus der Abzinsung von Rückstellungen"),
        ("2145", "Zinsaufwendungen aus der Abzinsung von Pensionsrückstellungen und ähnlichen/vergleichbaren Verpflichtungen"),
        ("2146", "Zinsaufwendungen aus der Abzinsung von Pensionsrückstellungen und ähnlichen/vergleichbaren Verpflichtungen zur Verrechnung nach § 246 Abs. 2 HGB"),
        ("2147", "Aufwendungen aus Vermögensgegenständen zur Verrechnung nach § 246 Abs. 2 HGB"),
        ("2148", "Steuerlich nicht abzugsfähige Zinsaufwendungen aus der Abzinsung von Rückstellungen"),
        ("2149", "Zinsähnliche Aufwendungen an verbundene Unternehmen"),
        
        ("2200", "Körperschaftsteuer"),
        ("2203", "Körperschaftsteuer für Vorjahre"),
        ("2204", "Körperschaftsteuererstattungen für Vorjahre"),
        ("2208", "Solidaritätszuschlag"),
        ("2209", "Solidaritätszuschlag für Vorjahre"),
        ("2210", "Solidaritätszuschlagerstattungen für Vorjahre"),
        ("2213", "Kapitalertragsteuer 25 %"),
        ("2216", "Anrechenbarer Solidaritätszuschlag auf Kapitalertragsteuer 25 %"),
        ("2218", "Ausländische Steuer auf im Inland steuerfreie DBA-Einkünfte"),
        ("2219", "Anrechnung/Abzug ausländische Quellensteuer"),
        ("2250", "Aufwendungen aus der Zuführung und Auflösung von latenten Steuern"),
        ("2255", "Erträge aus der Zuführung und Auflösung von latenten Steuern"),
        ("2260", "Aufwendungen aus der Zuführung zu Steuerrückstellungen für Steuerstundung (BStBK)"),
        ("2265", "Erträge aus der Auflösung von Steuerrückstellungen für Steuerstundung (BStBK)"),
        ("2281", "Gewerbesteuernachzahlungen und Gewerbesteuererstattungen für Vorjahre nach § 4 Abs. 5b EStG"),
        ("2283", "Erträge aus der Auflösung von Gewerbesteuerrückstellungen nach § 4 Abs. 5b EStG"),
        ("2285", "Steuernachzahlungen Vorjahre für sonstige Steuern"),
        ("2287", "Steuererstattungen Vorjahre für sonstige Steuern"),
        ("2289", "Erträge aus der Auflösung von Rückstellungen für sonstige Steuern"),
        
        ("3000", "Roh-, Hilfs- und Betriebsstoffe"),
        ("3100", "Fremdleistungen"),
        ("3106", "Fremdleistungen 19 % Vorsteuer"),
        ("3108", "Fremdleistungen 7 % Vorsteuer"),
        ("3109", "Fremdleistungen ohne Vorsteuer"),
        ("3200", "Wareneingang"),
        
        ("4000", "Material- und Stoffverbrauch"),
        ("4100", "Löhne und Gehälter"),
        ("4110", "Löhne"),
        ("4120", "Gehälter"),
        ("4124", "Geschäftsführergehälter der GmbH-Gesellschafter"),
        ("4125", "Ehegattengehalt"),
        ("4126", "Tantiemen Gesellschafter-Geschäftsführer"),
        ("4127", "Geschäftsführergehälter"),
        ("4128", "Vergütungen an angestellte Mitunternehmer § 15 EStG (mit Sonderbetriebseinnahme korrespondierend)"),
        ("4129", "Tantiemen Arbeitnehmer"),
        ("4130", "Gesetzliche soziale Aufwendungen"),
        ("4137", "Gesetzliche soziale Aufwendungen für Mitunternehmer § 15 EStG (mit Sonderbetriebseinnahme korrespondierend)"),
        ("4138", "Beiträge zur Berufsgenossenschaft"),
        ("4139", "Ausgleichsabgabe nach dem Schwerbehindertengesetz"),
        ("4140", "Freiwillige soziale Aufwendungen, lohnsteuerfrei"),
        ("4141", "Sonstige soziale Abgaben"),
        ("4144", "Soziale Abgaben für Minijobber"),
        ("4145", "Freiwillige soziale Aufwendungen, lohnsteuerpflichtig"),
        ("4146", "Freiwillige Zuwendungen an Minijobber"),
        ("4147", "Freiwillige Zuwendungen an Gesellschafter-Geschäftsführer"),
        ("4148", "Freiwillige Zuwendungen an angestellte Mitunternehmer § 15 EStG (mit Sonderbetriebseinnahme korrespondierend)"),
        ("4149", "Pauschale Steuer auf sonstige Bezüge (z. B. Fahrtkostenzuschüsse)"),
        ("4150", "Krankengeldzuschüsse"),
        ("4151", "Sachzuwendungen und Dienstleistungen an Minijobber"),
        ("4152", "Sachzuwendungen und Dienstleistungen an Arbeitnehmer"),
        ("4153", "Sachzuwendungen und Dienstleistungen an Gesellschafter-Geschäftsführer"),
        ("4154", "Sachzuwendungen und Dienstleistungen an angestellte Mitunternehmer § 15 EStG (mit Sonderbetriebseinnahme korrespondierend)"),
        ("4155", "Zuschüsse der Agenturen für Arbeit (Haben)"),
        ("4156", "Aufwendungen aus der Veränderung von Urlaubsrückstellungen"),
        ("4157", "Aufwendungen aus der Veränderung von Urlaubsrückstellungen für Gesellschafter-Geschäftsführer"),
        ("4158", "Aufwendungen aus der Veränderung von Urlaubsrückstellungen für angestellte Mitunternehmer § 15 EStG (mit Sonderbetriebseinnahme korrespondierend)"),
        ("4159", "Aufwendungen aus der Veränderung von Urlaubsrückstellungen für Minijobber"),
        ("4160", "Versorgungskassen"),
        ("4165", "Aufwendungen für Altersversorgung"),
        ("4166", "Aufwendungen für Altersversorgung für Gesellschafter-Geschäftsführer"),
        ("4167", "Pauschale Steuer auf sonstige Bezüge (z. B. Direktversicherungen)"),
        ("4168", "Aufwendungen für Altersversorgung für Mitunternehmer § 15 EStG (mit Sonderbetriebseinnahme korrespondierend)"),
        ("4169", "Aufwendungen für Unterstützung"),
        ("4170", "Vermögenswirksame Leistungen"),
        ("4175", "Fahrtkostenerstattung - Wohnung/Arbeitsstätte"),
        ("4180", "Bedienungsgelder"),
        ("4190", "Aushilfslöhne"),
        ("4194", "Pauschale Steuer für Minijobber"),
        ("4195", "Löhne für Minijobs"),
        ("4196", "Pauschale Steuer für Gesellschafter-Geschäftsführer"),
        ("4197", "Pauschale Steuer für angestellte Mitunternehmer § 15 EStG (mit Sonderbetriebseinnahme korrespondierend)"),
        ("4198", "Pauschale Steuer für Arbeitnehmer"),
        ("4199", "Pauschale Steuer für Aushilfen"),
        
        ("4200", "Raumkosten"),
        ("4210", "Miete (unbewegliche Wirtschaftsgüter)"),
        ("4211", "Aufwendungen für gemietete oder gepachtete unbewegliche Wirtschaftsgüter, die gewerbesteuerlich hinzuzurechnen sind"),
        ("4212", "Miete/Aufwendungen für doppelte Haushaltsführung Unternehmer"),
        ("4215", "Leasing (unbewegliche Wirtschaftsgüter)"),
        ("4219", "Vergütungen an Mitunternehmer für die mietweise Überlassung ihrer unbeweglichen Wirtschaftsgüter § 15 EStG (mit Sonderbetriebseinnahme korrespondierend)"),
        ("4220", "Pacht (unbewegliche Wirtschaftsgüter)"),
        ("4222", "Vergütungen an Gesellschafter für die miet- oder pachtweise Überlassung ihrer unbeweglichen Wirtschaftsgüter"),
        ("4228", "Miet- und Pachtnebenkosten, die gewerbesteuerlich nicht hinzuzurechnen sind"),
        ("4229", "Vergütungen an Mitunternehmer für die pachtweise Überlassung ihrer unbeweglichen Wirtschaftsgüter § 15 EStG (mit Sonderbetriebseinnahme korrespondierend)"),
        ("4230", "Heizung"),
        ("4240", "Gas, Strom, Wasser"),
        ("4250", "Reinigung"),
        ("4260", "Instandhaltung betrieblicher Räume"),
        ("4270", "Abgaben für betrieblich genutzten Grundbesitz"),
        ("4280", "Sonstige Raumkosten"),
        ("4287", "Tagespauschale für die Tätigkeit in der häuslichen Wohnung"),
        ("4288", "Aufwendungen für ein häusliches Arbeitszimmer (abziehbarer Anteil)"),
        ("4289", "Aufwendungen für ein häusliches Arbeitszimmer (nicht abziehbarer Anteil)"),
        ("4290", "Grundstücksaufwendungen betrieblich"),
        
        ("4300", "Nicht abziehbare Vorsteuer"),
        ("4301", "Nicht abziehbare Vorsteuer 7 %"),
        ("4306", "Nicht abziehbare Vorsteuer 19 %"),
        ("4320", "Gewerbesteuer"),
        ("4340", "Sonstige Betriebssteuern"),
        ("4350", "Verbrauchsteuer (sonstige Steuern)"),
        ("4355", "Ökosteuer"),
        ("4360", "Versicherungen"),
        ("4366", "Versicherungen für Gebäude"),
        ("4370", "Netto-Prämie für Rückdeckung künftiger Versorgungsleistungen"),
        ("4380", "Beiträge"),
        ("4390", "Sonstige Abgaben"),
        ("4396", "Steuerlich abzugsfähige Verspätungszuschläge und Zwangsgelder"),
        ("4397", "Steuerlich nicht abzugsfähige Verspätungszuschläge und Zwangsgelder"),
        
        ("4500", "Fahrzeugkosten"),
        ("4510", "Kfz-Steuer"),
        ("4520", "Fahrzeug-Versicherungen"),
        ("4530", "Laufende Fahrzeug-Betriebskosten"),
        ("4540", "Fahrzeug-Reparaturen"),
        ("4550", "Garagenmiete"),
        ("4560", "Mautgebühren"),
        ("4570", "Mietleasing Kfz"),
        ("4575", "Mietleasingaufwendungen für Elektrofahrzeuge und Fahrräder, die gewerbesteuerlich hinzuzurechnen sind"),
        ("4580", "Sonstige Fahrzeugkosten"),
        ("4590", "Kosten für betrieblich genutzte zum Privatvermögen gehörende Fahrzeuge"),
        ("4595", "Fremdfahrzeugkosten"),
        
        ("4600", "Werbekosten"),
        ("4605", "Streuartikel"),
        ("4630", "Geschenke abzugsfähig ohne § 37b EStG"),
        ("4631", "Geschenke abzugsfähig mit § 37b EStG"),
        ("4632", "Pauschale Steuer für Geschenke und Zuwendungen abzugsfähig"),
        ("4635", "Geschenke nicht abzugsfähig ohne § 37b EStG"),
        ("4636", "Geschenke nicht abzugsfähig mit § 37b EStG"),
        ("4637", "Pauschale Steuer für Geschenke und Zuwendungen nicht abzugsfähig"),
        ("4638", "Geschenke ausschließlich betrieblich genutzt"),
        ("4639", "Zugaben mit § 37b EStG"),
        ("4640", "Repräsentationskosten"),
        ("4650", "Bewirtungskosten"),
        ("4651", "Sonstige eingeschränkt abziehbare Betriebsausgaben (abziehbarer Anteil)"),
        ("4652", "Sonstige eingeschränkt abziehbare Betriebsausgaben (nicht abziehbarer Anteil)"),
        ("4653", "Aufmerksamkeiten"),
        ("4654", "Nicht abzugsfähige Bewirtungskosten"),
        ("4655", "Nicht abzugsfähige Betriebsausgaben aus Werbe- und Repräsentationskosten"),
        
        ("4660", "Reisekosten Arbeitnehmer"),
        ("4663", "Reisekosten Arbeitnehmer Fahrtkosten"),
        ("4664", "Reisekosten Arbeitnehmer Verpflegungsmehraufwand"),
        ("4666", "Reisekosten Arbeitnehmer Übernachtungsaufwand"),
        ("4668", "Kilometergelderstattung Arbeitnehmer"),
        ("4670", "Reisekosten Unternehmer"),
        ("4672", "Reisekosten Unternehmer (nicht abziehbarer Anteil)"),
        ("4673", "Reisekosten Unternehmer Fahrtkosten"),
        ("4674", "Reisekosten Unternehmer Verpflegungsmehraufwand"),
        ("4676", "Reisekosten Unternehmer Übernachtungsaufwand und Reisenebenkosten"),
        ("4678", "Fahrten zwischen Wohnung und Betriebsstätte und Familienheimfahrten (abziehbarer Anteil) - Fahrzeuge im Betriebsvermögen"),
        ("4679", "Fahrten zwischen Wohnung und Betriebsstätte und Familienheimfahrten (nicht abziehbarer Anteil) - Fahrzeuge im Betriebsvermögen"),
        ("4680", "Fahrten zwischen Wohnung und Betriebsstätte und Familienheimfahrten (Haben) - Fahrzeuge im Betriebsvermögen"),
        ("4681", "Verpflegungsmehraufwendungen im Rahmen der doppelten Haushaltsführung Unternehmer"),
        
        ("4700", "Kosten der Warenabgabe"),
        ("4710", "Verpackungsmaterial"),
        ("4730", "Ausgangsfrachten"),
        ("4750", "Transportversicherungen"),
        ("4760", "Verkaufsprovisionen"),
        ("4780", "Fremdarbeiten (Vertrieb)"),
        ("4790", "Aufwand für Gewährleistungen"),
        
        ("4800", "Reparaturen und Instandhaltungen von technischen Anlagen und Maschinen"),
        ("4801", "Reparaturen und Instandhaltung von Bauten"),
        ("4805", "Reparaturen und Instandhaltungen von anderen Anlagen und Betriebs- und Geschäftsausstattung"),
        ("4806", "Wartungskosten für Hard- und Software"),
        ("4808", "Zuführung zu Aufwandsrückstellungen"),
        ("4809", "Sonstige Reparaturen und Instandhaltungen"),
        ("4810", "Mietleasing bewegliche Wirtschaftsgüter für technische Anlagen und Maschinen"),
        ("4815", "Kaufleasing"),
        
        ("4822", "Abschreibungen auf immaterielle Vermögensgegenstände"),
        ("4823", "Abschreibungen auf selbst geschaffene immaterielle Vermögensgegenstände"),
        ("4824", "Abschreibungen auf den Geschäfts- oder Firmenwert"),
        ("4825", "Außerplanmäßige Abschreibungen auf den Geschäfts- oder Firmenwert"),
        ("4826", "Außerplanmäßige Abschreibungen auf immaterielle Vermögensgegenstände"),
        ("4827", "Außerplanmäßige Abschreibungen auf selbst geschaffene immaterielle Vermögensgegenstände"),
        ("4830", "Abschreibungen auf Sachanlagen (ohne AfA auf Fahrzeuge und Gebäude)"),
        ("4831", "Abschreibungen auf Gebäude"),
        ("4832", "Abschreibungen auf Fahrzeuge"),
        ("4833", "Abschreibungen auf Gebäudeanteil des häuslichen Arbeitszimmers"),
        ("4840", "Außerplanmäßige Abschreibungen auf Sachanlagen"),
        ("4841", "Absetzung für außergewöhnliche technische und wirtschaftliche Abnutzung der Gebäude"),
        ("4842", "Absetzung für außergewöhnliche technische und wirtschaftliche Abnutzung der Fahrzeuge"),
        ("4843", "Absetzung für außergewöhnliche technische und wirtschaftliche Abnutzung sonstiger Wirtschaftsgüter"),
        ("4850", "Abschreibungen auf Sachanlagen auf Grund steuerlicher Sondervorschriften"),
        ("4851", "Sonderabschreibungen nach § 7g Abs. 5 EStG (ohne Fahrzeuge)"),
        ("4852", "Sonderabschreibungen nach § 7g Abs. 5 EStG (für Fahrzeuge)"),
        ("4853", "Kürzung der Anschaffungs- oder Herstellungskosten nach § 7g Abs. 2 EStG (ohne Fahrzeuge)"),
        ("4854", "Kürzung der Anschaffungs- oder Herstellungskosten nach § 7g Abs. 2 EStG (für Fahrzeuge)"),
        ("4855", "Sofortabschreibung geringwertiger Wirtschaftsgüter"),
        ("4856", "Sonderabschreibungen nach § 7b EStG (Mietwohnungsneubau)"),
        ("4859", "Abzugsbetrag nach § 6b EStG"),
        ("4860", "Abschreibungen auf aktivierte, geringwertige Wirtschaftsgüter"),
        ("4862", "Abschreibungen auf den Sammelposten Wirtschaftsgüter"),
        ("4865", "Außerplanmäßige Abschreibungen auf aktivierte, geringwertige Wirtschaftsgüter"),
        ("4866", "Abschreibungen auf Finanzanlagen (nicht dauerhaft)"),
        ("4870", "Abschreibungen auf Finanzanlagen (dauerhaft)"),
        ("4871", "Abschreibungen auf Finanzanlagen § 3 Nr. 40 EStG bzw. § 8b Abs. 3 KStG (dauerhaft)"),
        ("4872", "Aufwendungen auf Grund von Verlustanteilen an gewerblichen und selbständigen Mitunternehmerschaften, § 8 GewStG bzw. § 18 EStG"),
        ("4873", "Abschreibungen auf Finanzanlagen auf Grund § 6b EStG-Rücklage, § 3 Nr. 40 EStG bzw. § 8b Abs. 3 KStG"),
        ("4874", "Abschreibungen auf Finanzanlagen auf Grund § 6b EStG-Rücklage"),
        ("4875", "Abschreibungen auf Wertpapiere des Umlaufvermögens"),
        ("4876", "Abschreibungen auf Wertpapiere des Umlaufvermögens § 3 Nr. 40 EStG bzw. § 8b Abs. 3 KStG"),
        ("4877", "Abschreibungen auf Finanzanlagen - verbundene Unternehmen"),
        ("4878", "Abschreibungen auf Wertpapiere des Umlaufvermögens - verbundene Unternehmen"),
        ("4880", "Abschreibungen auf sonstige Vermögensgegenstände des Umlaufvermögens (soweit unüblich hoch)"),
        ("4882", "Abschreibungen auf Umlaufvermögen, steuerrechtlich bedingt (soweit unüblich hoch)"),
        ("4886", "Abschreibungen auf Umlaufvermögen außer Vorräte und Wertpapiere des Umlaufvermögens (übliche Höhe)"),
        ("4887", "Abschreibungen auf Umlaufvermögen außer Vorräte und Wertpapiere des Umlaufvermögens, steuerrechtlich bedingt (übliche Höhe)"),
        ("4892", "Abschreibungen auf Roh-, Hilfs- und Betriebsstoffe/Waren (soweit unübliche Höhe)"),
        ("4893", "Abschreibungen auf fertige und unfertige Erzeugnisse (soweit unübliche Höhe)"),
        
        ("4900", "Sonstige betriebliche Aufwendungen"),
        ("4902", "Interimskonto für Aufwendungen in einem anderen Land, bei denen eine Vorsteuervergütung möglich ist"),
        ("4905", "Sonstige Aufwendungen betrieblich und regelmäßig"),
        ("4909", "Fremdleistungen/Fremdarbeiten"),
        ("4910", "Porto"),
        ("4920", "Telefon"),
        ("4925", "Internetkosten"),
        ("4930", "Bürobedarf"),
        ("4940", "Zeitschriften, Bücher, digitale Medien (Fachliteratur)"),
        ("4945", "Fortbildungskosten"),
        ("4946", "Freiwillige Sozialleistungen"),
        ("4948", "Sonstige Vergütungen an Mitunternehmer § 15 EStG (mit Sonderbetriebseinnahme korrespondierend)"),
        ("4949", "Haftungsvergütung an Mitunternehmer § 15 EStG (mit Sonderbetriebseinnahme korrespondierend)"),
        ("4950", "Rechts- und Beratungskosten"),
        ("4955", "Buchführungskosten"),
        ("4957", "Abschluss- und Prüfungskosten"),
        ("4958", "Vergütungen an Gesellschafter für die miet- oder pachtweise Überlassung ihrer beweglichen Wirtschaftsgüter"),
        ("4959", "Vergütungen an Mitunternehmer für die miet- oder pachtweise Überlassung ihrer beweglichen Wirtschaftsgüter § 15 EStG (mit Sonderbetriebseinnahme korrespondierend)"),
        ("4960", "Mieten für Einrichtungen (bewegliche Wirtschaftsgüter)"),
        ("4961", "Pacht (bewegliche Wirtschaftsgüter)"),
        ("4963", "Aufwendungen für gemietete oder gepachtete bewegliche Wirtschaftsgüter, die gewerbesteuerlich hinzuzurechnen sind"),
        ("4964", "Aufwendungen für die zeitlich befristete Überlassung von Rechten (Lizenzen, Konzessionen)"),
        ("4965", "Mietleasing bewegliche Wirtschaftsgüter für Betriebs- und Geschäftsausstattung"),
        ("4969", "Aufwendungen für Abraum- und Abfallbeseitigung"),
        ("4970", "Nebenkosten des Geldverkehrs"),
        ("4971", "Verwahrentgelt"),
        ("4975", "Aufwendungen aus Anteilen an Kapitalgesellschaften §§ 3 Nr. 40 und 3c EStG bzw. § 8b Abs. 1 und 4 KStG"),
        ("4976", "Veräußerungskosten § 3 Nr. 40 EStG bzw. § 8b Abs. 2 KStG (bei Buchgewinn)"),
        ("4977", "Veräußerungskosten § 3 Nr. 40 EStG bzw. § 8b Abs. 2 KStG i. V. m. § 8b Abs. 3 S. 3 KStG (bei Buchverlust)"),
        ("4980", "Sonstiger Betriebsbedarf"),
        ("4984", "Genossenschaftliche Rückvergütung an Mitglieder"),
        ("4985", "Werkzeuge und Kleingeräte"),
        
        ("4990", "Kalkulatorischer Unternehmerlohn"),
        ("4991", "Kalkulatorische Miete und Pacht"),
        ("4992", "Kalkulatorische Zinsen"),
        ("4993", "Kalkulatorische Abschreibungen"),
        ("4994", "Kalkulatorische Wagnisse"),
        ("4995", "Kalkulatorischer Lohn für unentgeltliche Mitarbeiter"),
        
        ("4996", "Herstellungskosten"),
        ("4997", "Verwaltungskosten"),
        ("4998", "Vertriebskosten"),
        ("4999", "Gegenkonto 4996-4998"),
        
        ("7000", "Unfertige Erzeugnisse, unfertige Leistungen (Bestand)"),
        ("7050", "Unfertige Erzeugnisse (Bestand)"),
        ("7080", "Unfertige Leistungen (Bestand)"),
        ("7090", "In Ausführung befindliche Bauaufträge"),
        ("7095", "In Arbeit befindliche Aufträge"),
        ("7100", "Fertige Erzeugnisse und Waren (Bestand)"),
        ("7110", "Fertige Erzeugnisse (Bestand)"),
        ("7140", "Waren (Bestand)"),
        
        ("8000", "Umsatzerlöse"),
        ("8100", "Steuerfreie Umsätze § 4 Nr. 8 ff. UStG"),
        ("8105", "Steuerfreie Umsätze nach § 4 Nr. 12 UStG (Vermietung und Verpachtung)"),
        ("8110", "Sonstige steuerfreie Umsätze Inland"),
        ("8120", "Steuerfreie Umsätze nach § 4 Nr. 1a UStG"),
        ("8125", "Steuerfreie innergemeinschaftliche Lieferungen nach § 4 Nr. 1b UStG"),
        ("8130", "Lieferungen des ersten Abnehmers bei innergemeinschaftlichen Dreiecksgeschäften § 25b Abs. 2 UStG"),
        ("8135", "Steuerfreie innergemeinschaftliche Lieferungen von Neufahrzeugen an Abnehmer ohne USt-Id-Nr."),
        ("8140", "Steuerfreie Umsätze Offshore usw."),
        ("8150", "Sonstige steuerfreie Umsätze (z. B. § 4 Nr. 2 bis 7 UStG)"),
        ("8160", "Steuerfreie Umsätze ohne Vorsteuerabzug zum Gesamtumsatz gehörend, § 4 UStG"),
        ("8165", "Steuerfreie Umsätze ohne Vorsteuerabzug zum Gesamtumsatz gehörend"),
        ("8190", "Erlöse, die mit den Durchschnittssätzen des § 24 UStG versteuert werden"),
        ("8191", "Umsatzerlöse nach §§ 25 und 25a UStG 19 % USt"),
        ("8192", "Steuerfreie Erlöse Kleinunternehmer nach § 19 Abs. 1 UStG"),
        ("8193", "Umsatzerlöse nach §§ 25 und 25a UStG ohne USt"),
        ("8194", "Umsatzerlöse aus Reiseleistungen § 25 Abs. 2 UStG, steuerfrei"),
        ("8195", "Erlöse als Kleinunternehmer nach § 19 Abs. 1 UStG a. F."),
        ("8196", "Erlöse aus Geldspielautomaten 19 % USt"),
        ("8200", "Erlöse"),
        ("8290", "Erlöse 0 % USt"),
        ("8300", "Erlöse 7 % USt"),
        ("8315", "Erlöse aus im Inland steuerpflichtigen EU-Lieferungen 19 % USt"),
        ("8334", "Erlöse 7 % USt"),
        ("8335", "Erlöse aus Lieferungen von Mobilfunkgeräten, Tablet-Computern, Spielekonsolen und integrierten Schaltkreisen, für die der Leistungsempfänger die Umsatzsteuer nach § 13b UStG schuldet"),
        ("8336", "Erlöse aus im anderen EU-Land steuerpflichtigen sonstigen Leistungen, für die der Leistungsempfänger die Umsatzsteuer schuldet"),
        ("8337", "Erlöse aus Leistungen, für die der Leistungsempfänger die Umsatzsteuer nach § 13b UStG schuldet"),
        ("8338", "Erlöse aus im Drittland steuerbaren Leistungen, im Inland nicht steuerbare Umsätze"),
        ("8339", "Erlöse aus im anderen EU-Land steuerbaren Leistungen, im Inland nicht steuerbare Umsätze"),
        ("8400", "Erlöse 19 % USt"),
        ("8449", "Erlöse aus im Inland steuerpflichtigen elektronischen Dienstleistungen 19 % USt"),
        ("8499", "Nebenerlöse (Bezug zu Materialaufwand)"),
        
        ("8500", "Sonderbetriebseinnahmen, Tätigkeitsvergütung"),
        ("8501", "Sonderbetriebseinnahmen, Miet-/Pachteinnahmen"),
        ("8502", "Sonderbetriebseinnahmen, Zinseinnahmen"),
        ("8503", "Sonderbetriebseinnahmen, Haftungsvergütung"),
        ("8504", "Sonderbetriebseinnahmen, Pensionszahlungen"),
        ("8505", "Sonderbetriebseinnahmen, sonstige Sonderbetriebseinnahmen"),
        ("8510", "Provisionsumsätze"),
        ("8514", "Provisionsumsätze, steuerfrei § 4 Nr. 8 ff. UStG"),
        ("8515", "Provisionsumsätze, steuerfrei § 4 Nr. 5 UStG"),
        ("8519", "Provisionsumsätze 19 % USt"),
        ("8520", "Erlöse Abfallverwertung"),
        ("8540", "Erlöse Leergut"),
        ("8570", "Sonstige Erträge aus Provisionen, Lizenzen und Patenten"),
        ("8574", "Sonstige Erträge aus Provisionen, Lizenzen und Patenten, steuerfrei § 4 Nr. 8 ff. UStG"),
        ("8575", "Sonstige Erträge aus Provisionen, Lizenzen und Patenten, steuerfrei § 4 Nr. 5 UStG"),
        ("8576", "Sonstige Erträge aus Provisionen, Lizenzen und Patenten 7 % USt"),
        ("8579", "Sonstige Erträge aus Provisionen, Lizenzen und Patenten 19 % USt"),
        
        ("8580", "Statistisches Konto Erlöse zum allgemeinen Umsatzsteuersatz (EÜR)"),
        ("8581", "Statistisches Konto Erlöse zum ermäßigten Umsatzsteuersatz (EÜR)"),
        ("8582", "Statistisches Konto Erlöse steuerfrei und nicht steuerbar (EÜR)"),
        ("8589", "Gegenkonto 8580-8582 bei Aufteilung der Erlöse nach Steuersätzen (EÜR)"),
        
        ("8590", "Verrechnete sonstige Sachbezüge (keine Waren)"),
        ("8591", "Sachbezüge 7 % USt (Waren)"),
        ("8595", "Sachbezüge 19 % USt (Waren)"),
        ("8600", "Sonstige Erlöse betrieblich und regelmäßig"),
        ("8603", "Sonstige betriebliche Erträge"),
        ("8604", "Erstattete Vorsteuer anderer Länder"),
        ("8605", "Sonstige Erträge betrieblich und regelmäßig"),
        ("8606", "Sonstige betriebliche Erträge von verbundenen Unternehmen"),
        ("8607", "Andere Nebenerlöse"),
        ("8609", "Sonstige Erträge betrieblich und regelmäßig, steuerfrei § 4 Nr. 8 ff. UStG"),
        ("8610", "Verrechnete sonstige Sachbezüge"),
        ("8611", "Verrechnete sonstige Sachbezüge aus Fahrzeug-Gestellung 19 % USt"),
        ("8613", "Verrechnete sonstige Sachbezüge 19 % USt"),
        ("8614", "Verrechnete sonstige Sachbezüge ohne Umsatzsteuer"),
        
        ("8650", "Erlöse Zinsen und Diskontspesen"),
        ("8660", "Erlöse Zinsen und Diskontspesen aus verbundenen Unternehmen"),
        
        ("8700", "Erlösschmälerungen"),
        ("8701", "Erlösschmälerungen für steuerfreie Umsätze nach § 4 Nr. 8 ff. UStG"),
        ("8702", "Erlösschmälerungen für steuerfreie Umsätze nach § 4 Nr. 2 bis 7 UStG"),
        ("8703", "Erlösschmälerungen für sonstige steuerfreie Umsätze ohne Vorsteuerabzug"),
        ("8704", "Erlösschmälerungen für sonstige steuerfreie Umsätze mit Vorsteuerabzug"),
        ("8705", "Erlösschmälerungen aus steuerfreien Umsätzen § 4 Nr. 1a UStG"),
        ("8706", "Erlösschmälerungen für steuerfreie innergemeinschaftliche Dreiecksgeschäfte nach § 25b Abs. 2 und 4 UStG"),
        ("8719", "Erlösschmälerungen 0 % USt"),
        ("8724", "Erlösschmälerungen aus steuerfreien innergemeinschaftlichen Lieferungen"),
        ("8725", "Erlösschmälerungen aus im Inland steuerpflichtigen EU-Lieferungen 7 % USt"),
        ("8726", "Erlösschmälerungen aus im Inland steuerpflichtigen EU-Lieferungen 19 % USt"),
        ("8730", "Gewährte Skonti"),
        ("8731", "Gewährte Skonti 7 % USt"),
        ("8734", "Gewährte Skonti 0 % USt"),
        ("8736", "Gewährte Skonti 19 % USt"),
        ("8738", "Gewährte Skonti aus Lieferungen von Mobilfunkgeräten etc., für die der Leistungsempfänger die Umsatzsteuer nach § 13b Abs. 2 Nr. 10 UStG schuldet"),
        ("8741", "Gewährte Skonti aus Leistungen, für die der Leistungsempfänger die Umsatzsteuer nach § 13b UStG schuldet"),
        ("8742", "Gewährte Skonti aus Erlösen aus im anderen EU-Land steuerpflichtigen sonstigen Leistungen, für die der Leistungsempfänger die Umsatzsteuer schuldet"),
        ("8743", "Gewährte Skonti aus steuerfreien innergemeinschaftlichen Lieferungen § 4 Nr. 1b UStG"),
        ("8745", "Gewährte Skonti aus im Inland steuerpflichtigen EU-Lieferungen"),
        ("8746", "Gewährte Skonti aus im Inland steuerpflichtigen EU-Lieferungen 7 % USt"),
        ("8748", "Gewährte Skonti aus im Inland steuerpflichtigen EU-Lieferungen 19 % USt"),
        ("8769", "Gewährte Boni"),
        ("8770", "Gewährte Rabatte"),
        
        ("8800", "Erlöse aus Verkäufen Sachanlagevermögen (bei Buchverlust)"),
        ("8817", "Erlöse aus Verkäufen immaterieller Vermögensgegenstände (bei Buchverlust)"),
        ("8818", "Erlöse aus Verkäufen Finanzanlagen (bei Buchverlust)"),
        ("8819", "Erlöse aus Verkäufen Finanzanlagen § 3 Nr. 40 EStG bzw. § 8b Abs. 2 KStG i. V. m. § 8b Abs. 3 S. 3 KStG (bei Buchverlust)"),
        ("8829", "Erlöse aus Verkäufen Sachanlagevermögen (bei Buchgewinn)"),
        ("8837", "Erlöse aus Verkäufen immaterieller Vermögensgegenstände (bei Buchgewinn)"),
        ("8838", "Erlöse aus Verkäufen Finanzanlagen (bei Buchgewinn)"),
        ("8839", "Erlöse aus Verkäufen Finanzanlagen § 3 Nr. 40 EStG bzw. § 8b Abs. 2 KStG (bei Buchgewinn)"),
        ("8850", "Erlöse aus Verkäufen von Wirtschaftsgütern des Umlaufvermögens 19 % USt für § 4 Abs. 3 Satz 4 EStG"),
        ("8851", "Erlöse aus Verkäufen von Wirtschaftsgütern des Umlaufvermögens, umsatzsteuerfrei § 4 Nr. 8 ff. UStG i. V. m. § 4 Abs. 3 Satz 4 EStG"),
        ("8852", "Erlöse aus Verkäufen von Wirtschaftsgütern des Umlaufvermögens, umsatzsteuerfrei § 4 Nr. 8 ff. UStG i. V. m. § 4 Abs. 3 Satz 4 EStG und § 3 Nr. 40 EStG bzw. § 8b Abs. 2 KStG"),
        ("8853", "Erlöse aus Verkäufen von Wirtschaftsgütern des Umlaufvermögens nach § 4 Abs 3 Satz 4 EStG"),
        
        ("8900", "Unentgeltliche Wertabgaben"),
        ("8905", "Entnahme von Gegenständen ohne USt"),
        ("8906", "Verwendung von Gegenständen für Zwecke außerhalb des Unternehmens ohne USt"),
        ("8917", "Entnahme durch den Unternehmer für Zwecke außerhalb des Unternehmens (Waren) 7 % USt"),
        ("8918", "Verwendung von Gegenständen für Zwecke außerhalb des Unternehmens ohne USt (Telefon-Nutzung)"),
        ("8919", "Entnahme durch den Unternehmer für Zwecke außerhalb des Unternehmens (Waren) ohne USt"),
        ("8920", "Verwendung von Gegenständen für Zwecke außerhalb des Unternehmens 19 % USt"),
        ("8921", "Verwendung von Gegenständen für Zwecke außerhalb des Unternehmens 19 % USt (Fahrzeug-Nutzung)"),
        ("8922", "Verwendung von Gegenständen für Zwecke außerhalb des Unternehmens 19 % USt (Telefon-Nutzung)"),
        ("8924", "Verwendung von Gegenständen für Zwecke außerhalb des Unternehmens ohne USt (Fahrzeug-Nutzung)"),
        ("8929", "Unentgeltliche Erbringung einer sonstigen Leistung ohne USt"),
        ("8930", "Verwendung von Gegenständen für Zwecke außerhalb des Unternehmens 7 % USt"),
        ("8931", "Verwendung von Gegenständen für Zwecke außerhalb des Unternehmens 7 % USt"),
        ("8932", "Unentgeltliche Erbringung einer sonstigen Leistung 7 % USt"),
        ("8933", "Unentgeltliche Erbringung einer sonstigen Leistung 7 % USt"),
        ("8939", "Unentgeltliche Zuwendung von Gegenständen ohne USt"),
        ("8949", "Unentgeltliche Zuwendung von Waren ohne USt"),
        ("8950", "Nicht steuerbare Umsätze (Innenumsätze)"),
        ("8955", "Umsatzsteuervergütungen, z. B. nach § 24 UStG"),
        ("8959", "Direkt mit dem Umsatz verbundene Steuern"),
        
        ("8960", "Bestandsveränderungen - unfertige Erzeugnisse"),
        ("8970", "Bestandsveränderungen - unfertige Leistungen"),
        ("8975", "Bestandsveränderungen - in Ausführung befindliche Bauaufträge"),
        ("8977", "Bestandsveränderungen - in Arbeit befindliche Aufträge"),
        ("8980", "Bestandsveränderungen - fertige Erzeugnisse"),
        ("8990", "Andere aktivierte Eigenleistungen"),
        ("8994", "Aktivierte Eigenleistungen (den Herstellungskosten zurechenbare Fremdkapitalzinsen)"),
        ("8995", "Aktivierte Eigenleistungen zur Erstellung von selbst geschaffenen immateriellen Vermögensgegenständen"),
        
        ("9000", "Saldenvorträge, Sachkonten"),
        ("9008", "Saldenvorträge, Debitoren"),
        ("9009", "Saldenvorträge, Kreditoren"),
        ("9050", "Offene Posten aus 2020"),
        ("9051", "Offene Posten aus 2021"),
        ("9052", "Offene Posten aus 2022"),
        ("9053", "Offene Posten aus 2023"),
        ("9054", "Offene Posten aus 2024"),
        ("9055", "Offene Posten aus 2025"),
        ("9090", "Summenvortragskonto"),
        
        ("9101", "Verkaufstage"),
        ("9102", "Anzahl der Barkunden"),
        ("9103", "Beschäftigte Personen"),
        ("9104", "Unbezahlte Personen"),
        ("9105", "Verkaufskräfte"),
        ("9106", "Geschäftsraum qm"),
        ("9107", "Verkaufsraum qm"),
        ("9116", "Anzahl Rechnungen"),
        ("9117", "Anzahl Kreditkunden monatlich"),
        ("9118", "Anzahl Kreditkunden aufgelaufen"),
        ("9120", "Erweiterungsinvestitionen"),
        ("9135", "Auftragseingang im Geschäftsjahr"),
        ("9140", "Auftragsbestand"),
        ("9141", "Variables Kapital TH"),
        ("9142", "Variables Kapital - Anteil Teilhafter"),
        
        ("9143", "Privatsteuern Kapitalertragsteuer (Sammelposten)"),
        ("9144", "Privatsteuern Solidaritätszuschlag (Sammelposten)"),
        ("9145", "Privatsteuern Kirchensteuer (Sammelposten)"),
        
        ("9200", "Beschäftigte Personen"),
        ("9209", "Gegenkonto zu 9200"),
        ("9210", "Produktive Löhne"),
        ("9219", "Gegenkonto zu 9210"),
        ("9220", "Gezeichnetes Kapital in DM (Art. 42 Abs. 3 Satz 1 EGHGB)"),
        ("9229", "Gegenkonto zu 9220"),
        
        ("9240", "Investitionsverbindlichkeiten bei den Leistungsverbindlichkeiten"),
        ("9241", "Investitionsverbindlichkeiten aus Sachanlagekäufen bei Leistungsverbindlichkeiten"),
        ("9242", "Investitionsverbindlichkeiten aus Käufen von immateriellen Vermögensgegenständen bei Leistungsverbindlichkeiten"),
        ("9243", "Investitionsverbindlichkeiten aus Käufen von Finanzanlagen bei Leistungsverbindlichkeiten"),
        ("9244", "Gegenkonto zu Konten 9240-9243"),
        ("9245", "Forderungen aus Sachanlageveräufen bei sonstigen Vermögensgegenständen"),
        ("9246", "Forderungen aus Verkäufen immaterieller Vermögensgegenstände bei sonstigen Vermögensgegenständen"),
        ("9247", "Forderungen aus Verkäufen von Finanzanlagen bei sonstigen Vermögensgegenständen"),
        ("9249", "Gegenkonto zu Konten 9245-9247"),
        
        ("9260", "Kurzfristige Rückstellungen"),
        ("9262", "Mittelfristige Rückstellungen"),
        ("9264", "Langfristige Rückstellungen, außer Pensionen"),
        ("9269", "Gegenkonto zu Konten 9260-9268"),
        
        ("9270", "Gegenkonto zu 9271-9279 (Soll-Buchung)"),
        ("9271", "Verbindlichkeiten aus der Begebung und Übertragung von Wechseln"),
        ("9272", "Verbindlichkeiten aus der Begebung und Übertragung von Wechseln gegenüber verbundenen/assoziierten Unternehmen"),
        ("9273", "Verbindlichkeiten aus Bürgschaften, Wechsel- und Scheckbürgschaften"),
        ("9274", "Verbindlichkeiten aus Bürgschaften, Wechsel- und Scheckbürgschaften gegenüber verbundenen/assoziierten Unternehmen"),
        ("9275", "Verbindlichkeiten aus Gewährleistungsverträgen"),
        ("9276", "Verbindlichkeiten aus Gewährleistungsverträgen gegenüber verbundenen/assoziierten Unternehmen"),
        ("9277", "Haftung aus der Bestellung von Sicherheiten für fremde Verbindlichkeiten"),
        ("9278", "Haftung aus der Bestellung von Sicherheiten für fremde Verbindlichkeiten gegenüber verbundenen/assoziierten Unternehmen"),
        ("9279", "Verpflichtungen aus Treuhandvermögen"),
        
        ("9280", "Gegenkonto zu 9281-9284"),
        ("9281", "Verpflichtungen aus Miet- und Leasingverträgen"),
        ("9282", "Verpflichtungen aus Miet- und Leasingverträgen gegenüber verbundenen Unternehmen"),
        ("9283", "Andere Verpflichtungen nach § 285 Nr. 3a HGB"),
        ("9284", "Andere Verpflichtungen nach § 285 Nr. 3a HGB gegenüber verbundenen Unternehmen"),
        
        ("9285", "Unterschiedsbetrag aus der Abzinsung von Altersversorgungsverpflichtungen nach § 253 Abs. 6 HGB (Haben)"),
        ("9286", "Gegenkonto zu 9285"),
        
        ("9287", "Zinsen bei Buchungen über Debitoren bei § 4 Abs. 3 EStG"),
        ("9288", "Mahngebühren bei Buchungen über Debitoren bei § 4 Abs. 3 EStG"),
        ("9289", "Gegenkonto zu 9287 und 9288"),
        ("9290", "Statistisches Konto steuerfreie Auslagen"),
        ("9291", "Gegenkonto zu 9290"),
        ("9292", "Statistisches Konto Fremdgeld"),
        ("9293", "Gegenkonto zu 9292"),
        
        ("9295", "Einlagen atypisch stiller Gesellschafter"),
        ("9297", "Steuerlicher Ausgleichsposten (Körperschaften)"),
        ("9298", "Steuerlicher Ausgleichsposten VH (Personengesellschaften, Einzelunternehmen)"),
        ("9299", "Steuerlicher Ausgleichsposten TH (Personengesellschaften)"),
        
        ("9400", "Privatentnahmen allgemein (TH), EK"),
        ("9410", "Privatsteuern (TH), EK"),
        ("9420", "Sonderausgaben beschränkt abzugsfähig (TH), EK"),
        ("9430", "Sonderausgaben unbeschränkt abzugsfähig (TH), EK"),
        ("9440", "Zuwendungen, Spenden (TH), EK"),
        ("9450", "Außergewöhnliche Belastungen (TH), EK"),
        ("9460", "Grundstücksaufwand (TH), EK"),
        ("9470", "Grundstücksertrag (TH), EK"),
        ("9480", "Unentgeltliche Wertabgaben (TH), EK"),
        ("9490", "Privateinlagen (TH), EK"),
        
        ("9500", "Anteil für Konto 0900 Teilhafter"),
        ("9510", "Anteil für Konto 0910 Teilhafter"),
        ("9520", "Anteil für Konto 0920 Teilhafter"),
        ("9530", "Anteil für Konto 9950 Teilhafter"),
        ("9540", "Anteil für Konto 9930 Vollhafter"),
        ("9550", "Anteil für Konto 9810 Vollhafter"),
        ("9560", "Anteil für Konto 9820 Vollhafter"),
        ("9570", "Anteil für Konto 0870 Vollhafter"),
        ("9580", "Anteil für Konto 0880 Vollhafter"),
        ("9590", "Anteil für Konto 0890 Vollhafter"),
        
        ("9600", "Name des Gesellschafters Vollhafter"),
        ("9610", "Tätigkeitsvergütung Vollhafter"),
        ("9620", "Tantieme Vollhafter"),
        ("9630", "Darlehensverzinsung Vollhafter"),
        ("9640", "Gebrauchsüberlassung Vollhafter"),
        ("9650", "Sonstige Vergütungen Vollhafter"),
        ("9660", "Sonstige Vergütungen Vollhafter"),
        ("9670", "Sonstige Vergütungen Vollhafter"),
        ("9680", "Sonstige Vergütungen Vollhafter"),
        ("9690", "Restanteil Vollhafter"),
        
        ("9700", "Name des Gesellschafters Teilhafter"),
        ("9710", "Tätigkeitsvergütung Teilhafter"),
        ("9720", "Tantieme Teilhafter"),
        ("9730", "Darlehensverzinsung Teilhafter"),
        ("9740", "Gebrauchsüberlassung Teilhafter"),
        ("9750", "Sonstige Vergütungen Teilhafter"),
        ("9760", "Sonstige Vergütungen Teilhafter"),
        ("9770", "Sonstige Vergütungen Teilhafter"),
        ("9780", "Anteil für Konto 9840 Teilhafter"),
        ("9790", "Restanteil Teilhafter"),
        
        ("9802", "Gesamthänderisch gebundene Rücklagen - andere Kapitalkontenanpassungen"),
        ("9803", "Gewinnvortrag/Verlustvortrag - andere Kapitalkontenanpassungen"),
        ("9804", "Gesamthänderisch gebundene Rücklagen - Umbuchungen"),
        ("9805", "Gewinnvortrag/Verlustvortrag - Umbuchungen"),
        
        ("9806", "Zuzurechnender Anteil am Jahresüberschuss/Jahresfehlbetrag - je Gesellschafter"),
        ("9807", "Zuzurechnender Anteil am Bilanzgewinn/Bilanzverlust - je Gesellschafter"),
        ("9808", "Gegenkonto für zuzurechnenden Anteil am Jahresüberschuss/Jahresfehlbetrag"),
        ("9809", "Gegenkonto für zuzurechnenden Anteil am Bilanzgewinn/Bilanzverlust"),
        
        ("9810", "Kapitalkonto III"),
        ("9820", "Verlust-/Vortragskonto"),
        ("9830", "Verrechnungskonto für Einzahlungsverpflichtungen"),
        ("9840", "Kapitalkonto III"),
        ("9850", "Verrechnungskonto für Einzahlungsverpflichtungen"),
        
        ("9860", "Einzahlungsverpflichtungen persönlich haftender Gesellschafter"),
        ("9870", "Einzahlungsverpflichtungen Kommanditisten"),
        
        ("9880", "Ausgleichsposten für aktivierte eigene Anteile"),
        ("9883", "Nicht durch Vermögenseinlagen gedeckte Entnahmen persönlich haftender Gesellschafter"),
        ("9884", "Nicht durch Vermögenseinlagen gedeckte Entnahmen Kommanditisten"),
        ("9885", "Verrechnungskonto für nicht durch Vermögenseinlagen gedeckte Entnahmen persönlich haftender Gesellschafter"),
        ("9886", "Verrechnungskonto für nicht durch Vermögenseinlagen gedeckte Entnahmen Kommanditisten"),
        ("9887", "Steueraufwand der Gesellschafter"),
        ("9889", "Gegenkonto zu 9887"),
        
        ("9890", "Statistisches Konto für den Gewinnzuschlag nach §§ 6b Abs. 7 und 6c EStG (Haben)"),
        ("9891", "Gegenkonto zu statistischen Konten für den Gewinnzuschlag (Soll)"),
        ("9892", "Veränderung der gesamthänderisch gebundenen Rücklagen (Einlagen/Entnahmen)"),
        
        ("9893", "Umsatzsteuer in den Forderungen zum allgemeinen Umsatzsteuersatz (EÜR)"),
        ("9894", "Umsatzsteuer in den Forderungen zum ermäßigten Umsatzsteuersatz (EÜR)"),
        ("9895", "Gegenkonto 9893-9894 für die Aufteilung der Umsatzsteuer (EÜR)"),
        ("9896", "Vorsteuer in den Verbindlichkeiten zum allgemeinen Umsatzsteuersatz (EÜR)"),
        ("9897", "Vorsteuer in den Verbindlichkeiten zum ermäßigten Umsatzsteuersatz (EÜR)"),
        ("9898", "Vorsteuer in den Verbindlichkeiten aus verschiedenen Kosten (EÜR)"),
        ("9899", "Gegenkonto 9896-9897 für die Aufteilung der Vorsteuer (EÜR)"),
        ("9900", "Umsatzsteuer nicht fällig - sonstige Erlöse (EÜR)"),
        ("9901", "Gegenkonto zu 9900"),
        ("9902", "Umsatzsteuer in den Forderungen aus sonstigen Erlösen (EÜR)"),
        ("9906", "Steuerfreie Einnahmen und Entnahmen nach § 3 Nr. 72 EStG (Soll)"),
        ("9907", "Gegenkonto zu steuerfreien Einnahmen und Entnahmen nach § 3 Nr. 72 EStG (Haben)"),
        ("9908", "Nicht abzugsfähige Betriebsausgaben nach § 3c Abs. 1 EStG i. V. m. § 3 Nr. 72 EStG (Haben)"),
        ("9909", "Gegenkonto zu nicht abzugsfähigen Betriebsausgaben nach § 3c Abs. 1 EStG i. V. m. § 3 Nr. 72 EStG (Soll)"),
        
        ("9910", "Gegenkonto zur Minderung der Entnahmen § 4 Abs. 4a EStG"),
        ("9911", "Minderung der Entnahmen § 4 Abs. 4a EStG (Haben)"),
        ("9912", "Erhöhung der Entnahmen § 4 Abs. 4a EStG"),
        ("9913", "Gegenkonto zur Erhöhung der Entnahmen § 4 Abs. 4a EStG (Haben)"),
        ("9916", "Hinzurechnung Investitionsabzugsbetrag § 7g Abs. 2 EStG aus dem 2. vorangegangenen Wirtschaftsjahr, außerbilanziell (Haben)"),
        ("9917", "Hinzurechnung Investitionsabzugsbetrag § 7g Abs. 2 EStG aus dem 3. vorangegangenen Wirtschaftsjahr, außerbilanziell (Haben)"),
        ("9918", "Rückgängigmachung Investitionsabzugsbetrag § 7g Abs. 3 und 4 EStG im 2. vorangegangenen Wirtschaftsjahr"),
        ("9919", "Rückgängigmachung Investitionsabzugsbetrag § 7g Abs. 3 und 4 EStG im 3. vorangegangenen Wirtschaftsjahr"),
        
        ("9920", "Ausstehende Einlagen auf das Komplementär-Kapital, nicht eingefordert"),
        ("9930", "Ausstehende Einlagen auf das Komplementär-Kapital, eingefordert"),
        ("9940", "Ausstehende Einlagen auf das Kommandit-Kapital, nicht eingefordert"),
        ("9950", "Ausstehende Einlagen auf das Kommandit-Kapital, eingefordert"),
        
        ("9960", "Bewertungskorrektur zu Forderungen aus Lieferungen und Leistungen (Währungsumrechnung)"),
        ("9961", "Bewertungskorrektur zu sonstigen Verbindlichkeiten (Währungsumrechnung)"),
        ("9962", "Bewertungskorrektur zu Guthaben bei Kreditinstituten (Bewertung Finanzmittelfonds)"),
        ("9963", "Bewertungskorrektur zu Verbindlichkeiten gegenüber Kreditinstituten (Bewertung Finanzmittelfonds)"),
        ("9964", "Bewertungskorrektur zu Verbindlichkeiten aus Lieferungen und Leistungen (Währungsumrechnung)"),
        ("9965", "Bewertungskorrektur zu sonstigen Vermögensgegenständen (Währungsumrechnung)"),
        
        ("9970", "Investitionsabzugsbetrag § 7g Abs. 1 EStG, außerbilanziell (Soll)"),
        ("9971", "Investitionsabzugsbetrag § 7g Abs. 1 EStG, außerbilanziell (Haben) - Gegenkonto zu 9970"),
        ("9972", "Hinzurechnung Investitionsabzugsbetrag § 7g Abs. 2 EStG aus dem vorangegangenen Wirtschaftsjahr, außerbilanziell (Haben)"),
        ("9973", "Hinzurechnung Investitionsabzugsbetrag § 7g Abs. 2 EStG aus den vorangegangenen Wirtschaftsjahren, außerbilanziell (Soll) - Gegenkonto zu 9972, 9916, 9917"),
        ("9974", "Rückgängigmachung Investitionsabzugsbetrag § 7g Abs. 3 und 4 EStG im vorangegangenen Wirtschaftsjahr"),
        ("9975", "Rückgängigmachung Investitionsabzugsbetrag § 7g Abs. 3 und 4 EStG in den vorangegangenen Wirtschaftsjahren - Gegenkonto zu 9974, 9918, 9919"),
        
        ("9976", "Nicht abzugsfähige Zinsaufwendungen nach § 4h EStG (Haben)"),
        ("9977", "Nicht abzugsfähige Zinsaufwendungen nach § 4h EStG (Soll) - Gegenkonto zu 9976"),
        ("9978", "Abziehbare Zinsaufwendungen aus Vorjahren nach § 4h EStG (Soll)"),
        ("9979", "Abziehbare Zinsaufwendungen aus Vorjahren nach § 4h EStG (Haben) - Gegenkonto zu 9978"),
        
        ("9980", "Anteil Belastung auf Verbindlichkeitskonten"),
        ("9981", "Verrechnungskonto für Anteil Belastung auf Verbindlichkeitskonten"),
        ("9982", "Anteil Gutschrift auf Verbindlichkeitskonten"),
        ("9983", "Verrechnungskonto für Anteil Gutschrift auf Verbindlichkeitskonten"),
        
        ("9984", "Gewinnkorrektur nach § 60 Abs. 2 EStDV - Erhöhung handelsrechtliches Ergebnis durch Habenbuchung - Minderung handelsrechtliches Ergebnis durch Sollbuchung"),
        ("9985", "Gegenkonto zu 9984"),
        ("9986", "Ergebnisverteilung auf Fremdkapital"),
        ("9987", "Korrekturkonto für die Überleitungsrechnung"),
        ("9989", "Gegenkonto zu 9986-9988"),

        ("9990", "Erträge von außergewöhnlicher Größenordnung oder Bedeutung"),
        ("9991", "Erträge (aperiodisch)"),
        ("9992", "Erträge von außergewöhnlicher Größenordnung oder Bedeutung (aperiodisch)"),
        ("9993", "Aufwendungen von außergewöhnlicher Größenordnung oder Bedeutung"),
        ("9994", "Aufwendungen (aperiodisch)"),
        ("9995", "Aufwendungen von außergewöhnlicher Größenordnung oder Bedeutung (aperiodisch)"),
        ("9998", "Gegenkonto zu 9990-9997"),
    ]
    
    return accounts


def create_simple_mapping() -> pd.DataFrame:
    """
    Create a simple DataFrame with account number and German description
    """
    accounts = extract_datev_accounts()
    
    df = pd.DataFrame(accounts, columns=["Kontonummer", "Kontenbeschreibung"])
    
    # Add basic classification for line-item mapping
    df["Bilanzposition"] = df["Kontonummer"].apply(classify_account_type)
    df["GuV_Position"] = df["Kontonummer"].apply(classify_pnl_type)
    df["Bilanz_Seite"] = df["Kontonummer"].apply(classify_balance_sheet_side)
    
    return df


def classify_account_type(account_num: str) -> str:
    """Classify accounts into higher categories based on their headers"""
    num = int(account_num)
    
    # Anlage- und Kapitalkonten
    if 0 <= num <= 49:
        # There is one account before that does not have any higher level
        return "Immaterielle Vermögensgegenstände"
    elif 50 <= num <= 499:
        return "Sachanlagen"
    elif 500 <= num <= 599:
        return "Finanzanlagen"
    elif 600 <= num <= 799:
        return "Verbindlichkeiten"
    elif 800 <= num <= 839:
        # There is a "Kapital" in front here as well, do we use that as well?
        return "Kapitalgesellschaft"
    elif 840 <= num <= 845:
        return "Kapitalrücklage"
    elif 846 <= num <= 869:
        return "Gewinnrücklagen"
    elif 870 <= num <= 889:
        # There is also a "Kapital" in front here as well, do we use that as well?
        return "Eigenkapital Vollhafter/Einzelunternehmer"
    elif 890 <= num <= 899:
        return "Fremdkapital Vollhafter"
    elif 900 <= num <= 919:
        return "Eigenkapital Teilhafter"
    elif 920 <= num <= 929:
        return "Fremdkapital Teilhafter"
    elif 930 <= num <= 949:
        return "Sonderposten mit Rücklageanteil"
    elif 950 <= num <= 979:
        return "Rückstellungen"
    elif 980 <= num <= 999:
        return "Abgrenzungsposten"
    
    # Finanz- und Privatkonten
    elif 1000 <= num <= 1339:
        return "Kassenbestand, Bundesbank- und Postbankguthaben, Guthaben bei Kreditinstituten und Schecks"
    elif 1340 <= num <= 1349:
        return "Wertpapiere"
    elif 1350 <= num <= 1599:
        return "Forderungen und sonstige Vermögensgegenstände"
    elif 1600 <= num <= 1799:
        return "Verbindlichkeiten"
    elif 1800 <= num <= 1899:
        return "Privat (Eigenkapital) Vollhafter/Einzelunternehmer"
    elif 1900 <= num <= 1999:
        return "Privat (Fremdkapital) Teilhafter"
    
    # Abgrenzungskonten
    elif 2000 <= num <= 2009:
        return "Sonstige betriebliche Aufwendungen"
    elif 2010 <= num <= 2020:
        return "Betriebsfremde und periodenfremde Aufwendungen"
    elif 2030 <= num <= 2099:
        return "Aufwendungen aus der Anwendung von Übergangsvorschriften i. S. d. BilMoG"
    elif 2100 <= num <= 2199:
        return "Zinsen und ähnliche Aufwendungen"
    elif 2200 <= num <= 2299:
        return "Steuern vom Einkommen und Ertrag"
    elif 2300 <= num <= 2499:
        return "Sonstige Aufwendungen"
    elif 2500 <= num <= 2509:
        return "Sonstige betriebliche Erträge"
    elif 2510 <= num <= 2520:
        return "Betriebsfremde und periodenfremde Erträge"
    elif 2530 <= num <= 2599:
        return "Erträge aus der Anwendung von Übergangsvorschriften i. S. d. BilMoG"
    elif 2600 <= num <= 2699:
        return "Zinserträge"
    elif 2700 <= num <= 2870:
        return "Sonstige Erträge"
    elif 2880 <= num <= 2999:
        return "Verrechnete kalkulatorische Kosten"
    
    # Wareneingangs- und Bestandskonten
    elif 3000 <= num <= 3109:
        return "Materialaufwand"
    elif 3110 <= num <= 3969:
        return "Umsätze, für die als Leistungsempfänger die Steuer nach § 13b UStG geschuldet wird"
    elif 3970 <= num <= 3889:
        return "Bestand an Vorräten"
    elif 3990 <= num <= 3999:
        return "Verrechnete Stoffkosten"
    
    # Betriebliche Aufwendungen
    elif 4000 <= num <= 4099:
        return "Material- und Stoffverbrauch"
    elif 4100 <= num <= 4199:
        return "Personalaufwendungen"
    elif 4200 <= num <= 4989:
        return "Sonstige betriebliche Aufwendungen und Abschreibungen"
    elif 4990 <= num <= 4995:
        return "Kalkulatorische Kosten"
    elif 4996 <= num <= 4999:
        return "Kosten bei Anwendung des Umsatzkostenverfahrens"
    
    # There are no 5000-6999 accounts and headers, therefore it continues at 7000
    
    # Bestände an Erzeugnissen
    elif 7000 <= num <= 7999:
        return "Bestände an Erzeugnissen"
    
    # Erlöskonten
    elif 8000 <= num <= 8499:
        return "Umsatzerlöse"
    elif 8500 <= num <= 8579:
        return "Konten für die Verbuchung von Sonderbetriebseinnahmen"
    elif 8580 <= num <= 8999:
        return "Statistische Konten EÜR"
    
    # Vortrags-, Kapital-, Korrektur- und statistische Konten
    elif 9000 <= num <= 9100:
        return "Vortragskonten"
    elif 9101 <= num <= 9140:
        return "Statistische Konten für betriebswirtschaftliche Auswertungen (BWA)"
    elif num in [9141, 9142]:
        return "Variables Kapital Teilhafter"
    elif 9143 <= num <= 9145:
        return "Sammelposten anrechenbare Privatsteuern"
    elif 9146 <= num <= 9149:
        return "Kapitaländerungen durch Übertragung einer § 6b EStG Rücklage"
    elif 9150 <= num <= 9156:
        return " Andere Kapitalkontenanpassungen: Vollhafter"
    elif 9157 <= num <= 9159:
        return "Anrechenbare Privatsteuern Vollhafter, Eigenkapital"
    elif 9160 <= num <= 9166:
        return "Andere Kapitalrücklagenanpassungen: Teilhafter"
    elif 9167 <= num <= 9169:
        return "Anrechenbare Privatsteuern Teilhafter, Eigenkapital"
    elif 9167 <= num <= 9169:
        return "Anrechenbare Privatsteuern Teilhafter, Eigenkapital"
    elif 9170 <= num <= 9179:
        return "Umbuchungen auf andere Kapitalkonten: Vollhafter"
    elif 9180 <= num <= 9185:
        return "Umbuchungen auf andere Kapitalkonten: Teilhafter"
    elif 9186 <= num <= 9189:
        return "Anrechenbare Privatsteuern Teilhafter, Fremdkapital"
    elif 9190 <= num <= 9199:
        return "Gegenkonten zu statistischen Konten für Betriebswirtschaftliche Auswertungen"
    # The following are have the same header twice so they are summed up into one
    elif 9200 <= num <= 9219:
        return "Statistische Konten für die Kennzahlen der Bilanz"
    elif 9220 <= num <= 9229:
        return "Statistische Konten zur informativen Angabe des gezeichneten Kapitals in anderer Währung"
    elif 9240 <= num <= 9259:
        return "Statistische Konten für die Kapitalflussrechnung"
    elif 9260 <= num <= 9269:
        return "Aufgliederung der Rückstellungen für die Programme der Wirtschaftsforschung"
    elif 9270 <= num <= 9279:
        return "Statistische Konten für in der Bilanz auszuweisende Haftungsverhältnisse"    
    elif 9280 <= num <= 9284:
        return "Statistische Konten für die im Anhang anzugebenden sonstigen finanziellen Verpflichtungen"
    elif num in [9285, 9286]:
        return "Unterschiedsbeträge aus der Abzinsung von Altersversorgungsverpflichtungen nach § 253 Abs. 6 HGB"
    elif 9287 <= num <= 9399:
        return "Statistische Konten für § 4 Abs. 3 EStG"
    elif 9400 <= num <= 9499:
        return "Privat Teilhafter (Eigenkapital, für Verrechnung mit Kapitalkonto III - Konto 9840)"
    elif 9500 <= num <= 9799:
        return "Statistische Konten für die Kapitalfortentwicklung"
    elif 9802 <= num <= 9805:
        return "Rücklagen, Gewinn-, Verlustvorträge"
    elif 9806 <= num <= 9809:
        return "Statistische Anteile an den Posten Jahresüberschuss/-fehlbetrag bzw. Bilanzgewinn/-verlust"
    elif 9810 <= num <= 9839:
        return "Kapital Personengesellschaft Vollhafter"
    elif 9840 <= num <= 9859:
        return "Kapital Personengesellschaft Teilhafter"
    elif 9860 <= num <= 9879:
        return "Einzahlungsverpflichtungen im Bereich der Forderungen"
    elif num == 9880:
        return "Ausgleichsposten für aktivierte eigene Anteile"
    elif num in [9883, 9884]:
        return "Nicht durch Vermögenseinlagen gedeckte Entnahmen"
    elif num in [9885, 9886]:
        return "Verrechnungskonto für nicht durch Vermögenseinlagen gedeckte Entnahmen"
    elif num in [9887, 9888]:
        return "Steueraufwand der Gesellschafter"
    elif num in [9890, 9891]:
        return "Statistische Konten für Gewinnzuschlag"
    elif num == 9892:
        return "Veränderung der gesamthänderisch gebundenen Rücklagen (Einlagen/Entnahmen)"
    elif 9893 <= num <= 9909:
        return "Vorsteuer-/Umsatzsteuerkonten zur Korrektur der Forderungen/Verbindlichkeiten (EÜR)"
    elif 9910 <= num <= 9913:
        return "Statistische Konten für § 4 Abs. 4a EStG"
    elif 9914 <= num <= 9919:
        return "Statistische Konten für den außerhalb der Bilanz zu berücksichtigenden Investitionsabzugsbetrag nach § 7g EStG"
    elif 9920 <= num <= 9959:
        return "Ausstehende Einlagen"
    elif 9960 <= num <= 9969:
        return "Konten zu Bewertungskorrekturen"
    elif 9970 <= num <= 9975:
        return "Statistische Konten für den außerhalb der Bilanz zu berücksichtigenden Investitionsabzugsbetrag nach § 7g EStG"
    elif 9976 <= num <= 9979:
        return "Statistische Konten für die Zinsschranke § 4h EStG bzw. § 8a KStG"
    elif 9980 <= num <= 9983:
        return "Statistische Konten für den GuVAusweis in \"Gutschrift bzw. Belastung auf Verbindlichkeitskonten\" bei den Auswertungen für PersHG nach KapCoRiLiG"
    elif num in [9984, 9985]:
        return "Statistische Konten für die Gewinnkorrektur nach § 60 Abs. 2 EStDV"
    elif 9986 <= num <= 9989:
        return "Statistische Konten für Korrekturbuchungen in der Überleitungsrechnung"
    elif 9990 <= num <= 9998:
        return "Statistische Konten für außergewöhnliche und aperiodische Geschäftsvorfälle für Anhangsangabe nach § 285 Nr. 31 und Nr. 32 HGB"
    elif 10000 <= num <= 99999:
        return "Personenkonten"
    else:
        return "N/A"
    
    

def classify_pnl_type(account_num: str) -> str:
    """Classify P&L accounts"""
    num = int(account_num)
    
    if 2000 <= num <= 2999:
        return "Finanzergebnis"
    elif 3000 <= num <= 3999:
        return "Materialaufwand"
    elif 4000 <= num <= 4199:
        return "Materialaufwand"
    elif 4100 <= num <= 4199:
        return "Personalaufwand"
    elif 4200 <= num <= 4999:
        return "Sonstige betriebliche Aufwendungen"
    elif 8000 <= num <= 8999:
        return "Umsatzerlöse"
    else:
        return "N/A"

def classify_balance_sheet_side(account_num: str) -> str:
    """Classify balance sheet side"""
    num = int(account_num)
    
    if 0 <= num <= 1599:
        return "Aktiva"
    elif 1600 <= num <= 1999:
        if 1600 <= num <= 1799:
            return "Passiva"
        else:
            return "Aktiva"
    elif num >= 600 and num <= 999:
        return "Passiva"
    else:
        return "N/A"

def save_to_excel(df: pd.DataFrame, filename: str = "../../data/raw/excel/datev_skr03_account_mapping.xlsx") -> str:
    """Save DataFrame to Excel file with formatting"""
    
    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        # Main sheet with all accounts
        df.to_excel(writer, sheet_name="Alle_Konten", index=False)
        
        # Separate sheets by major categories
        aktiva_accounts = df[df["Bilanz_Seite"] == "Aktiva"]
        passiva_accounts = df[df["Bilanz_Seite"] == "Passiva"]
        balance_sheet_accounts = pd.concat([aktiva_accounts, passiva_accounts], ignore_index=True)
        balance_sheet_accounts.to_excel(writer, sheet_name="Bilanzkonten", index=False)
        
        pnl_accounts = df[df["GuV_Position"] != "N/A"]
        pnl_accounts.to_excel(writer, sheet_name="GuV_Konten", index=False)
        
        # Summary by position
        summary = df.groupby("Bilanzposition").size().reset_index(name="Anzahl_Konten")
        summary.to_excel(writer, sheet_name="Zusammenfassung", index=False)
    
    print(f"Excel-Datei erstellt: {filename}")
    print(f"Anzahl Konten gesamt: {len(df)}")
    print(f"Bilanzkonten: {len(balance_sheet_accounts)}")
    print(f"GuV-Konten: {len(pnl_accounts)}")
    
    return filename

# Main execution
if __name__ == "__main__":
    print("Extrahiere DATEV SKR 03 Konten...")
    
    # Create the mapping
    df = create_simple_mapping()
    
    # Save to Excel
    filename = save_to_excel(df)
    
    # Display sample
    print("\nBeispiel der ersten 20 Konten:")
    print(df.head(20).to_string(index=False))
    
    # Display summary statistics
    print(f"\nKonten nach Bilanzpositionen:")
    print(df["Bilanzposition"].value_counts())
    








# Edit this, then put it somewhere up top, auf Bilanz- oder GuV-Posten achten

def classify_position_level(account_num: str) -> str:
    """Classify accounts into detailed position levels based on their positions
    as seen in leftmost and middle column in SKR03 framework."""
    num = int(account_num)
    
    # Anlage- und Kapitalkonten    
    if num < 10:
        return "Rückständige fällige Einzahlungen auf Geschäftsanteile"
    # Immaterielle Vermögensgegenstände
    elif 10 <= num <= 30:
        return "Entgeltlich erworbene Konzessionen, gewerbliche Schutzrechte und ähnliche Rechte und Werte sowie Lizenzen an solchen Rechten und Werten"
    elif num == 35:
        return "Geschäfts- oder Firmenwert"
    elif num in [38, 39]:
        return "Geleistete Anzahlungen"
    elif 43 <= num <= 48:
        return "Selbst geschaffene gewerbliche Schutzrechte und ähnliche Rechte und Werte"
    # Sachanlagen
    elif 50 <= num <= 75 or 80 <= num <= 115 or 140 <= num <= 149 or 160 <= num <= 179 or 190 <= num <= 194:
        return "Grundstücke, grundstücksgleiche Rechte und Bauten einschließlich der Bauten auf fremden Grundstücken"
    elif num == 79 or num in [120, 129] or num in [150, 159] or num in [180, 189] or num in [195, 199] or num in [290, 299] or num in [498, 499]:
        return "Geleistete Anzahlungen und Anlagen im Bau"
    elif 200 <= num <= 280:
        return "Technische Anlagen und Maschinen"
    elif 300 <= num <= 490:
        return "Andere Anlagen, Betriebs- und Geschäftsausstattung"
    # Finanzanlagen
    elif 500 <= num <= 504 or num == 509:
        return "Anteile an verbundenen Unternehmen"
    elif 505 <= num <= 508:
        return "Ausleihungen an verbundene Unternehmen"
    elif 510 <= num <= 519:
        return "Beteiligungen"
    elif 520 <= num <= 524:
        return "Ausleihungen an Unternehmen, mit denen ein Beteiligungsverhältnis besteht"
    elif 525 <= num <= 538:
        return "Wertpapiere des Anlagevermögens"
    elif 540 <= num <= 550 or 580 <= num <= 590:
        return "Sonstige Ausleihungen"
    elif num == 570:
        return "Genossenschaftsanteile"
    elif num == 595:
        return "Rückdeckungsansprüche aus Lebensversicherungen"
        # Verbindlichkeiten
    elif 600 <= num <= 625:
        return "Anleihen"
    elif 630 <= num <= 690:
        return "Verbindlichkeiten gegenüber Kreditinstituten oder Kassenbestand, Bundesbankguthaben, Guthaben bei Kreditinstituten und Schecks"
    elif num == 699:
        return "Verbindlichkeiten gegenüber Kreditinstituten"
    elif 700 <= num <= 710:
        return "Verbindlichkeiten gegenüber verbundenen Unternehmen oder Forderungen gegen verbundene Unternehmen"
    elif 715 <= num <= 729:
        return "Verbindlichkeiten gegenüber Unternehmen, mit denen ein Beteiligungsverhältnis besteht oder Forderungen gegen Unternehmen, mit denen ein Beteiligungsverhältnis besteht"
    elif 730 <= num <= 799:
        return "Sonstige Verbindlichkeiten"
    # Kapital Kapitalgesellschaft
    elif 800 <= num <= 815:
        return "Gezeichnetes Kapital"
    elif num == 819:
        return "Eigene Anteile"
    elif 820 <= num <= 829:
        return "Nicht eingeforderte ausstehende Einlagen"
    elif 830 <= num <= 838:
        return "Eingeforderte, noch ausstehende Kapitaleinlagen"
    elif num == 839:
        return "Nachschüsse"
    elif 840 <= num <= 845:
        return "Kapitalrücklage"
    # Gewinnrücklagen
    elif num == 846:
        return "Gesetzliche Rücklage"
    elif num == 848:
        return "Andere Gewinnrücklagen"
    elif num == 849:
        return "Rücklage für Anteile an einem herrschenden oder mehrheitlich beteiligten Unternehmen"
    # This is kind of an edge case as 852 is in between and does not really seem to belong here
    elif num == 851:
        return "Satzungsmäßige Rücklagen"
    # GPT said to go with 852 onwards even though there is no position label here
    elif 852 <= num <= 859:
        return "Andere Gewinnrücklagen"
    elif 860 <= num <= 868:
        return "Gewinnvortrag oder Verlustvortrag"
    # Eigenkapital Vollhafter/Einzelunternehmer
    elif 870 <= num <= 881:
        return "Eigenkapital Vollhafter/Einzelunternehmer"
    # Fremdkapital Vollhafter
    elif 890 <= num <= 899:
        return "Fremdkapital Vollhafter"
    # Eigenkapital Teilhafter
    elif 900 <= num <= 919:
        return "Eigenkapital Teilhafter"
    # Fremdkapital Teilhafter
    elif 920 <= num <= 929:
        return "Fremdkapital Teilhafter"
    # Sonderposten mit Rücklageanteil
    elif 930 <= num <= 947:
        return "Sonderposten mit Rücklageanteil"
    # Sonderposten für Zuschüsse und Zulagen
    elif 948 <= num <= 949:
        return "Sonderposten für Zuschüsse und Zulagen"
    # Rückstellungen für Pensionen
    elif num == 950 or 952 <= num <= 954:
        return "Rückstellungen für Pensionen und ähnliche Verpflichtungen"
    elif num == 951:
        return "Rückstellungen für Pensionen und ähnliche Verpflichtungen oder aktiver Unterschiedsbetrag aus der Vermögensverrechnung"
    elif num in [955, 956] or num in [962, 963]:
        return "Steuerrückstellungen"
    elif num == 961 or 964 <= num <= 966:
        return "Sonstige Rückstellungen"
    elif num == 967:
        return "Sonstige Rückstellungen oder aktiver Unterschiedsbetrag aus der Vermögensverrechnung"
    elif num == 968:
        return "Passive latente Steuern"
    elif num == 969:
        return "Steuerrückstellungen"
    elif 970 <= num <= 979:
        return "Sonstige Rückstellungen"
    # Abgrenzungsposten
    elif num == 980 or 984 <= num <= 986:
        return "Rechnungsabgrenzungsposten (Aktiva)"
    elif num == 983:
        return "Aktive latente Steuern"
    elif 987 <= num <= 989:
        return "Andere Gewinnrücklagen"
    elif num == 990:
        return "Rechnungsabgrenzungsposten (Passiva)"
    elif num == 992:
        return "Sonstige Aktiva oder sonstige Passiva"
    elif 996 <= num <= 999:
        return "Forderungen aus Lieferungen und Leistungen H-Saldo"
    
    # Finanz- und Privatkonten    
    # Kassenbestand, Bundesbank- und Postbankguthaben, Guthaben bei Kreditinstituten und Schecks 
    elif 1000 <= num <= 1020 or num == 1330:
        return "Kassenbestand, Bundesbankguthaben, Guthaben bei Kreditinstituten und Schecks"
    elif 1100 <= num <= 1295:
        return "Kassenbestand, Bundesbankguthaben, Guthaben bei Kreditinstituten und Schecks oder Verbindlichkeiten gegenüber Kreditinstituten"    
    elif 1300 <= num <= 1309:
        return "Forderungen aus Lieferungen und Leistungen oder sonstige Verbindlichkeiten"
    elif 1310 <= num <= 1319:
        return "Forderungen gegen verbundene Unternehmen oder Verbindlichkeiten gegenüber verbundenen Unternehmen"
    elif 1320 <= num <= 1326:
        return "Forderungen gegenüber Unternehmen, mit denen ein Beteiligungsverhältnis besteht oder Verbindlichkeiten gegenüber Unternehmen, mit denen ein Beteiligungsverhältnis besteht"
    elif 1327 <= num <= 1329:
        return "Sonstige Wertpapiere"
    elif 1340 <= num <= 1344:
        return "Anteile an verbundenen Unternehmen"
    elif 1348 <= num <= 1349:
        return "Sonstige Wertpapiere"
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # Ab hier weitermachen
    elif 1350 <= num <= 1353:
        return "Sonstige Vermögensgegenstände"
    elif num == 1354:
        return "Aktiver Unterschiedsbetrag aus der Vermögensverrechnung oder sonstige Rückstellungen"
    elif 1355 <= num <= 1356:
        return "Sonstige Vermögensgegenstände"
    elif num == 1357:
        return "Aktiver Unterschiedsbetrag aus der Vermögensverrechnung oder Rückstellungen für Pensionen und ähnliche Verpflichtungen"
    elif 1358 <= num <= 1371:
        return "Sonstige Vermögensgegenstände oder sonstige Verbindlichkeiten"
    elif num == 1372:
        return "Wirtschaftsgüter des Umlaufvermögens nach § 4 Abs. 3 Satz 4 EStG"
    elif 1373 <= num <= 1394:
        return "Sonstige Vermögensgegenstände"
    elif num == 1394:
        return "Sonstige Vermögensgegenstände oder sonstige Verbindlichkeiten - Forderungen gegen Gesellschaft/Gesamthand"
    
    # Forderungen aus Lieferungen und Leistungen
    elif 1400 <= num <= 1449:
        return "Forderungen aus Lieferungen und Leistungen oder sonstige Verbindlichkeiten"
    elif 1450 <= num <= 1465:
        return "Forderungen aus Lieferungen und Leistungen oder sonstige Verbindlichkeiten"
    elif 1470 <= num <= 1475:
        return "Forderungen gegen verbundene Unternehmen oder Verbindlichkeiten gegenüber verbundenen Unternehmen"
    elif 1478 <= num <= 1479:
        return "Forderungen gegen verbundene Unternehmen H-Saldo"
    elif 1480 <= num <= 1485:
        return "Forderungen gegen Unternehmen, mit denen ein Beteiligungsverhältnis besteht oder Verbindlichkeiten gegenüber Unternehmen, mit denen ein Beteiligungsverhältnis besteht"
    elif 1488 <= num <= 1489:
        return "Forderungen gegen Unternehmen, mit denen ein Beteiligungsverhältnis besteht H-Saldo"
    elif 1490 <= num <= 1495:
        return "Forderungen aus Lieferungen und Leistungen oder sonstige Verbindlichkeiten"
    elif num == 1498:
        return "Forderungen aus Lieferungen und Leistungen H-Saldo"
    elif num == 1499:
        return "Forderungen aus Lieferungen und Leistungen H-Saldo oder sonstige Verbindlichkeiten S-Saldo"
    
    # Sonstige Vermögensgegenstände
    elif 1500 <= num <= 1509:
        return "Sonstige Vermögensgegenstände"
    
    # Geleistete Anzahlungen
    elif 1510 <= num <= 1518:
        return "Geleistete Anzahlungen"
    
    # Sonstige Vermögensgegenstände (Fortsetzung)
    elif 1519 <= num <= 1593:
        return "Sonstige Vermögensgegenstände"
    elif num == 1593:
        return "Sonstige Verbindlichkeiten S-Saldo"
    elif 1594 <= num <= 1596:
        return "Forderungen gegen verbundene Unternehmen oder Verbindlichkeiten gegenüber verbundenen Unternehmen"
    elif 1597 <= num <= 1599:
        return "Forderungen gegen Unternehmen, mit denen ein Beteiligungsverhältnis besteht oder Verbindlichkeiten gegenüber Unternehmen, mit denen ein Beteiligungsverhältnis besteht"
    
    # Verbindlichkeiten aus Lieferungen und Leistungen
    elif 1600 <= num <= 1624:
        return "Verbindlichkeiten aus Lieferungen und Leistungen oder sonstige Vermögensgegenstände"
    elif 1625 <= num <= 1628:
        return "Verbindlichkeiten aus Lieferungen und Leistungen"
    elif 1630 <= num <= 1638:
        return "Verbindlichkeiten gegenüber verbundenen Unternehmen oder Forderungen gegen verbundene Unternehmen"
    elif 1640 <= num <= 1648:
        return "Verbindlichkeiten gegenüber Unternehmen, mit denen ein Beteiligungsverhältnis besteht oder Forderungen gegen Unternehmen, mit denen ein Beteiligungsverhältnis besteht"
    elif 1650 <= num <= 1658:
        return "Verbindlichkeiten aus Lieferungen und Leistungen oder sonstige Vermögensgegenstände"
    elif num == 1659:
        return "Verbindlichkeiten aus Lieferungen und Leistungen S-Saldo oder sonstige Vermögensgegenstände H-Saldo"
    
    # Verbindlichkeiten aus Wechseln
    elif 1660 <= num <= 1664:
        return "Verbindlichkeiten aus der Annahme gezogener Wechsel und aus der Ausstellung eigener Wechsel"
    
    # Sonstige Verbindlichkeiten
    elif 1665 <= num <= 1709:
        return "Sonstige Verbindlichkeiten"
    
    # Erhaltene Anzahlungen
    elif 1710 <= num <= 1721:
        return "Erhaltene Anzahlungen auf Bestellungen (Passiva)"
    elif num == 1722:
        return "Erhaltene Anzahlungen auf Bestellungen (Aktiva)"
    
    # Sonstige Verbindlichkeiten oder sonstige Vermögensgegenstände
    elif 1725 <= num <= 1799:
        return "Sonstige Verbindlichkeiten oder sonstige Vermögensgegenstände"
    elif 1760 <= num <= 1794:
        return "Steuerrückstellungen oder sonstige Vermögensgegenstände"
    elif num == 1793:
        return "Sonstige Vermögensgegenstände H-Saldo"
    
    # Privat (Eigenkapital)
    elif 1800 <= num <= 1891:
        return "Privat (Eigenkapital) Vollhafter/Einzelunternehmer"
    
    # Privat (Fremdkapital) Teilhafter
    elif 1900 <= num <= 1999:
        return "Privat (Fremdkapital) Teilhafter"
    
    # === KLASSE 2: ABGRENZUNGSKONTEN ===
    
    # Sonstige betriebliche Aufwendungen
    elif 2000 <= num <= 2009:
        return "Sonstige betriebliche Aufwendungen"
    elif 2010 <= num <= 2020:
        return "Betriebsfremde und periodenfremde Aufwendungen"
    elif 2090 <= num <= 2094:
        return "Aufwendungen aus der Anwendung von Übergangsvorschriften i. S. d. BilMoG"
    
    # Zinsen und ähnliche Aufwendungen
    elif 2100 <= num <= 2145:
        return "Zinsen und ähnliche Aufwendungen"
    elif 2146 <= num <= 2147:
        return "Zinsen und ähnliche Aufwendungen oder sonstige Zinsen und ähnliche Erträge"
    elif 2148 <= num <= 2149:
        return "Zinsen und ähnliche Aufwendungen"
    
    # Sonstige betriebliche Aufwendungen
    elif 2150 <= num <= 2176:
        return "Sonstige betriebliche Aufwendungen"
    
    # Steuern vom Einkommen und Ertrag
    elif 2200 <= num <= 2283:
        return "Steuern vom Einkommen und Ertrag"
    
    # Sonstige Steuern
    elif 2285 <= num <= 2289:
        return "Sonstige Steuern"
    
    # Sonstige Aufwendungen
    elif 2300 <= num <= 2309:
        return "Sonstige betriebliche Aufwendungen"
    elif 2310 <= num <= 2328:
        return "Sonstige betriebliche Aufwendungen - Anlagenabgänge"
    elif num == 2315:
        return "Sonstige betriebliche Erträge - Anlagenabgänge (bei Buchgewinn)"
    elif num == 2316:
        return "Sonstige betriebliche Erträge - Anlagenabgänge (bei Buchgewinn)"
    elif num == 2317:
        return "Sonstige betriebliche Erträge - Anlagenabgänge (bei Buchgewinn)"
    elif num == 2318:
        return "Sonstige betriebliche Erträge - Anlagenabgänge (bei Buchgewinn)"
    elif 2339 <= num <= 2347:
        return "Sonstige betriebliche Aufwendungen - Einstellungen in Rücklagen"
    elif num == 2350:
        return "Sonstige Grundstücksaufwendungen (neutral)"
    elif num == 2375:
        return "Sonstige Steuern - Grundsteuer"
    elif 2380 <= num <= 2390:
        return "Sonstige betriebliche Aufwendungen - Zuwendungen und Spenden"
    elif 2400 <= num <= 2409:
        return "Sonstige betriebliche Aufwendungen - Forderungsverluste (übliche Höhe)"
    elif 2430 <= num <= 2449:
        return "Abschreibungen auf Vermögensgegenstände des Umlaufvermögens, soweit diese die in der Kapitalgesellschaft üblichen Abschreibungen überschreiten"
    elif 2450 <= num <= 2451:
        return "Sonstige betriebliche Aufwendungen - Einstellungen in Wertberichtigungen"
    elif num == 2480:
        return "Einstellungen in Gewinnrücklagen in die Rücklage für Anteile an einem herrschenden oder mehrheitlich beteiligten Unternehmen"
    elif num == 2481:
        return "Einstellungen in gesamthänderisch gebundene Rücklagen"
    elif 2485 <= num <= 2489:
        return "Einstellungen in Gewinnrücklagen"
    elif num == 2490:
        return "Aufwendungen aus Verlustübernahme"
    elif num == 2491:
        return "Auf Grund einer Gewinngemeinschaft, eines Gewinn- oder Teilgewinnabführungsvertrags abgeführte Gewinne oder Erträge aus Verlustübernahme"
    elif num == 2492:
        return "Auf Grund einer Gewinngemeinschaft, eines Gewinn- oder Teilgewinnabführungsvertrags abgeführte Gewinne"
    elif num == 2493:
        return "Auf Grund einer Gewinngemeinschaft, eines Gewinn- oder Teilgewinnabführungsvertrags abgeführte Gewinne oder Erträge aus Verlustübernahme"
    elif num == 2494:
        return "Auf Grund einer Gewinngemeinschaft, eines Gewinn- oder Teilgewinnabführungsvertrags abgeführte Gewinne"
    elif num == 2495:
        return "Einstellung in die Kapitalrücklage nach den Vorschriften über die vereinfachte Kapitalherabsetzung"
    elif num == 2496:
        return "Einstellungen in Gewinnrücklagen in die gesetzliche Rücklage"
    elif num == 2497:
        return "Einstellungen in Gewinnrücklagen in satzungsmäßige Rücklagen"
    elif num == 2498:
        return "Einstellungen in Gewinnrücklagen in die Rücklage für Anteile an einem herrschenden oder mehrheitlich beteiligten Unternehmen"
    elif num == 2499:
        return "Einstellungen in Gewinnrücklagen in andere Gewinnrücklagen"
    
    # Sonstige betriebliche Erträge
    elif 2504 <= num <= 2509:
        return "Sonstige betriebliche Erträge"
    elif 2510 <= num <= 2520:
        return "Betriebsfremde und periodenfremde Erträge"
    elif 2590 <= num <= 2594:
        return "Erträge aus der Anwendung von Übergangsvorschriften i. S. d. BilMoG"
    
    # Zinserträge - Erträge aus Beteiligungen
    elif 2600 <= num <= 2649:
        return "Erträge aus Beteiligungen"
    
    # Zinserträge - Erträge aus anderen Wertpapieren und Ausleihungen
    elif 2650 <= num <= 2689:
        return "Sonstige Zinsen und ähnliche Erträge"
    elif 2686 <= num <= 2687:
        return "Sonstige Zinsen und ähnliche Erträge oder Zinsen und ähnliche Aufwendungen"
    
    # Sonstige Erträge
    elif 2700 <= num <= 2749:
        return "Sonstige betriebliche Erträge"
    elif 2750 <= num <= 2752:
        return "Umsatzerlöse - Grundstückserträge"
    elif 2760 <= num <= 2764:
        return "Sonstige betriebliche Erträge"
    elif num == 2790:
        return "Erträge aus Verlustübernahme"
    elif num == 2792:
        return "Auf Grund einer Gewinngemeinschaft, eines Gewinn- oder Teilgewinnabführungsvertrags erhaltene Gewinne"
    elif num == 2794:
        return "Auf Grund einer Gewinngemeinschaft, eines Gewinn- oder Teilgewinnabführungsvertrags erhaltene Gewinne"    
    elif num == 2795:
        return "Entnahmen aus der Kapitalrücklage"
    elif num == 2796:
        return "Entnahmen aus Gewinnrücklagen aus der gesetzlichen Rücklage"
    elif num == 2797:
        return "Entnahmen aus Gewinnrücklagen aus satzungsmäßigen Rücklagen"
    elif num == 2798:
        return "Entnahmen aus Gewinnrücklagen aus der Rücklage für Anteile an einem herrschenden oder mehrheitlich beteiligten Unternehmen"
    elif num == 2799:
        return "Entnahmen aus Gewinnrücklagen aus anderen Gewinnrücklagen"
    elif num == 2840:
        return "Entnahmen aus Gewinnrücklagen aus der Rücklage für Anteile an einem herrschenden oder mehrheitlich beteiligten Unternehmen"
    elif num == 2841:
        return "Entnahmen aus gesamthänderisch gebundenen Rücklagen"
    elif num == 2850:
        return "Entnahmen aus anderen Ergebnisrücklagen"
    elif 2860 <= num <= 2868:
        return "Gewinnvortrag oder Verlustvortrag"
    elif num == 2870:
        return "Ausschüttung"
    elif 2890 <= num <= 2895:
        return "Verrechnete kalkulatorische Kosten - Sonstige betriebliche Aufwendungen"
    
    # === KLASSE 3: WARENEINGANGS- UND BESTANDSKONTEN ===
    
    # Materialaufwand - Roh-, Hilfs- und Betriebsstoffe
    elif 3000 <= num <= 3098:
        return "Aufwendungen für Roh-, Hilfs- und Betriebsstoffe und für bezogene Waren"
    elif num == 3100:
        return "Aufwendungen für bezogene Leistungen"
    elif 3106 <= num <= 3109:
        return "Aufwendungen für bezogene Leistungen"
    
    # Umsätze § 13b UStG
    elif 3110 <= num <= 3165:
        return "Umsätze, für die als Leistungsempfänger die Steuer nach § 13b UStG geschuldet wird - Aufwendungen für bezogene Leistungen"
    elif 3170 <= num <= 3185:
        return "Aufwendungen für bezogene Leistungen"
    
    # Wareneingang
    elif 3200 <= num <= 3349:
        return "Aufwendungen für Roh-, Hilfs- und Betriebsstoffe und für bezogene Waren - Wareneingang"
    elif 3400 <= num <= 3599:
        return "Aufwendungen für Roh-, Hilfs- und Betriebsstoffe und für bezogene Waren - Wareneingang"
    elif 3600 <= num <= 3669:
        return "Nicht abziehbare Vorsteuer"
    
    # Nachlässe
    elif 3700 <= num <= 3729:
        return "Aufwendungen für Roh-, Hilfs- und Betriebsstoffe und für bezogene Waren - Nachlässe"
    
    # Erhaltene Skonti
    elif 3730 <= num <= 3749:
        return "Aufwendungen für Roh-, Hilfs- und Betriebsstoffe und für bezogene Waren - Erhaltene Skonti"
    
    # Erhaltene Boni
    elif 3750 <= num <= 3769:
        return "Aufwendungen für Roh-, Hilfs- und Betriebsstoffe und für bezogene Waren - Erhaltene Boni"
    
    # Erhaltene Rabatte
    elif 3770 <= num <= 3799:
        return "Aufwendungen für Roh-, Hilfs- und Betriebsstoffe und für bezogene Waren - Erhaltene Rabatte"
    
    # Bezugsnebenkosten
    elif 3800 <= num <= 3850:
        return "Aufwendungen für Roh-, Hilfs- und Betriebsstoffe und für bezogene Waren - Bezugsnebenkosten"
    
    # Bestandsveränderungen
    elif 3950 <= num <= 3969:
        return "Bestandsveränderungen"
    
    # Bestand an Vorräten
    elif 3970 <= num <= 3989:
        return "Bestand an Vorräten"
    
    # Verrechnete Stoffkosten
    elif 3990 <= num <= 3999:
        return "Verrechnete Stoffkosten - Aufwendungen für Roh-, Hilfs- und Betriebsstoffe und für bezogene Waren"
    
    # === KLASSE 4: BETRIEBLICHE AUFWENDUNGEN ===
    
    # Material- und Stoffverbrauch
    elif 4000 <= num <= 4099:
        return "Material- und Stoffverbrauch - Aufwendungen für Roh-, Hilfs- und Betriebsstoffe und für bezogene Waren"
    
    # Löhne und Gehälter
    elif 4100 <= num <= 4129:
        return "Löhne und Gehälter"
    
    # Soziale Abgaben
    elif 4130 <= num <= 4199:
        return "Soziale Abgaben und Aufwendungen für Altersversorgung und für Unterstützung"
    elif num == 4139:
        return "Sonstige betriebliche Aufwendungen - Ausgleichsabgabe Schwerbehindertengesetz"
    elif 4145 <= num <= 4159:
        return "Löhne und Gehälter"
    elif 4160 <= num <= 4199:
        return "Soziale Abgaben und Aufwendungen für Altersversorgung und für Unterstützung"
    
    # Raumkosten
    elif 4200 <= num <= 4299:
        return "Sonstige betriebliche Aufwendungen - Raumkosten"
    
    # Steuern und Versicherungen
    elif 4300 <= num <= 4306:
        return "Nicht abziehbare Vorsteuer"
    elif num == 4320:
        return "Steuern vom Einkommen und Ertrag - Gewerbesteuer"
    elif 4340 <= num <= 4397:
        return "Sonstige Steuern / Sonstige betriebliche Aufwendungen"
    
    # Fahrzeugkosten
    elif 4500 <= num <= 4509:
        return "Sonstige betriebliche Aufwendungen - Fahrzeugkosten"
    elif num == 4510:
        return "Sonstige Steuern - Kfz-Steuer"
    elif 4520 <= num <= 4595:
        return "Sonstige betriebliche Aufwendungen - Fahrzeugkosten"
    
    # Werbekosten
    elif 4600 <= num <= 4689:
        return "Sonstige betriebliche Aufwendungen - Werbekosten / Geschenke / Bewirtungskosten / Reisekosten"
    
    # Kosten der Warenabgabe
    elif 4700 <= num <= 4799:
        return "Sonstige betriebliche Aufwendungen - Kosten der Warenabgabe"
    
    # Reparaturen
    elif 4800 <= num <= 4815:
        return "Sonstige betriebliche Aufwendungen - Reparaturen und Instandhaltungen"
    
    # Abschreibungen
    elif 4822 <= num <= 4865:
        return "Abschreibungen auf immaterielle Vermögensgegenstände des Anlagevermögens und Sachanlagen"
    elif 4866 <= num <= 4893:
        return "Abschreibungen auf Finanzanlagen und auf Wertpapiere des Umlaufvermögens"
    elif 4880 <= num <= 4887:
        return "Abschreibungen auf Vermögensgegenstände des Umlaufvermögens, soweit diese die in der Kapitalgesellschaft üblichen Abschreibungen überschreiten"
    elif 4892 <= num <= 4893:
        return "Abschreibungen auf Vermögensgegenstände des Umlaufvermögens, soweit diese die in der Kapitalgesellschaft üblichen Abschreibungen überschreiten"
    
    # Sonstige betriebliche Aufwendungen
    elif 4900 <= num <= 4985:
        return "Sonstige betriebliche Aufwendungen"
    
    # Kalkulatorische Kosten
    elif 4990 <= num <= 4995:
        return "Kalkulatorische Kosten - Sonstige betriebliche Aufwendungen"
    
    # Kosten Umsatzkostenverfahren
    elif 4996 <= num <= 4999:
        return "Kosten bei Anwendung des Umsatzkostenverfahrens - Sonstige betriebliche Aufwendungen"
    
    # === KLASSE 5-6: SONSTIGE BETRIEBLICHE AUFWENDUNGEN ===
    elif 5000 <= num <= 6999:
        return "Sonstige betriebliche Aufwendungen"
    
    # === KLASSE 7: BESTÄNDE AN ERZEUGNISSEN ===
    
    elif 7000 <= num <= 7089:
        return "Unfertige Erzeugnisse, unfertige Leistungen"
    elif num == 7090:
        return "In Ausführung befindliche Bauaufträge"
    elif num == 7095:
        return "In Arbeit befindliche Aufträge"
    elif 7100 <= num <= 7999:
        return "Fertige Erzeugnisse und Waren"
    
    # === KLASSE 8: ERLÖSKONTEN ===
    
    # Umsatzerlöse - Steuerfreie Umsätze
    elif 8000 <= num <= 8099:
        return "Umsatzerlöse"
    elif 8100 <= num <= 8165:
        return "Umsatzerlöse - Steuerfreie Umsätze"
    elif 8190 <= num <= 8198:
        return "Umsatzerlöse - Durchschnittssätze § 24 UStG / Kleinunternehmer"
    
    # Umsatzerlöse - Steuerpflichtige Erlöse
    elif num == 8200:
        return "Umsatzerlöse - Erlöse"
    elif num == 8290:
        return "Umsatzerlöse - Erlöse 0% USt"
    elif 8300 <= num <= 8339:
        return "Umsatzerlöse - Erlöse 7% / 19% USt / EU-Lieferungen"
    elif 8340 <= num <= 8499:
        return "Umsatzerlöse - Erlöse 16% / 19% USt"
    
    # Sonderbetriebseinnahmen
    elif 8500 <= num <= 8505:
        return "Sonderbetriebseinnahmen"
    elif 8510 <= num <= 8579:
        return "Umsatzerlöse - Provisionsumsätze / Sonstige Erträge"
    
    # Statistische Konten EÜR
    elif 8580 <= num <= 8589:
        return "Statistische Konten EÜR"
    
    # Sonstige betriebliche Erträge
    elif 8590 <= num <= 8614:
        return "Sonstige betriebliche Erträge - Verrechnete Sachbezüge"
    elif 8625 <= num <= 8649:
        return "Sonstige betriebliche Erträge"
    
    # Zinserträge
    elif 8650 <= num <= 8660:
        return "Sonstige Zinsen und ähnliche Erträge - Erlöse Zinsen und Diskontspesen"
    
    # Erlösschmälerungen
    elif 8700 <= num <= 8799:
        return "Umsatzerlöse - Erlösschmälerungen / Gewährte Skonti / Gewährte Boni / Gewährte Rabatte"
    
    # Erlöse aus Anlagenverkäufen
    elif 8800 <= num <= 8853:
        return "Sonstige betriebliche Aufwendungen / Sonstige betriebliche Erträge - Erlöse aus Verkäufen Anlagevermögen"
    
    # Unentgeltliche Wertabgaben
    elif 8900 <= num <= 8949:
        return "Sonstige betriebliche Erträge - Unentgeltliche Wertabgaben"
    elif 8950 <= num <= 8959:
        return "Umsatzerlöse - Nicht steuerbare Umsätze / Umsatzsteuervergütungen"
    
    # Bestandsveränderungen
    elif 8960 <= num <= 8980:
        return "Erhöhung des Bestands an fertigen und unfertigen Erzeugnissen oder Verminderung des Bestands"
    
    # Andere aktivierte Eigenleistungen
    elif 8990 <= num <= 8995:
        return "Andere aktivierte Eigenleistungen"
    
    # === KLASSE 9: VORTRAGS-, KAPITAL-, KORREKTUR- UND STATISTISCHE KONTEN ===
    
    # Vortragskonten
    elif 9000 <= num <= 9099:
        return "Vortragskonten"
    
    # Statistische Konten BWA
    elif 9101 <= num <= 9145:
        return "Statistische Konten für Betriebswirtschaftliche Auswertungen (BWA)"
    
    # Kapitalkontenanpassungen
    elif 9146 <= num <= 9189:
        return "Kapitaländerungen / Andere Kapitalkontenanpassungen / Umbuchungen / Anrechenbare Privatsteuern"
    
    # Gegenkonten
    elif 9190 <= num <= 9199:
        return "Gegenkonten zu statistischen Konten für Betriebswirtschaftliche Auswertungen"
    
    # Statistische Konten Bilanz
    elif 9200 <= num <= 9229:
        return "Statistische Konten für die Kennzahlen der Bilanz"
    
    # Kapitalflussrechnung
    elif 9240 <= num <= 9259:
        return "Statistische Konten für die Kapitalflussrechnung"
    
    # Rückstellungen
    elif 9260 <= num <= 9269:
        return "Aufgliederung der Rückstellungen für die Programme der Wirtschaftsberatung"
    
    # Haftungsverhältnisse
    elif 9270 <= num <= 9279:
        return "Statistische Konten für in der Bilanz auszuweisende Haftungsverhältnisse"
    
    # Sonstige finanzielle Verpflichtungen
    elif 9280 <= num <= 9289:
        return "Statistische Konten für die im Anhang anzugebenden sonstigen finanziellen Verpflichtungen"
    elif 9285 <= num <= 9286:
        return "Unterschiedsbetrag aus der Abzinsung von Altersversorgungsverpflichtungen nach § 253 Abs. 6 HGB"
    elif 9287 <= num <= 9293:
        return "Statistische Konten für § 4 Abs. 3 EStG"
    
    # Einlagen stiller Gesellschafter
    elif num == 9295:
        return "Einlagen stiller Gesellschafter"
    elif 9297 <= num <= 9299:
        return "Steuerlicher Ausgleichsposten"
    
    # Privat Teilhafter
    elif 9400 <= num <= 9499:
        return "Privat Teilhafter (Eigenkapital, für Verrechnung mit Kapitalkonto III)"
    
    # Statistische Konten Kapitalkontenentwicklung
    elif 9500 <= num <= 9799:
        return "Statistische Konten für die Kapitalkontenentwicklung"
    
    # Rücklagen
    elif 9802 <= num <= 9809:
        return "Rücklagen, Gewinn-, Verlustvortrag / Statistische Anteile"
    
    # Kapital Personenhandelsgesellschaft
    elif 9810 <= num <= 9899:
        return "Kapital Personenhandelsgesellschaft / Einzahlungsverpflichtungen / Ausgleichsposten / Steueraufwand"
    
    # Statistische Konten
    elif 9900 <= num <= 9999:
        return "Statistische Konten (Investitionsabzugsbetrag / Zinsschranke / Bewertungskorrekturen / Außergewöhnliche Geschäftsvorfälle)"
    
    else:
        return "N/A"
    
    

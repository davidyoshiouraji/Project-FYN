import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Set
import warnings
warnings.filterwarnings('ignore')

class FDDAccountMapper:
    """
    Automatisiert das Mapping von Kundenkontendaten auf standardisierte Bilanzpositionen
    für Financial Due Diligence Prozesse basierend auf DATEV SKR03.
    """
    
    def __init__(self, customer_file: str, mapping_file: str):
        """
        Initialisiert den Mapper mit Kunden- und Mapping-Dateien.
        
        Args:
            customer_file: Pfad zur Kundendatei (Excel)
            mapping_file: Pfad zur SKR03-Mapping-Datei (Excel)
        """
        self.customer_file = customer_file
        self.mapping_file = mapping_file
        self.customer_data = None
        self.mapping_dict = None
        self.unmapped_accounts = set()
        
    def load_customer_data(self) -> pd.DataFrame:
        """
        Lädt Kundendaten mit bekannter Struktur aus Screenshot.
        
        Returns:
            DataFrame mit Kundenkontendaten
        """
        print("📊 Lade Kundendaten...")
        
        # Optimiert für die bekannte Struktur: Account Number | Account Name | Monthly Data...
        self.customer_data = pd.read_excel(
            self.customer_file,
            engine='openpyxl',
            header=0,  # Erste Zeile als Header
            dtype={'Account Number': str}  # Kontonummer als String
        )
        
        # Saubere Kontonummern (Leerzeichen entfernen, NaN behandeln)
        if 'Account Number' in self.customer_data.columns:
            self.customer_data['Account Number'] = (
                self.customer_data['Account Number']
                .astype(str)
                .str.strip()
                .replace('nan', '')
            )
            
            # Leere Kontonummern entfernen
            self.customer_data = self.customer_data[
                self.customer_data['Account Number'] != ''
            ]
        
        print(f"✓ {len(self.customer_data)} Kundendatensätze geladen")
        print(f"📅 Verfügbare Spalten: {list(self.customer_data.columns)}")
        return self.customer_data
    
    def load_mapping_data(self) -> Dict[str, Tuple[str, str]]:
        """
        Lädt Mapping-Daten mit vereinfachter Level-Logik.
        
        Level 1: Spalte E (Bilanz_Seite) oder F, falls nicht N/A
        Level 2: Spalte C (Bilanzposition)
        
        Returns:
            Dictionary: {Kontonummer: (Level1, Level2)}
        """
        print("🗺️  Lade DATEV SKR03 Mapping...")
        
        # Alle Spalten als String laden für konsistentes Handling
        mapping_df = pd.read_excel(
            self.mapping_file,
            engine='openpyxl',
            header=0,
            dtype=str
        )
        
        print(f"📋 Mapping-Spalten: {list(mapping_df.columns)}")
        
        # Performance-optimierter Dictionary-Lookup
        self.mapping_dict = {}
        
        for _, row in mapping_df.iterrows():
            # Robuste Kontonummer-Behandlung
            account_num = str(row['Kontonummer']).strip()
            
            # Mehrere Varianten für besseres Matching speichern
            account_variations = [
                account_num,  # Original
                account_num.lstrip('0') if account_num.lstrip('0') else account_num,  # Ohne führende Nullen
            ]
            
            # Level 2: Spalte C (Bilanzposition)
            level2 = str(row.get('Bilanzposition', 'Unbekannt')).strip()
            if level2 in ['nan', 'N/A', '']:
                level2 = 'Unbekannt'
            
            # Level 1 Logik: Erst GuV_Position (Spalte D), dann Bilanz_Seite (Spalte E)
            guv_position = str(row.get('GuV_Position', 'N/A')).strip()
            bilanz_seite = str(row.get('Bilanz_Seite', 'N/A')).strip()
            
            # Priorität: 1. GuV_Position, 2. Bilanz_Seite, 3. Unbekannt
            if guv_position not in ['N/A', 'nan', '', 'Unbekannt']:
                level1 = guv_position
            elif bilanz_seite not in ['N/A', 'nan', '', 'Unbekannt']:
                level1 = bilanz_seite
            else:
                level1 = 'Unbekannt'
            
            # Alle Varianten der Kontonummer im Dictionary speichern
            for variation in account_variations:
                if variation:  # Nur nicht-leere Varianten
                    self.mapping_dict[variation] = (level1, level2)
        
        print(f"✓ {len(self.mapping_dict)} Mapping-Einträge erstellt")
        
        # Debug: Zeige ein paar Beispiele
        print("🔍 Mapping-Beispiele:")
        for i, (k, v) in enumerate(list(self.mapping_dict.items())[:3]):
            print(f"   {k} → Level1: '{v[0]}', Level2: '{v[1]}'")
        
        return self.mapping_dict
    
    def apply_mapping(self) -> pd.DataFrame:
        """
        Wendet vereinfachtes Mapping basierend auf Kontonummer an.
        
        Returns:
            DataFrame mit Level1/Level2 zwischen Account Name und Jahresspalten eingefügt
        """
        print("🔄 Wende vereinfachtes DATEV-Mapping an...")
        
        if self.customer_data is None or self.mapping_dict is None:
            raise ValueError("Daten müssen zuerst geladen werden")
        
        result_df = self.customer_data.copy()
        
        # Vereinfachte Mapping-Funktion
        def map_account(account_num: str) -> Tuple[str, str]:
            """Mappt Kontonummer direkt über Dictionary-Lookup."""
            # Bereinigung der Input-Kontonummer
            clean_account = str(account_num).strip()
            
            # Direktes Lookup - Dictionary enthält bereits alle Varianten
            if clean_account in self.mapping_dict:
                return self.mapping_dict[clean_account]
            
            # Zusätzlicher Versuch ohne führende Nullen
            clean_no_zeros = clean_account.lstrip('0')
            if clean_no_zeros and clean_no_zeros in self.mapping_dict:
                return self.mapping_dict[clean_no_zeros]
            
            # Nicht gefunden
            print(f"🔍 Konto nicht gefunden: '{account_num}'")
            self.unmapped_accounts.add(account_num)
            return ('Unbekannt', 'Unbekannt')
        
        # Vektorisierte Anwendung des Mappings
        mapping_results = result_df['Account Number'].apply(map_account)
        
        # Level-Spalten extrahieren
        result_df['Level1'] = [result[0] for result in mapping_results]
        result_df['Level2'] = [result[1] for result in mapping_results]
        
        # Spalten-Reihenfolge: Account Number | Account Name | Level1 | Level2 | Jahresspalten (original Reihenfolge)
        base_cols = ['Account Number', 'Account Name', 'Level1', 'Level2']
        
        # Jahresspalten in ursprünglicher Reihenfolge beibehalten (keine Sortierung!)
        year_cols = [col for col in result_df.columns if col not in base_cols]
        
        # Finale Spalten-Anordnung
        result_df = result_df[base_cols + year_cols]
        
        print(f"✓ Mapping abgeschlossen")
        print(f"📊 {len(result_df) - len(self.unmapped_accounts)} erfolgreich gemappt")
        print(f"⚠️  {len(self.unmapped_accounts)} nicht gemappte Konten")
        
        return result_df
    
    def print_unmapped_accounts(self) -> None:
        """Detaillierte Ausgabe unmappbarer Konten für manuelle Nachbearbeitung."""
        if self.unmapped_accounts:
            print(f"\n⚠️  {len(self.unmapped_accounts)} UNMAPPBARE KONTEN:")
            print("=" * 80)
            print(f"{'Kontonummer':<15} {'Kontoname':<50} {'Grund':<15}")
            print("-" * 80)
            
            for account in sorted(self.unmapped_accounts):
                account_name = "Name nicht verfügbar"
                if self.customer_data is not None:
                    mask = self.customer_data['Account Number'] == account
                    if mask.any():
                        account_name = str(self.customer_data.loc[mask, 'Account Name'].iloc[0])[:47]
                
                # Grund für fehlende Zuordnung analysieren
                reason = "Nicht im Mapping"
                if account == '' or account == 'nan':
                    reason = "Leere Nummer"
                
                print(f"{account:<15} {account_name:<50} {reason:<15}")
                
            print("\n💡 Tipp: Prüfen Sie diese Konten manuell oder erweitern Sie das Mapping")
        else:
            print("✅ Perfekt! Alle Konten erfolgreich gemappt!")
    
    def generate_mapping_stats(self, mapped_df: pd.DataFrame) -> Dict[str, any]:
        """
        Generiert detaillierte Statistiken für FDD-Report.
        
        Args:
            mapped_df: Gemappte Daten
            
        Returns:
            Dictionary mit Mapping-Statistiken
        """
        total_accounts = len(mapped_df)
        mapped_accounts = total_accounts - len(self.unmapped_accounts)
        
        # Level1-Verteilung
        level1_dist = mapped_df['Level1'].value_counts().to_dict()
        
        # Bilanz vs. GuV Klassifikation
        bilanz_accounts = len(mapped_df[mapped_df['Level1'] != 'GuV-Position'])
        guv_accounts = len(mapped_df[mapped_df['Level1'] == 'GuV-Position'])
        
        # Identifizierung von Jahresspalten (ursprüngliche Reihenfolge beibehalten)
        year_cols = [col for col in mapped_df.columns if col not in 
                    ['Account Number', 'Account Name', 'Level1', 'Level2']]
        
        data_completeness = {}
        for col in year_cols:
            non_zero = (mapped_df[col] != 0).sum() if col in mapped_df.columns else 0
            data_completeness[col] = f"{non_zero}/{total_accounts} ({non_zero/total_accounts*100:.1f}%)"
        
        return {
            'total_accounts': total_accounts,
            'mapped_accounts': mapped_accounts,
            'unmapped_accounts': len(self.unmapped_accounts),
            'mapping_success_rate': round(mapped_accounts / total_accounts * 100, 2),
            'level1_distribution': level1_dist,
            'bilanz_accounts': bilanz_accounts,
            'guv_accounts': guv_accounts,
            'data_completeness': data_completeness
        }
    
    def export_to_excel(self, mapped_df: pd.DataFrame, output_file: str = "fdd_mapped_results.xlsx") -> None:
        """
        Exportiert FDD-optimierte Excel-Ausgabe mit mehreren Analysesheets.
        
        Args:
            mapped_df: Gemappte Daten
            output_file: Output-Dateiname
        """
        print(f"💾 Exportiere FDD-Analyse nach {output_file}...")
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            
            # 1. Haupt-Mapping Ergebnisse
            mapped_df.to_excel(writer, sheet_name='Mapped_Accounts', index=False)
            
            # 2. Executive Summary für FDD-Team
            stats = self.generate_mapping_stats(mapped_df)
            
            summary_data = {
                'KPI': [
                    'Gesamtanzahl Konten',
                    'Erfolgreich gemappt',
                    'Nicht gemappt', 
                    'Mapping-Erfolgsquote (%)',
                    'Bilanzkonten',
                    'GuV-Konten',
                    'Nicht klassifiziert'
                ],
                'Wert': [
                    stats['total_accounts'],
                    stats['mapped_accounts'],
                    stats['unmapped_accounts'],
                    stats['mapping_success_rate'],
                    stats['bilanz_accounts'],
                    stats['guv_accounts'],
                    stats['total_accounts'] - stats['bilanz_accounts'] - stats['guv_accounts']
                ],
                'Status': [
                    '✓', '✓', '⚠️' if stats['unmapped_accounts'] > 0 else '✓',
                    '✓' if stats['mapping_success_rate'] >= 95 else '⚠️',
                    '✓', '✓', '⚠️' if stats['total_accounts'] - stats['bilanz_accounts'] - stats['guv_accounts'] > 0 else '✓'
                ]
            }
            
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Executive_Summary', index=False)
            
            # 3. Level1-Kategorien für FDD-Struktur
            level1_breakdown = mapped_df['Level1'].value_counts().reset_index()
            level1_breakdown.columns = ['Kategorie', 'Anzahl_Konten']
            level1_breakdown['Prozent'] = round(level1_breakdown['Anzahl_Konten'] / len(mapped_df) * 100, 1)
            level1_breakdown.to_excel(writer, sheet_name='Kategorien_Breakdown', index=False)
            
            # 4. Unmapped Accounts mit Details
            if self.unmapped_accounts:
                unmapped_details = []
                for account in sorted(self.unmapped_accounts):
                    account_name = "Unbekannt"
                    if self.customer_data is not None:
                        mask = self.customer_data['Account Number'] == account
                        if mask.any():
                            account_name = self.customer_data.loc[mask, 'Account Name'].iloc[0]
                    
                    unmapped_details.append({
                        'Account_Number': account,
                        'Account_Name': account_name,
                        'Empfehlung': 'Manuell in Mapping-Tabelle ergänzen'
                    })
                
                unmapped_df = pd.DataFrame(unmapped_details)
                unmapped_df.to_excel(writer, sheet_name='Unmapped_Accounts', index=False)
            
            # 5. Datenqualitäts-Check für Jahreswerte  
            year_cols = [col for col in mapped_df.columns if col not in 
                        ['Account Number', 'Account Name', 'Level1', 'Level2']]
            
            if year_cols:
                quality_data = []
                for col in year_cols:
                    non_zero = (mapped_df[col] != 0).sum()
                    zero_values = (mapped_df[col] == 0).sum()
                    null_values = mapped_df[col].isna().sum()
                    
                    quality_data.append({
                        'Periode': col,
                        'Konten_mit_Daten': non_zero,
                        'Null_Werte': zero_values,
                        'Fehlende_Werte': null_values,
                        'Datenqualität_%': round(non_zero / len(mapped_df) * 100, 1)
                    })
                
                quality_df = pd.DataFrame(quality_data)
                quality_df.to_excel(writer, sheet_name='Datenqualitaet', index=False)
        
        print(f"✅ FDD-Excel erfolgreich exportiert: {output_file}")
        print(f"📁 Sheets: Mapped_Accounts, Executive_Summary, Kategorien_Breakdown, Unmapped_Accounts, Datenqualitaet")

def run_fdd_mapping(customer_file: str, mapping_file: str, output_file: str = "fdd_mapping_results.xlsx") -> pd.DataFrame:
    """
    Hauptfunktion für automatisierte FDD Account Mapping.
    
    Args:
        customer_file: Pfad zur Kundendatei  
        mapping_file: Pfad zur DATEV SKR03 Mapping-Datei
        output_file: Pfad für Excel-Output
        
    Returns:
        DataFrame mit FDD-ready gemappten Daten
    """
    print("🚀 FDD ACCOUNT MAPPING AUTOMATISIERUNG")
    print("=" * 60)
    print("🎯 Ziel: Automatisierung der Financial Due Diligence")
    print("📋 Mapping: DATEV SKR03 → Standardisierte Bilanzpositionen")
    print("-" * 60)
    
    # Mapper initialisieren und ausführen
    mapper = FDDAccountMapper(customer_file, mapping_file)
    
    # Workflow ausführen
    mapper.load_customer_data()
    mapper.load_mapping_data() 
    mapped_data = mapper.apply_mapping()
    
    # Qualitätskontrolle
    mapper.print_unmapped_accounts()
    
    # FDD-Excel generieren
    mapper.export_to_excel(mapped_data, output_file)
    
    # Erfolgs-Summary
    stats = mapper.generate_mapping_stats(mapped_data)
    
    print(f"\n🎉 FDD MAPPING ERFOLGREICH ABGESCHLOSSEN!")
    print("=" * 60)
    print(f"📊 Verarbeitete Konten: {stats['total_accounts']}")
    print(f"✅ Erfolgreich gemappt: {stats['mapped_accounts']}")
    print(f"📈 Erfolgsquote: {stats['mapping_success_rate']}%")
    print(f"🏦 Bilanzkonten: {stats['bilanz_accounts']}")
    print(f"📊 GuV-Konten: {stats['guv_accounts']}")
    
    if stats['mapping_success_rate'] >= 95:
        print("🌟 Exzellente Mapping-Qualität! Ready für FDD-Analyse.")
    elif stats['mapping_success_rate'] >= 90:
        print("✅ Gute Mapping-Qualität. Geringe manuelle Nacharbeit erforderlich.")
    else:
        print("⚠️  Mapping-Qualität verbesserungswürdig. Prüfen Sie unmapped accounts.")
    
    return mapped_data

# Verwendungsbeispiel:
if __name__ == "__main__":
    # Ihre Dateipfade
    customer_file = "../../data/raw/excel/synthetic_test_data_part_01.xlsx"
    mapping_file = "../../data/raw/excel/datev_skr03_account_mapping.xlsx"
    
    # FDD Mapping ausführen
    result = run_fdd_mapping(customer_file, mapping_file, "../../data/raw/excel/fdd_lead_sheet.xlsx")
    
    # Quick Preview für Validation
    print("\n📋 VORSCHAU - Erste 3 gemappte Datensätze:")
    print("-" * 100)
    preview_cols = ['Account Number', 'Account Name', 'Level1', 'Level2']
    available_cols = [col for col in preview_cols if col in result.columns]
    print(result[available_cols].head(3).to_string(index=False))
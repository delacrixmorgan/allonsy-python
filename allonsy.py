import os
import urllib.request
import csv
import tempfile

def download_google_sheet_csv(spreadsheet_id, sheet_name):
    """
    Download the Google Sheet as a CSV file.

    :param spreadsheet_id: Google Sheet ID
    :param sheet_name: The sheet name to download (e.g., 'Sheet1')
    :return: Path to the downloaded CSV file
    """
    csv_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')

    try:
        print(f"📥 Downloading the Google Sheet as CSV...")
        urllib.request.urlretrieve(csv_url, temp_file.name)
        print(f"✅ Successfully downloaded CSV: {temp_file.name}")
        return temp_file.name
    except Exception as e:
        print(f"🔥 Error occurred while downloading the CSV: {e}")
        raise

import re

def needs_formatted_false(text):
    """
    Determines if formatted="false" is needed in Android strings.xml.

    :param text: The text string to check
    :return: True if formatted="false" is needed, False otherwise
    """
    contains_braces = "{" in text or "}" in text  # Check for placeholders like {name}
    contains_android_formatting = bool(re.search(r"%\d*\$?[sd]", text))  # Matches %s, %1$s, %2$d, etc.

    return contains_braces and not contains_android_formatting  # Only add formatted="false" if {} is present

def export_translations(spreadsheet_id, sheet_name, export_dir, platform='android'):
    """
    Export translations from a Google Sheet to platform-specific localization files.

    :param spreadsheet_id: Google Sheet ID
    :param sheet_name: The sheet name to export from (e.g., 'Sheet1')
    :param export_dir: Directory where the localization files will be saved
    :param platform: The platform ('android' or 'ios'). Default is 'android'.
    """
    csv_file_path = download_google_sheet_csv(spreadsheet_id, sheet_name)

    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)

    headers = data[0]
    lang_columns = [col for col in headers[4:] if col.strip()]  # Skip blank language columns

    os.makedirs(export_dir, exist_ok=True)

    # Base Text Export (Android / iOS)
    if platform == 'android':
        base_xml_content = ['<?xml version="1.0" encoding="utf-8"?>', '<resources>']
        for row in data[1:]:
            if row[0].startswith("//"):  # Skip commented-out rows
                continue
            key, base_text = row[2], row[3]
            formatted_attr = ' formatted="false"' if needs_formatted_false(base_text) else ""
            base_xml_content.append(f'    <string name="{key}"{formatted_attr}>{base_text}</string>')
        base_xml_content.append("</resources>")

        base_xml_file = os.path.join(export_dir, "values", "strings.xml")
        os.makedirs(os.path.dirname(base_xml_file), exist_ok=True)
        with open(base_xml_file, "w", encoding="utf-8") as f:
            f.write("\n".join(base_xml_content))
        print(f"✅ Exported Base Text to: {base_xml_file}")

    elif platform == 'ios':
        base_str_content = []
        for row in data[1:]:
            if row[0].startswith("//"):  # Skip commented-out rows
                continue
            key, base_text = row[2], row[3]
            base_str_content.append(f'"{key}" = "{base_text}";')

        base_str_file = os.path.join(export_dir, "Base.lproj", "Localizable.strings")
        os.makedirs(os.path.dirname(base_str_file), exist_ok=True)
        with open(base_str_file, "w", encoding="utf-8") as f:
            f.write("\n".join(base_str_content))
        print(f"✅ Exported Base Text to: {base_str_file}")

    for lang in lang_columns:
        lang_index = headers.index(lang)

        if platform == 'android':
            lang_dir = os.path.join(export_dir, f"values-{lang}")
            os.makedirs(lang_dir, exist_ok=True)

            xml_content = ['<?xml version="1.0" encoding="utf-8"?>', '<resources>']
            for row in data[1:]:
                if row[0].startswith("//"):  # Skip commented-out rows
                    continue
                key, translation = row[2], row[lang_index]
                if not translation.strip():  # Skip blank translations
                    continue
                formatted_attr = ' formatted="false"' if needs_formatted_false(translation) else ""
                xml_content.append(f'    <string name="{key}"{formatted_attr}>{translation}</string>')
            xml_content.append("</resources>")

            xml_file = os.path.join(lang_dir, "strings.xml")
            with open(xml_file, "w", encoding="utf-8") as f:
                f.write("\n".join(xml_content))
            print(f"✅ Exported: {xml_file}")

        elif platform == 'ios':
            lang_dir = os.path.join(export_dir, f"{lang}.lproj")
            os.makedirs(lang_dir, exist_ok=True)

            str_content = []
            for row in data[1:]:
                if row[0].startswith("//"):  # Skip commented-out rows
                    continue
                key, translation = row[2], row[lang_index]
                if not translation.strip():  # Skip blank translations
                    continue
                str_content.append(f'"{key}" = "{translation}";')

            str_file = os.path.join(lang_dir, "Localizable.strings")
            with open(str_file, "w", encoding="utf-8") as f:
                f.write("\n".join(str_content))
            print(f"✅ Exported: {str_file}")

    print(f"🎉 All translations exported successfully for {platform}!")

    # After successful export, delete the CSV file
    os.remove(csv_file_path)

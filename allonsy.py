import os
import urllib.request
import csv
import tempfile
import re

def download_google_sheet_csv(spreadsheet_id, sheet_name):
    """
    Download the Google Sheet as a CSV file.

    :param spreadsheet_id: Google Sheet ID
    :param sheet_name: The sheet name to download (e.g., 'Sheet1')
    :return: Path to the downloaded CSV file
    """
    # Validate the spreadsheet_id
    if spreadsheet_id == "YOUR_SPREADSHEET_ID":
        raise ValueError("❌ Error: Please replace 'YOUR_SPREADSHEET_ID' with your actual Google Sheet ID.")

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

def needs_formatted_false(text):
    """
    Determines if formatted="false" is needed in Android strings.xml.

    :param text: The text string to check
    :return: True if formatted="false" is needed, False otherwise
    """
    contains_braces = "{" in text or "}" in text  # Check for placeholders like {name}
    contains_android_formatting = bool(re.search(r"%\d*\$?[sd]", text))  # Matches %s, %1$s, %2$d, etc.

    return contains_braces and not contains_android_formatting  # Only add formatted="false" if {} is present

def escape_android_string(text):
    """
    Escape special characters for Android XML strings using Android-specific escaping.

    :param text: The text string to escape
    :return: Escaped string for Android XML
    """
    if text is None:
        return ""

    # Escape special XML characters manually
    escaped = text.replace('&', '&amp;')
    escaped = escaped.replace('<', '&lt;')
    escaped = escaped.replace('>', '&gt;')

    # Handle specific Android XML escape sequences
    # Note: @ and ? at the beginning of a string need to be escaped
    if escaped.startswith('@'):
        escaped = '\\@' + escaped[1:]
    if escaped.startswith('?'):
        escaped = '\\?' + escaped[1:]

    # Escape apostrophes with backslash (Android-specific)
    escaped = escaped.replace("'", "\\'")

    # Replace newlines with the appropriate escape sequence
    escaped = escaped.replace('\n', '\\n')

    # Escape double quotes
    escaped = escaped.replace('"', '\\"')

    return escaped

def escape_ios_string(text):
    """
    Escape special characters for iOS Localizable.strings files.

    :param text: The text string to escape
    :return: Escaped string for iOS
    """
    if text is None:
        return ""

    # Escape backslashes first (to avoid double-escaping)
    escaped = text.replace('\\', '\\\\')

    # Escape double quotes (required for .strings files)
    escaped = escaped.replace('"', '\\"')

    # Escape control characters
    escaped = escaped.replace('\n', '\\n')
    escaped = escaped.replace('\r', '\\r')
    escaped = escaped.replace('\t', '\\t')

    # Handle Unicode characters that need escaping
    # This is a simplified approach - more comprehensive Unicode handling may be needed
    def replace_unicode(match):
        return f"\\u{ord(match.group(0)):04x}"

    # Replace non-ASCII characters with Unicode escapes
    escaped = re.sub(r'[^\x00-\x7F]', replace_unicode, escaped)

    return escaped

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

            # Escape the Android string
            escaped_text = escape_android_string(base_text)

            formatted_attr = ' formatted="false"' if needs_formatted_false(base_text) else ""
            base_xml_content.append(f'    <string name="{key}"{formatted_attr}>{escaped_text}</string>')
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
            # For iOS, use the iOS-specific escaping function
            escaped_text = escape_ios_string(base_text)
            base_str_content.append(f'"{key}" = "{escaped_text}";')

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

                # Escape the Android string
                escaped_translation = escape_android_string(translation)

                formatted_attr = ' formatted="false"' if needs_formatted_false(translation) else ""
                xml_content.append(f'    <string name="{key}"{formatted_attr}>{escaped_translation}</string>')
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
                # For iOS, use the iOS-specific escaping function
                escaped_translation = escape_ios_string(translation)
                str_content.append(f'"{key}" = "{escaped_translation}";')

            str_file = os.path.join(lang_dir, "Localizable.strings")
            with open(str_file, "w", encoding="utf-8") as f:
                f.write("\n".join(str_content))
            print(f"✅ Exported: {str_file}")

    print(f"🎉 All translations exported successfully for {platform}!")

    # After successful export, delete the CSV file
    os.remove(csv_file_path)
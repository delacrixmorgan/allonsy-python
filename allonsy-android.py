from allonsy import export_translations

spreadsheet_id = "YOUR_SPREADSHEET_ID"
sheet_name = "App"
export_dir = "app-android/src"
platform = "android"

export_translations(spreadsheet_id, sheet_name, export_dir, platform)

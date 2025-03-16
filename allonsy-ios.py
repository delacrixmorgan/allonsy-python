from allonsy import export_translations

spreadsheet_id = "YOUR_SPREADSHEET_ID"
sheet_name = "App"
export_dir = "app-ios/src"
platform = "ios"

export_translations(spreadsheet_id, sheet_name, export_dir, platform)

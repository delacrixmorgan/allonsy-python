# Allonsy - Google Sheet Strings Exporter ⚡

Welcome to **Allonsy!** A blazing-fast, works out of the box script that automatically downloads translations from
public **Google Sheets** and exports them into platform-specific localisation files for **Android** and **iOS.**

No more tedious copy-pasting or manual exports—just run Allonsy, and let it magic do its thing! 🔮
  
---  

## 🌟 What Can Allonsy Do?

- **Fetch Translations Automatically** 🏁
  Downloads a Google Sheet as a CSV file **without you lifting a finger.**
- **Generate Android and iOS Localization Files** 📱
  Converts the CSV data into proper **Android** and **iOS** formats.
- **Skip Blank Translations** 🚫
  Ignores empty translations so your localisation files stay clean.
- **Ignore Commented-Out Rows** 📝
  Detects rows that start with `//` and skips them.
- **Smart Formatting Detection** 🔍
    - If a string has `{}` placeholders → `formatted=false` is applied (for Android).
    - If a string has `%s, %d, %1$s` → kept as it is.

---  

## 🔧 How to Run Allonsy

### 💻 macOS & Windows (No Third-Party Libraries!)

Good news! You **don’t** need to install anything extra—Allonsy runs on pure Python 🐍

### **1️⃣ Clone the Repository**

```sh  
git clone https://github.com/delacrixmorgan/allonsy-python.git  
cd allonsy-python  
```  

### **2️⃣ Update your variables in the script**

For convenience, there are two Python files that store all the **necessary variables and configurations**:

- spreadsheet_id = The unique identifier of your Google Sheet.
- sheet_name = The name of the sheet you want to export.
- export_dir = The directory where the localisation files will be saved.
- platform = Choose between `android` or `ios`.

#### **Where to find your Spreadsheet ID?**

Your spreadsheet ID is the long string of characters in the URL of your Google Sheet:

```  
https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit#gid=0  
```  

Copy the `SPREADSHEET_ID` value and paste it into your script.

#### **What Google Sheet structure does the Allonsy supports?**

| Screen | Element | Key      | Base Text  | zh   | {ISO_639_LANGUAGE_CODE} |
|--------|---------|----------|------------|------|-------------------------|
| app    | name    | app_name | King's Cup | 国王之杯 | ?                       |

Here's a [Google Sheet sample](https://docs.google.com/spreadsheets/d/1vVQlcoCJCvoeEbQqoXjzaLtwIZJurjwKr65twRSFarA) on
how you **structure** your strings and its different locales. For the locale column, just use
the [ISO 639 Language Codes](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes?useskin=vector).

#### **Android `allonsy-android.py`**

```python  
from allonsy import export_translations  
  
spreadsheet_id = "YOUR_SPREADSHEET_ID"  
sheet_name = "YOUR_SHEET_NAME"  
export_dir = "app-android/src"  
platform = "android"  
  
export_translations(spreadsheet_id, sheet_name, export_dir, platform)  
```  

#### **iOS `allonsy-ios.py`**

```python  
from allonsy import export_translations  
  
spreadsheet_id = "YOUR_SPREADSHEET_ID"  
sheet_name = "YOUR_SHEET_NAME"  
export_dir = "app-ios/src"  
platform = "ios"  
  
export_translations(spreadsheet_id, sheet_name, export_dir, platform)  
```  

### **3️⃣ Run the Script**

It's that easy!

```sh  
python allonsy-android.py
python allonsy-ios.py  
```  

🎉 **Boom! Your string translations are now ready.**
  
---  

## ⚡ Scenarios Handled by Allonsy

🔹 **Scenario: Blank Language Column?** ✅ **Ignored!**

> If a language column is empty, Allonsy will **skip it**—no more clutter!

🔹 **Scenario: Commented-Out Rows? ✅ Ignored!**

> Any row starting with `//` is **ignored**, keeping your translations organized.

🔹 **Scenario: {} in Strings? ✅ formatted="false" added!**

> If a string contains `{}` placeholders (e.g., `Hello {name}`), Allonsy **adds **``** for Android.**

🔹 **Scenario: %d, %s, %1s in Strings?** ✅ Kept it!

> If a string uses Android-style placeholders like `%d`, `%s` or `%1s`, Allonsy **keeps formatting enabled.**

---  

## ⚠️ Limitation of Allonsy

For the Google Sheet to be downloaded through the script, you will need to make that spreadsheet to be set as **public
**.

Reason being, you will need more setup like creating a service in Google Cloud Console to get your own
`google-services.json`.

For Allonsy, the intention is to just **keep it simple**. It's even written to use the openly supported `.csv` file
format rather than the conventional Excel's `.xlsx`. So that you can just easily run out of the box, rather than
fiddling with installing 3rd party libraries and Google Cloud Console setup.
  
---  

## 💡 Why "Allonsy"? 🤔

Inspired by **Doctor Who**, "Allons-y" means "Let's go!" in French. This script is all about **speed, automation, and
making your life easier.**

🚀 **So, what are you waiting for? Let's go—Allons-y!** 🚀

![Allonsy](/gif/doctorwho-david-tennant.gif "Allonsy")
# 🧹 Windows Debloater & App Remover Tool



An interactive, lightweight Python command-line utility designed to clean up pre-installed Windows bloatware, telemetry tools, sponsored games, and background services on Windows 10 and Windows 11.

---
## 🛑 IMPORTANT

If you’re able to, please support me by [joining my patreon.](https://www.patreon.com/Modi393)

Your support will help me make more updates to Windows Debloater!

If you’re unable to, I hope you enjoy the program!

This is just a fun nonprofit lil project i made :P

---

## ✨ Features

- **Interactive Selection Menu:** Choose exactly which apps to remove—keep what you use, delete what you don't.
- **Range & Multi-Select:** Toggle items using individual numbers (`1 3 5`) or ranges (`1-5`).
- **Comprehensive Purge:** Removes both active AppX packages and provisioned offline installer packages across all user accounts.
- **Deep Clean Capabilities:**
  - Disables **Windows Copilot** via Registry policies.
  - Removes sponsored games (**Candy Crush**, **Royal Match**, **Disney** promos).
  - Uninstalls persistent background apps (**OneDrive**, **Teams**, **Phone Link**, **Widgets**).
  - Optionally disables **Windows Defender** real-time monitoring.

---

## 📋 Included Bloatware Definitions

| Category | Apps & Services Included |
| :--- | :--- |
| **Assistants & AI** | Cortana, Windows Copilot |
| **System Bloat** | Get Help, Windows Widgets & News Feed, Tips & Getting Started, Feedback Hub |
| **Communications** | Microsoft Teams (Consumer), Skype, Phone Link |
| **Games & Promo** | Candy Crush, Royal Match, Disney games, Solitaire Collection |
| **Utilities** | Clipchamp Video Editor, Paint 3D, 3D Builder/Viewer, Windows Maps, Mixed Reality Portal |
| **Background Sync & Defense** | Microsoft OneDrive, Windows Defender Real-Time Protection |

---

## ⚡ Prerequisites

- **Operating System:** Windows 10 or Windows 11
- **Python:** Python 3.6 or newer installed on system PATH
- **Privileges:** Administrator access (Command Prompt / PowerShell run as Administrator)

---

## 🚀 Usage Guide

1. **Clone or Download the Repository:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/windows-debloater.git
   cd windows-debloater
   ```

2. **Open Command Prompt / PowerShell as Administrator:**
   - Right-click **Command Prompt** or **PowerShell** and choose **Run as Administrator**.

3. **Run the Script:**
   ```cmd
   python debloat_windows.py
   ```

4. **Interact with the Menu:**
   - Type numbers to toggle items (e.g., `1 3 5` or `1-7`).
   - Enter `A` to select all items or `N` to clear selections.
   - Enter `R` to run the removal process.

---

## ⚠️ Important Notes & Disclaimers

### Disabling Windows Defender
If you intend to disable Windows Defender using this script, you **must disable Tamper Protection** first in Windows settings:
1. Open **Windows Security** $\rightarrow$ **Virus & threat protection**.
2. Click **Manage settings** under *Virus & threat protection settings*.
3. Turn **Tamper Protection** to **Off**.

### Reinstalling Default Windows Apps
If you ever want to restore all original built-in Windows applications, open PowerShell as Administrator and execute:

```powershell
Get-AppxPackage -AllUsers | Foreach {Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\AppXManifest.xml"}
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE). Free to use, modify, and distribute.

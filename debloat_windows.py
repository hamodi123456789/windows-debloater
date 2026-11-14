import os
import sys
import subprocess
import ctypes

# Full list of Windows bloatware definitions with expanded package wildcards
BLOATWARE_LIST = [
    {
        "id": "cortana",
        "name": "Cortana",
        "type": "appx",
        "packages": ["*549981C3F5F10*"],
        "desc": "Microsoft Cortana voice assistant."
    },
    {
        "id": "copilot",
        "name": "Windows Copilot",
        "type": "copilot",
        "packages": ["*Copilot*"],
        "desc": "Windows AI Copilot integration and taskbar button."
    },
    {
        "id": "get_help",
        "name": "Get Help App",
        "type": "appx",
        "packages": ["*GetHelp*"],
        "desc": "Windows Get Help app and automated support tools. (but no one cares because we all hate this app right?!!!!)"
    },
    {
        "id": "widgets",
        "name": "Windows Widgets & News Feed",
        "type": "appx",
        "packages": ["*WebExperience*"],
        "desc": "The taskbar news feed and MSN widget board hogging background RAM."
    },
    {
        "id": "sponsored_games",
        "name": "Candy Crush & Sponsored Games",
        "type": "appx",
        "packages": ["*CandyCrush*", "*RoyalMatch*", "*BubbleWitch*", "*King.com*", "*Disney*"],
        "desc": "Candy Crush, Royal Match, and random OEM promo games Windows installs silently."
    },
    {
        "id": "teams_personal",
        "name": "Microsoft Teams (Consumer)",
        "type": "appx",
        "packages": ["*MSTeams*"],
        "desc": "The annoying built-in personal version of Teams that auto-starts on boot."
    },
    {
        "id": "clipchamp",
        "name": "Clipchamp Video Editor",
        "type": "appx",
        "packages": ["*Clipchamp*"],
        "desc": "Microsoft's cloud video editor pushing monthly sub options."
    },
    {
        "id": "tips",
        "name": "Windows Tips & Getting Started",
        "type": "appx",
        "packages": ["*Getstarted*"],
        "desc": "Unwanted notification pop-ups explaining basic desktop features."
    },
    {
        "id": "mixed_reality",
        "name": "Mixed Reality Portal",
        "type": "appx",
        "packages": ["*MixedReality.Portal*"],
        "desc": "VR framework and hub that almost no standard PC user ever touches."
    },
    {
        "id": "skype",
        "name": "Skype",
        "type": "appx",
        "packages": ["*SkypeApp*"],
        "desc": "The legacy video calling app nobody uses anymore. (come on Microsoft why would you keep it in windows if it’s literally shut down like five years ago or something)"
    },
    {
        "id": "paint_3d",
        "name": "Paint 3D & 3D Viewer",
        "type": "appx",
        "packages": ["*Paint3D*", "*3DViewer*", "*3DBuilder*"],
        "desc": "Leftover 3D modeling utility bloat from older Windows updates."
    },
    {
        "id": "feedback",
        "name": "Feedback Hub",
        "type": "appx",
        "packages": ["*WindowsFeedbackHub*"],
        "desc": "Background feedback telemetry prompt app."
    },
    {
        "id": "maps",
        "name": "Windows Maps",
        "type": "appx",
        "packages": ["*WindowsMaps*"],
        "desc": "Built-in offline desktop maps app."
    },
    {
        "id": "your_phone",
        "name": "Phone Link (Your Phone)",
        "type": "appx",
        "packages": ["*YourPhone*", "*PhoneLink*"],
        "desc": "Windows Phone Link connection app and persistent background service."
    },
    {
        "id": "bing_apps",
        "name": "Bing News, Weather & Finance",
        "type": "appx",
        "packages": ["*bing*"],
        "desc": "MSN News, Weather, and Sports apps running background updates."
    },
    {
        "id": "solitaire",
        "name": "Microsoft Solitaire Collection",
        "type": "appx",
        "packages": ["*solitaire*"],
        "desc": "Ad-supported version of Solitaire."
    },
    {
        "id": "xbox",
        "name": "Xbox Apps & Game Bar",
        "type": "appx",
        "packages": ["*xbox*"],
        "desc": "Xbox Overlay, Game Bar shortcuts, and background streaming tools."
    },
    {
        "id": "onedrive",
        "name": "Microsoft OneDrive",
        "type": "onedrive",
        "packages": [],
        "desc": "Uninstalls OneDrive background file sync app."
    },
    {
        "id": "defender",
        "name": "Windows Defender (Disable)",
        "type": "defender",
        "packages": [],
        "desc": "Disables Defender Real-time Protection & services (Requires Tamper Protection OFF)."
    }
]


def is_admin():
    """Check if the script is running with Administrator privileges on Windows."""
    if sys.platform != "win32":
        return False
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def run_powershell(command):
    """Execute a PowerShell command with strict error handling."""
    ps_script = f"$ErrorActionPreference = 'Stop'; {command}"
    full_cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_script]
    result = subprocess.run(full_cmd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout.strip() or result.stderr.strip()


def remove_appx(package_patterns):
    """Remove AppX packages by wildcard while returning an actual failure if any match cannot be removed."""
    all_success = True
    messages = []

    for pattern in package_patterns:
        escaped_pattern = pattern.replace("'", "''")
        ps_script = f"""
$pattern = '{escaped_pattern}'
$packages = @(Get-AppxPackage -AllUsers -ErrorAction SilentlyContinue | Where-Object {{ $_.Name -like $pattern -or $_.PackageFullName -like $pattern -or $_.InstallLocation -like $pattern }})
$provisioned = @(Get-AppxProvisionedPackage -Online -ErrorAction SilentlyContinue | Where-Object {{ $_.DisplayName -like $pattern -or $_.PackageName -like $pattern }})

if ($packages.Count -eq 0 -and $provisioned.Count -eq 0) {{
    'NO_MATCHES'
    exit 0
}}

foreach ($pkg in $packages) {{
    try {{
        Remove-AppxPackage -AllUsers $pkg.PackageFullName -ErrorAction Stop | Out-Null
    }} catch {{
        $_ | Out-String
        exit 1
    }}
}}

foreach ($pkg in $provisioned) {{
    try {{
        Remove-AppxProvisionedPackage -Online -PackageName $pkg.PackageName -ErrorAction Stop | Out-Null
    }} catch {{
        $_ | Out-String
        exit 1
    }}
}}

'REMOVED'
"""
        success, msg = run_powershell(ps_script)
        if not success:
            all_success = False
        if msg:
            messages.append(msg)

    return all_success, "\n".join(messages)


def disable_copilot():
    """Remove Copilot AppX and set Registry keys to disable taskbar integration."""
    remove_appx(["*Copilot*"])
    reg_cmd = (
        'New-Item -Path "HKCU:\\Software\\Policies\\Microsoft\\Windows\\WindowsCopilot" -Force | Out-Null; '
        'Set-ItemProperty -Path "HKCU:\\Software\\Policies\\Microsoft\\Windows\\WindowsCopilot" -Name "TurnOffWindowsCopilot" -Value 1 -Type DWord; '
        'Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" -Name "ShowCopilotButton" -Value 0 -Type DWord'
    )
    return run_powershell(reg_cmd)


def disable_defender():
    """Disable Real-time Protection via PowerShell commands."""
    defender_cmd = (
        'Set-MpPreference -DisableRealtimeMonitoring $true -ErrorAction SilentlyContinue; '
        'Set-MpPreference -DisableBehaviorMonitoring $true -ErrorAction SilentlyContinue; '
        'Set-MpPreference -DisableIOAVProtection $true -ErrorAction SilentlyContinue'
    )
    return run_powershell(defender_cmd)


def remove_onedrive():
    """Kill running OneDrive processes and execute uninstaller."""
    subprocess.run(["taskkill", "/f", "/im", "OneDrive.exe"], capture_output=True)

    sys_root = os.environ.get("SystemRoot", "C:\\Windows")
    sys32 = os.path.join(sys_root, "System32", "OneDriveSetup.exe")
    sys64 = os.path.join(sys_root, "SysWOW64", "OneDriveSetup.exe")
    local_appdata = os.environ.get("LOCALAPPDATA", "")
    user_setup = os.path.join(local_appdata, "Microsoft", "OneDrive", "OneDriveSetup.exe")

    setup_path = None
    for path in [sys64, sys32, user_setup]:
        if os.path.exists(path):
            setup_path = path
            break

    if setup_path:
        proc = subprocess.run([setup_path, "/uninstall"], capture_output=True, text=True)
        return proc.returncode == 0, "OneDrive uninstalled successfully."
    return False, "OneDrive installer not found."


def display_menu(selected_indices):
    """Display the interactive selection menu."""
    os.system("cls" if os.name == "nt" else "clear")
    print("=" * 75)
    print("         WINDOWS DEBLOATER & APP REMOVER TOOL")
    print("=" * 75)
    print("Select items to REMOVE (Toggle numbers/ranges, then type 'R' to run):\n")

    for idx, item in enumerate(BLOATWARE_LIST, 1):
        status = "[X] REMOVE" if idx in selected_indices else "[ ] KEEP  "
        print(f"  {idx:2d}. {status}  {item['name']}")
        print(f"      └─ {item['desc']}")

    print("\n" + "-" * 75)
    print("  [#] Toggle items (e.g. enter 1, 3, or ranges like 1-5)")
    print("  [A] Select All  |  [N] Deselect All")
    print("  [R] RUN Removal Process")
    print("  [Q] Quit Script")
    print("-" * 75)


def toggle_indices(choice_str, current_selected, max_val):
    """Toggle individual numbers or ranges (e.g., 1-5) in the selection set."""
    parts = choice_str.replace(',', ' ').split()
    for part in parts:
        if '-' in part:
            sub = part.split('-')
            if len(sub) == 2 and sub[0].isdigit() and sub[1].isdigit():
                start, end = int(sub[0]), int(sub[1])
                for val in range(min(start, end), max(start, end) + 1):
                    if 1 <= val <= max_val:
                        if val in current_selected:
                            current_selected.remove(val)
                        else:
                            current_selected.add(val)
        elif part.isdigit():
            val = int(part)
            if 1 <= val <= max_val:
                if val in current_selected:
                    current_selected.remove(val)
                else:
                    current_selected.add(val)


def main():
    if not is_admin():
        print("[!] Error: This script must be run as Administrator on Windows.")
        print("Please restart Command Prompt or PowerShell as Administrator.")
        input("\nPress Enter to exit...")
        sys.exit(1)

    # All bloatware items are unselected by default
    selected_indices = set()

    while True:
        display_menu(selected_indices)
        choice = input("\nEnter choice: ").strip().lower()

        if choice == 'q':
            print("Exiting without making changes.")
            sys.exit(0)
        elif choice == 'a':
            selected_indices = set(range(1, len(BLOATWARE_LIST) + 1))
        elif choice == 'n':
            selected_indices.clear()
        elif choice == 'r':
            if not selected_indices:
                input("\nNo items selected to remove. Press Enter to go back...")
                continue
            break
        else:
            toggle_indices(choice, selected_indices, len(BLOATWARE_LIST))

    print("\n" + "=" * 75)
    print("STARTING REMOVAL PROCESS")
    print("=" * 75 + "\n")

    for idx in sorted(selected_indices):
        item = BLOATWARE_LIST[idx - 1]
        print(f"[*] Removing {item['name']}...")

        if item["type"] == "appx":
            success, msg = remove_appx(item["packages"])
        elif item["type"] == "copilot":
            success, msg = disable_copilot()
        elif item["type"] == "defender":
            success, msg = disable_defender()
        elif item["type"] == "onedrive":
            success, msg = remove_onedrive()
        else:
            success, msg = False, "Unknown action type"

        if success:
            print("    └─ Done.")
        else:
            print(f"    └─ Failed: {msg or 'See PowerShell output for details.'}")

    print("\n" + "=" * 75)
    print("DEBLOAT COMPLETE! Restart your PC for all changes to take effect.")
    print("=" * 75)
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()

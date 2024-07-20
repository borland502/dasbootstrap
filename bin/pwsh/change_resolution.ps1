# This function retrieves the default monitor
function Get-DefaultMonitor {
  Get-DisplayConfig | Where-Object { $_.IsPrimary } | Select-Object -ExpandProperty DeviceName
}

# Get the default monitor name
$monitorName = Get-DefaultMonitor

# Launch display settings with a delay to allow focus switch
Start-Process ms-settings:display -Wait -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Simulate keyboard presses to navigate and set 100% scaling
$wshShell = New-Object -ComObject WScript.Shell
$wshShell.SendKeys("{Tab 2}") # Move to scaling selection
$wshShell.SendKeys("^{Down 1}") # Select 100% scaling
$wshShell.SendKeys("%{Enter}") # Confirm selection

# Close the settings window
$wshShell.SendKeys("%{F4}")

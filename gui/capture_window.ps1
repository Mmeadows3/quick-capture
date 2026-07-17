# Native Windows Forms text capture dialog
# Dark theme, auto-focus, keyboard shortcuts (Enter=save, Shift+Enter=newline, Esc=cancel)

# Suppress all PowerShell internal output (prevents banner text from leaking into captured text)
$ErrorActionPreference = 'SilentlyContinue'
$WarningPreference = 'SilentlyContinue'
$VerbosePreference = 'SilentlyContinue'
$DebugPreference = 'SilentlyContinue'

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Main window (600x300, centered, dark theme, stays on top)
$form = New-Object System.Windows.Forms.Form
$form.Text = "Quick Capture"
$form.Size = New-Object System.Drawing.Size(600, 300)
$form.StartPosition = 'CenterScreen'
$form.TopMost = $true
$form.BackColor = [System.Drawing.Color]::FromArgb(30, 30, 30)

# Instructions label (white on dark)
$label = New-Object System.Windows.Forms.Label
$label.Location = New-Object System.Drawing.Point(10, 10)
$label.Size = New-Object System.Drawing.Size(560, 40)
$label.Text = "Type or press Win+H to dictate`nEnter = Save | Shift+Enter = New line | Esc = Cancel"
$label.ForeColor = [System.Drawing.Color]::White
$label.BackColor = [System.Drawing.Color]::FromArgb(30, 30, 30)
$form.Controls.Add($label)

# Text input box (multiline, scrollable, dark theme)
$textBox = New-Object System.Windows.Forms.TextBox
$textBox.Multiline = $true
$textBox.ScrollBars = 'Vertical'
$textBox.Location = New-Object System.Drawing.Point(10, 60)
$textBox.Size = New-Object System.Drawing.Size(560, 180)
$textBox.Font = New-Object System.Drawing.Font("Segoe UI", 12)
$textBox.BackColor = [System.Drawing.Color]::FromArgb(45, 45, 45)
$textBox.ForeColor = [System.Drawing.Color]::White
$textBox.Text = ""
$form.Controls.Add($textBox)

# Keyboard shortcuts: Enter=save (unless Shift held), Esc=cancel
$textBox.Add_KeyDown({
    param($sender, $e)
    if ($e.KeyCode -eq [System.Windows.Forms.Keys]::Enter) {
        if (-not $e.Shift) {
            $e.SuppressKeyPress = $true  # Don't add newline
            $form.DialogResult = [System.Windows.Forms.DialogResult]::OK
            $form.Close()
        }
        # Shift+Enter: allow default newline
    }
    if ($e.KeyCode -eq [System.Windows.Forms.Keys]::Escape) {
        $form.DialogResult = [System.Windows.Forms.DialogResult]::Cancel
        $form.Close()
    }
})

# Auto-focus text box when window opens
$form.Add_Shown({
    $textBox.Select()
    $form.Activate()
})

# Show dialog, wait for user
$dialogResult = $form.ShowDialog()

# Filter out PowerShell banner lines that sometimes leak into dictation
# Only output if user pressed Enter (OK) and there's text
if ($dialogResult -eq [System.Windows.Forms.DialogResult]::OK -and $textBox.Text.Trim() -ne "") {
    $capturedText = $textBox.Text.Trim()

    # Noise patterns that should never be legitimate user input
    $noisePatterns = @(
        'Windows PowerShell',
        'Copyright',
        'Microsoft Corporation',
        'All rights reserved',
        'Try the new cross-platform PowerShell',
        'https://aka.ms/pscore6'
    )

    # Remove lines containing noise patterns
    $cleanLines = $capturedText -split "`n" | Where-Object {
        $line = $_
        $isNoise = $false
        foreach ($pattern in $noisePatterns) {
            if ($line -like "*$pattern*") {
                $isNoise = $true
                break
            }
        }
        -not $isNoise
    }

    $cleanText = ($cleanLines -join "`n").Trim()

    # Output clean text to stdout (Python captures this)
    if ($cleanText -ne "") {
        Write-Output $cleanText
    }
}

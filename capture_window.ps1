# capture_window.ps1 - Windows Forms capture window
# This is a PowerShell script that shows a native Windows form for text capture
# Goal: Fast, native Windows GUI that auto-focuses

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Create the form (window)
# System.Windows.Forms.Form = native Windows window class
$form = New-Object System.Windows.Forms.Form
$form.Text = "Quick Capture"
$form.Size = New-Object System.Drawing.Size(600, 300)
$form.StartPosition = 'CenterScreen'  # Center on screen automatically
$form.TopMost = $true  # Stay on top of other windows
$form.BackColor = [System.Drawing.Color]::FromArgb(30, 30, 30)  # Dark background

# Label with instructions
# System.Drawing.Color::FromArgb(R, G, B) = RGB color (white text)
$label = New-Object System.Windows.Forms.Label
$label.Location = New-Object System.Drawing.Point(10, 10)
$label.Size = New-Object System.Drawing.Size(560, 40)
$label.Text = "Type or press Win+H to dictate`nEnter = Save | Shift+Enter = New line | Esc = Cancel"
$label.ForeColor = [System.Drawing.Color]::White
$label.BackColor = [System.Drawing.Color]::FromArgb(30, 30, 30)
$form.Controls.Add($label)

# Text box for typing/dictation
# Multiline = allows multiple lines of text
# ScrollBars = shows scrollbar if text is long
$textBox = New-Object System.Windows.Forms.TextBox
$textBox.Multiline = $true
$textBox.ScrollBars = 'Vertical'
$textBox.Location = New-Object System.Drawing.Point(10, 60)
$textBox.Size = New-Object System.Drawing.Size(560, 180)
$textBox.Font = New-Object System.Drawing.Font("Segoe UI", 12)
$textBox.BackColor = [System.Drawing.Color]::FromArgb(45, 45, 45)  # Slightly lighter dark
$textBox.ForeColor = [System.Drawing.Color]::White
$form.Controls.Add($textBox)

# Handle Enter key in the text box
# In multiline text boxes, Enter adds new line by default
# We want: Enter = save, Shift+Enter = new line
$textBox.Add_KeyDown({
    param($sender, $e)
    # Check if Enter key pressed (KeyCode 13 = Enter)
    if ($e.KeyCode -eq [System.Windows.Forms.Keys]::Enter) {
        # If Shift NOT held down, save and close
        if (-not $e.Shift) {
            $e.SuppressKeyPress = $true  # Don't add newline
            $form.DialogResult = [System.Windows.Forms.DialogResult]::OK
            $form.Close()
        }
        # If Shift IS held down, allow the newline (do nothing)
    }
    # Escape key also handled here
    if ($e.KeyCode -eq [System.Windows.Forms.Keys]::Escape) {
        $form.DialogResult = [System.Windows.Forms.DialogResult]::Cancel
        $form.Close()
    }
})

# Variable to store result
$result = ""

# When form is shown, focus the text box
# Add_Shown event fires when window appears
$form.Add_Shown({
    $textBox.Select()  # Focus the text box
    $form.Activate()   # Bring window to front
})

# Show the form and wait for user action
# ShowDialog() = modal window (blocks until closed)
# Returns OK if Enter pressed, Cancel if Esc pressed
$dialogResult = $form.ShowDialog()

# Output the result to stdout (Python will read this)
# If user pressed Enter and there's text, output it
# If user pressed Esc or no text, output nothing
if ($dialogResult -eq [System.Windows.Forms.DialogResult]::OK -and $textBox.Text.Trim() -ne "") {
    # Write to stdout (Python reads this)
    Write-Output $textBox.Text.Trim()
}
# If cancelled or empty, output nothing (empty string)

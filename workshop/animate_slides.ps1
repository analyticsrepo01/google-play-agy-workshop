param(
    [string]$InputPath = (Join-Path $PSScriptRoot 'Beyond_AI_Assisted_Coding.pptx'),
    [string]$OutputPath = (Join-Path $PSScriptRoot 'Beyond_AI_Assisted_Coding_Animated.pptx')
)

$ErrorActionPreference = 'Stop'
$InputPath = (Resolve-Path -LiteralPath $InputPath).Path
$OutputPath = [System.IO.Path]::GetFullPath($OutputPath)
if ($InputPath -eq $OutputPath) {
    throw 'Use a separate output path to preserve the saved presentation.'
}

function Get-OfficeColor([string]$Hex) {
    return [Convert]::ToInt32($Hex.Substring(0, 2), 16) +
        256 * [Convert]::ToInt32($Hex.Substring(2, 2), 16) +
        65536 * [Convert]::ToInt32($Hex.Substring(4, 2), 16)
}

function Add-Reveal($Slide, $Shape, [int]$Trigger, [int]$Effect = 10, [single]$Duration = 0.35) {
    $animation = $Slide.TimeLine.MainSequence.AddEffect($Shape, $Effect, 0, $Trigger)
    if ($Effect -eq 22) {
        $animation.EffectParameters.Direction = 4
    }
    $animation.Timing.Duration = $Duration
    $animation.Timing.TriggerDelayTime = 0
}

function Add-Journey($Slide, [int]$Stage, [bool]$Cover, [bool]$Dark) {
    $labels = @('VIBE', 'TOOLS', 'SETUP', 'SKILLS', 'MCP', 'AGENT')
    $colors = @('185ABC', '185ABC', '137333', '137333', 'B3261E', 'B3261E')
    $left = 374
    $top = 19
    $width = 49
    $height = 16
    $gap = 4
    if ($Cover) {
        $left = 54
        $top = 61
        $width = 97
        $height = 14
        $gap = 4
    }
    for ($index = 0; $index -lt $labels.Count; $index++) {
        $chip = $Slide.Shapes.AddShape(5, $left + $index * ($width + $gap), $top, $width, $height)
        $chip.Name = "Workshop journey $($index + 1)"
        $chip.Adjustments.Item(1) = 0.4
        $chip.Line.Visible = 0
        $chip.Fill.Solid()
        $chip.Fill.ForeColor.RGB = Get-OfficeColor $(if ($index -eq $Stage) {
            $colors[$index]
        } elseif ($Dark) {
            '162B27'
        } else {
            'EEF3FA'
        })
        $chip.TextFrame.MarginLeft = 0
        $chip.TextFrame.MarginRight = 0
        $chip.TextFrame.MarginTop = 0
        $chip.TextFrame.MarginBottom = 0
        $chip.TextFrame.VerticalAnchor = 3
        $chip.TextFrame.TextRange.Text = $labels[$index]
        $chip.TextFrame.TextRange.Font.Name = 'Arial'
        $chip.TextFrame.TextRange.Font.Size = 8
        $chip.TextFrame.TextRange.Font.Bold = -1
        $chip.TextFrame.TextRange.Font.Color.RGB = Get-OfficeColor $(if ($index -eq $Stage -or $Dark) {
            'FFFFFF'
        } else {
            '475569'
        })
        $chip.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        $chip.AlternativeText = "$($labels[$index])$(if ($index -eq $Stage) { ': current chapter' })"
    }
}

$questions = @(
    'YOUR TURN | What would you like to build?',
    'YOUR TURN | Ready to build this together?',
    'CHAT | First AI build, or already building?',
    'PREDICT | What is missing from this prompt?',
    'REFLECT | What would count as real proof?',
    'CHAT | Which tool is your starting point?',
    'SPOT IT | Context, action, or evidence?',
    'PREDICT | What should happen before edits?',
    'CHECK | Account sign-in or model API key?',
    'SPOT IT | Real MCP or optional AI?',
    'DECIDE | Which permission would you limit?',
    'REFLECT | What workflow would you reuse?',
    'PREDICT | A plan, or permission to edit?',
    'QUICK CHECK | Skill, MCP, or agent?',
    'SPOT IT | Which two tools are exposed?',
    'PREDICT | Who builds, and who runs?',
    'SPOT IT | Where are points enforced?',
    'CHECK | Does the reply match tool data?',
    'PLAY | Answer on your phone; code ranks.',
    'RECAP | Skill vs MCP vs application tool?',
    'YOUR TURN | What will you build next?'
)

$app = $null
$deck = $null
try {
    $app = New-Object -ComObject PowerPoint.Application
    $deck = $app.Presentations.Open($InputPath, -1, 0, 0)
    if ($deck.Slides.Count -ne 21 -or
        [Math]::Abs($deck.PageSetup.SlideWidth - 720) -gt 0.1 -or
        [Math]::Abs($deck.PageSetup.SlideHeight - 405) -gt 0.1) {
        throw 'This finishing pass expects the 21-slide, 720 x 405 point workshop deck.'
    }
    foreach ($slide in $deck.Slides) {
        if ($slide.TimeLine.MainSequence.Count -gt 0 -or $slide.TimeLine.InteractiveSequences.Count -gt 0) {
            throw 'The input already has animation. Use the saved unanimated deck to avoid replacing custom effects.'
        }
    }
    for ($number = 1; $number -le $deck.Slides.Count; $number++) {
        $slide = $deck.Slides.Item($number)
        $original = @($slide.Shapes | ForEach-Object { $_ })
        $contentNumber = if ($number -gt 2) { $number - 1 } else { $number }
        $dark = $contentNumber -in @(6, 7, 17)
        $phase = $contentNumber -in @(4, 16, 19)
        $stage = if ($contentNumber -le 4) { 0 } elseif ($contentNumber -le 7) { 1 } elseif ($contentNumber -le 10) {
            2
        } elseif ($contentNumber -le 12) { 3 } elseif ($contentNumber -le 14) { 4 } else { 5 }

        Add-Journey $slide $stage ($number -eq 1) ($dark -or $phase)
        $question = $slide.Shapes.AddTextbox(1, 365, 384.5, 277, 12)
        $question.Name = 'Workshop audience question'
        $question.TextFrame.MarginLeft = 0
        $question.TextFrame.MarginRight = 0
        $question.TextFrame.MarginTop = 0
        $question.TextFrame.MarginBottom = 0
        $question.TextFrame.TextRange.Text = $questions[$number - 1]
        $question.TextFrame.TextRange.Font.Name = 'Arial'
        $question.TextFrame.TextRange.Font.Size = 8
        $question.TextFrame.TextRange.Font.Bold = -1
        $question.TextFrame.TextRange.Font.Color.RGB = Get-OfficeColor $(if ($dark) {
            'FFFFFF'
        } else {
            '20344B'
        })
        $question.TextFrame.TextRange.ParagraphFormat.Alignment = 3
        $savedFooter = @($original | Where-Object {
            $_.HasTextFrame -eq -1 -and $_.TextFrame.TextRange.Text.Trim() -ne '' -and
            $_.Top -gt 375 -and $_.Left -ge 360 -and $_.Left -lt 645
        })
        if ($savedFooter.Count -gt 0) {
            $question.Top = 373.75
            $question.Height = 10.5
        }

        # All original objects stay editable and keep their positions and IDs.
        if ($number -eq 1) {
            $title = @($original | Where-Object {
                $_.HasTextFrame -eq -1 -and $_.TextFrame.TextRange.Text -eq 'Beyond AI-Assisted Coding'
            })
            if ($title.Count -ne 1) { throw 'Cannot identify the saved cover title.' }
            Add-Reveal $slide $title[0] 2
            foreach ($photo in @($original | Where-Object { $_.Type -eq 13 })) {
                Add-Reveal $slide $photo 2 10 0.5
            }
            foreach ($shape in @($original | Where-Object {
                $_.HasTextFrame -eq -1 -and $_.Top -ge 248 -and $_.Top -lt 328
            })) {
                Add-Reveal $slide $shape $(if ($shape.Top -lt 280) { 1 } else { 2 }) 22 0.4
            }
        } else {
            $headers = @($original | Where-Object {
                $_.HasTextFrame -eq -1 -and $_.TextFrame.TextRange.Text.Trim() -ne '' -and
                $_.Top -ge 40 -and $_.Top -lt 100
            } | Sort-Object Left)
            foreach ($heading in $headers) {
                Add-Reveal $slide $heading 2 10 0.3
            }
            if ($contentNumber -eq 20) {
                $resources = @($original | Where-Object {
                    $_.HasTextFrame -eq -1 -and $_.TextFrame.TextRange.Text.Trim() -ne '' -and
                    $_.Left -lt 500 -and $_.Top -ge 144 -and $_.Top -lt 330
                } | Sort-Object Top)
                for ($index = 0; $index -lt $resources.Count; $index++) {
                    Add-Reveal $slide $resources[$index] $(if ($index -in @(0, 4)) { 1 } else { 2 })
                }
            } else {
                $panels = @($original | Where-Object {
                    [Math]::Abs($_.Top - 142.5) -lt 0.2 -and $_.Width -gt 200 -and $_.Height -gt 220
                } | Sort-Object Left)
                if ($panels.Count -lt 2 -or $panels.Count -gt 3) {
                    throw "Slide $number does not have the expected saved card layout."
                }
                for ($panelIndex = 0; $panelIndex -lt $panels.Count; $panelIndex++) {
                    $panel = $panels[$panelIndex]
                    $members = @($original | Where-Object {
                        $_.Left -ge $panel.Left - 0.2 -and $_.Top -ge $panel.Top - 0.2 -and
                        $_.Left + $_.Width -le $panel.Left + $panel.Width + 5 -and
                        $_.Top + $_.Height -le $panel.Top + $panel.Height + 5
                    })
                    if ($members.Count -lt 4) { throw "Slide $number has an incomplete card." }
                    for ($index = 0; $index -lt $members.Count; $index++) {
                        $member = $members[$index]
                        $effect = if ($member.HasTextFrame -eq -1 -and
                            $member.TextFrame.TextRange.Text.Trim() -ne '' -and $member.Top -ge 168) { 22 } else { 10 }
                        Add-Reveal $slide $member $(if ($index -eq 0) { 1 } else { 2 }) $effect 0.35
                    }
                    if (-not $phase) {
                        $tab = $slide.Shapes.AddShape(9, $panel.Left + $panel.Width - 23, 134, 17, 17)
                        $tab.Name = "Workshop step $($panelIndex + 1)"
                        $tab.Line.Visible = 0
                        $tab.Fill.ForeColor.RGB = Get-OfficeColor $(if ($dark) { '00FF94' } else { '20344B' })
                        $tab.TextFrame.MarginLeft = 0
                        $tab.TextFrame.MarginRight = 0
                        $tab.TextFrame.MarginTop = 0
                        $tab.TextFrame.MarginBottom = 0
                        $tab.TextFrame.VerticalAnchor = 3
                        $tab.TextFrame.TextRange.Text = ($panelIndex + 1).ToString()
                        $tab.TextFrame.TextRange.Font.Name = 'Arial'
                        $tab.TextFrame.TextRange.Font.Size = 8
                        $tab.TextFrame.TextRange.Font.Bold = -1
                        $tab.TextFrame.TextRange.Font.Color.RGB = Get-OfficeColor $(if ($dark) { '000000' } else { 'FFFFFF' })
                        $tab.TextFrame.TextRange.ParagraphFormat.Alignment = 2
                        Add-Reveal $slide $tab 2
                    }
                }
            }
        }
        $slide.SlideShowTransition.EntryEffect = 3849
        $slide.SlideShowTransition.Duration = 0.4
        $slide.SlideShowTransition.AdvanceOnClick = -1
        $slide.SlideShowTransition.AdvanceOnTime = 0
        Write-Output "Slide $number : $($slide.TimeLine.MainSequence.Count) coordinated effects; click-controlled."
    }
    $deck.SlideShowSettings.ShowWithAnimation = -1
    $deck.SlideShowSettings.AdvanceMode = 1
    $deck.SaveAs($OutputPath, 24)
    Write-Output "Saved animated copy: $OutputPath"
} finally {
    if ($null -ne $deck) {
        $deck.Close()
        [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($deck)
    }
    if ($null -ne $app) {
        [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($app)
    }
}

param(
    [Parameter(Mandatory = $true)]
    [string]$ScratchDirectory
)

$ErrorActionPreference = 'Stop'
$ScratchDirectory = [System.IO.Path]::GetFullPath($ScratchDirectory)
New-Item -ItemType Directory -Path $ScratchDirectory -Force | Out-Null
$app = $null
$deck = $null
try {
    $app = New-Object -ComObject PowerPoint.Application
    foreach ($name in @('Beyond_AI_Assisted_Coding', 'Beyond_AI_Assisted_Coding_Animated')) {
        $source = Join-Path $PSScriptRoot "$name.pptx"
        $copy = Join-Path $ScratchDirectory "$name.render-copy.pptx"
        Copy-Item -LiteralPath $source -Destination $copy
        try {
            # Render a private copy, not a presentation the user may have open.
            $deck = $app.Presentations.Open($copy, -1, 0, 0)
            if ($deck.Slides.Count -ne 21) {
                throw "Expected 21 slides in $name."
            }
            $preview = Join-Path $ScratchDirectory $name
            New-Item -ItemType Directory -Path $preview -Force | Out-Null
            foreach ($slide in $deck.Slides) {
                foreach ($shape in $slide.Shapes) {
                    if ($shape.HasTextFrame -and $shape.TextFrame.HasText) {
                        $frame = $shape.TextFrame2
                        $width = $shape.Width - $frame.MarginLeft - $frame.MarginRight
                        $height = $shape.Height - $frame.MarginTop - $frame.MarginBottom
                        if ($frame.TextRange.BoundWidth -gt $width + 1 -or
                            $frame.TextRange.BoundHeight -gt $height + 1) {
                            Write-Warning "$name slide $($slide.SlideIndex), shape $($shape.Id): text exceeds native bounds."
                        }
                    }
                }
                $slide.Export((Join-Path $preview "slide-$($slide.SlideIndex).png"), 'PNG', 1440, 810)
            }
            $deck.SaveAs((Join-Path $PSScriptRoot "$name.pdf"), 32)
            Write-Output "Exported $name.pdf and 21 slide previews."
        } finally {
            if ($null -ne $deck) {
                $deck.Close()
                [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($deck)
                $deck = $null
            }
            Remove-Item -LiteralPath $copy
        }
    }
} finally {
    if ($null -ne $app) {
        # Do not quit PowerPoint: other presentations may belong to the user.
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($app)
    }
}

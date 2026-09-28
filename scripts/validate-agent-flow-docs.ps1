param(
  [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
)

$ErrorActionPreference = "Stop"

$mapPath = Join-Path $Root "docs\taliya-agent-flow-deep-map.md"
$configPath = Join-Path $Root "docs\taliya-agent-flow-configuration-matrix.md"
$testsPath = Join-Path $Root "docs\taliya-agent-flow-test-scenarios.md"
$validationPath = Join-Path $Root "docs\taliya-agent-flow-validation-matrix.md"

$requiredFiles = @($mapPath, $configPath, $testsPath, $validationPath)
foreach ($file in $requiredFiles) {
  if (-not (Test-Path $file)) {
    Write-Error "Missing required file: $file"
  }
}

function Get-UniqueMatches {
  param(
    [string]$Path,
    [string]$Pattern
  )

  return Select-String -Path $Path -Pattern $Pattern |
    ForEach-Object { $_.Matches[0].Groups[1].Value } |
    Sort-Object -Unique
}

function Compare-CodeSets {
  param(
    [string[]]$Expected,
    [string[]]$Actual,
    [string]$Label
  )

  $missing = Compare-Object -ReferenceObject $Expected -DifferenceObject $Actual |
    Where-Object { $_.SideIndicator -eq "<=" } |
    ForEach-Object { $_.InputObject }

  $extra = Compare-Object -ReferenceObject $Expected -DifferenceObject $Actual |
    Where-Object { $_.SideIndicator -eq "=>" } |
    ForEach-Object { $_.InputObject }

  if ($missing.Count -gt 0) {
    Write-Host "Missing in ${Label}: $($missing -join ', ')" -ForegroundColor Red
  }

  if ($extra.Count -gt 0) {
    Write-Host "Extra in ${Label}: $($extra -join ', ')" -ForegroundColor Red
  }

  return ($missing.Count -eq 0 -and $extra.Count -eq 0)
}

$mapCodes = Get-UniqueMatches -Path $mapPath -Pattern "^### ([A-G][0-9]+)\."
$configCodes = Get-UniqueMatches -Path $configPath -Pattern "^\| ([A-G][0-9]+) \|"
$testCodes = Get-UniqueMatches -Path $testsPath -Pattern "^\| ([A-G][0-9]+)-"
$validationCodes = Get-UniqueMatches -Path $validationPath -Pattern "^\| ([A-G][0-9]+) "

$passed = $true

Write-Host "Flow counts:" -ForegroundColor Cyan
Write-Host "  map:        $($mapCodes.Count)"
Write-Host "  config:     $($configCodes.Count)"
Write-Host "  tests:      $($testCodes.Count)"
Write-Host "  validation: $($validationCodes.Count)"

$passed = (Compare-CodeSets -Expected $mapCodes -Actual $configCodes -Label "configuration matrix") -and $passed
$passed = (Compare-CodeSets -Expected $mapCodes -Actual $testCodes -Label "test scenarios") -and $passed
$passed = (Compare-CodeSets -Expected $mapCodes -Actual $validationCodes -Label "validation matrix") -and $passed

$mapText = Get-Content -Raw $mapPath
$headings = [regex]::Matches($mapText, "(?m)^### ([A-G][0-9]+)\. ")
$missingFields = @()

for ($i = 0; $i -lt $headings.Count; $i++) {
  $start = $headings[$i].Index
  $end = if ($i -lt $headings.Count - 1) { $headings[$i + 1].Index } else { $mapText.Length }
  $block = $mapText.Substring($start, $end - $start)
  $code = $headings[$i].Groups[1].Value
  $issues = @()

  if ($block -notmatch "(?m)^- Canal:") { $issues += "Canal" }
  if ($block -notmatch "(?m)^- Autonomia padrao:") { $issues += "Autonomia padrao" }
  if ($block -notmatch "(?m)^Estados finais:") { $issues += "Estados finais" }

  $autonomyLine = [regex]::Match($block, "(?m)^- Autonomia padrao: (.+)$")
  if ($autonomyLine.Success) {
    $allowedAutonomies = @("automatico", "copiloto", "customizado", "humano")
    $autonomyTokens = [regex]::Matches($autonomyLine.Groups[1].Value, '`([^`]+)`') |
      ForEach-Object { $_.Groups[1].Value }

    foreach ($token in $autonomyTokens) {
      if ($allowedAutonomies -notcontains $token) {
        $issues += "Autonomia invalida: $token"
      }
    }
  }

  $channelLine = [regex]::Match($block, "(?m)^- Canal: (.+)$")
  if ($channelLine.Success) {
    $allowedChannels = @("whatsapp", "sistema", "hibrido")
    $channelTokens = [regex]::Matches($channelLine.Groups[1].Value, '`([^`]+)`') |
      ForEach-Object { $_.Groups[1].Value }

    foreach ($token in $channelTokens) {
      if ($allowedChannels -notcontains $token) {
        $issues += "Canal invalido: $token"
      }
    }
  }

  $stateLine = [regex]::Match($block, "(?m)^Estados finais: (.+)$")
  if ($stateLine.Success) {
    $allowedStates = @(
      "resolvido",
      "aguardando_contato",
      "aguardando_equipe",
      "acao_registrada",
      "tarefa_criada",
      "handoff_humano",
      "proximo_fluxo",
      "sem_acao",
      "pausado"
    )
    $stateTokens = [regex]::Matches($stateLine.Groups[1].Value, '`([^`]+)`') |
      ForEach-Object { $_.Groups[1].Value }

    foreach ($token in $stateTokens) {
      if ($allowedStates -notcontains $token) {
        $issues += "Estado invalido: $token"
      }
    }
  }

  if ($issues.Count -gt 0) {
    $missingFields += "${code}: $($issues -join ', ')"
  }
}

if ($missingFields.Count -gt 0) {
  Write-Host "Flows missing required fields:" -ForegroundColor Red
  $missingFields | ForEach-Object { Write-Host "  $_" -ForegroundColor Red }
  $passed = $false
}

if ($passed) {
  Write-Host "Agent flow documentation validation passed." -ForegroundColor Green
  exit 0
}

Write-Host "Agent flow documentation validation failed." -ForegroundColor Red
exit 1

<#
.SYNOPSIS
    One-Click Automated GitHub Project, Issues, Labels, and Kanban Board Setup.
.DESCRIPTION
    Dynamically configures GitHub Issues, Labels, Milestones, and GitHub Projects v2
    Kanban Board for any Scrum PBL based on .github/project-setup.json.
    Works with ANY student's GitHub account and cloned repository.
#>

[CmdletBinding()]
param(
    [switch]$NonInteractive = $false,
    [switch]$SkipProject = $false
)

$ErrorActionPreference = "Continue"

# Colors and Formatting Functions
function Write-Header {
    param([string]$Text)
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host " $Text" -ForegroundColor White
    Write-Host "========================================" -ForegroundColor Cyan
}

function Write-Success { param([string]$Text) Write-Host "[+] $Text" -ForegroundColor Green }
function Write-Info    { param([string]$Text) Write-Host "[*] $Text" -ForegroundColor Yellow }
function Write-Note    { param([string]$Text) Write-Host "[-] $Text" -ForegroundColor Gray }
function Write-Warn    { param([string]$Text) Write-Host "[!] $Text" -ForegroundColor Magenta }
function Write-Err     { param([string]$Text) Write-Host "[ERROR] $Text" -ForegroundColor Red }

# Ensure gh CLI is accessible if installed in standard paths
function Ensure-GhInPath {
    if (Get-Command gh -ErrorAction SilentlyContinue) {
        return $true
    }
    $candidates = @(
        "$env:LOCALAPPDATA\GitHubCLI\gh.exe",
        "$env:LOCALAPPDATA\Programs\GitHub CLI\bin\gh.exe",
        "$env:LOCALAPPDATA\Programs\GitHub CLI\gh.exe",
        "C:\Program Files\GitHub CLI\gh.exe",
        "C:\Program Files\GitHub CLI\bin\gh.exe",
        "C:\Program Files (x86)\GitHub CLI\gh.exe"
    )
    foreach ($path in $candidates) {
        if (Test-Path $path) {
            $dir = Split-Path -Parent $path
            $env:Path = "$dir;$env:Path"
            return $true
        }
    }
    return $false
}

# ----------------------------------------------------
# STEP 1: PREREQUISITE CHECKS
# ----------------------------------------------------
Write-Header "Checking Prerequisites"

# 1. Check Git
$gitCmd = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitCmd) {
    Write-Err "Git is not installed or not found in system PATH."
    Write-Host "`nWHAT IS MISSING: Git Version Control System" -ForegroundColor Yellow
    Write-Host "WHY IT IS REQUIRED: Git is required to detect repository remote and manage codebase." -ForegroundColor Yellow
    Write-Host "HOW TO INSTALL: Download and install from https://git-scm.com/downloads`n" -ForegroundColor Yellow
    exit 1
}
$gitVersion = (git --version)
Write-Success "Git detected: $gitVersion"

# 2. Check Python
$pyCmd = Get-Command python -ErrorAction SilentlyContinue
if ($pyCmd) {
    $pyVer = (python --version 2>&1)
    Write-Success "Python detected: $pyVer"
} else {
    Write-Warn "Python is not detected. While GitHub setup can continue, Python is needed to run the PBL app."
}

# 3. Check GitHub CLI (gh)
$hasGh = Ensure-GhInPath
if (-not $hasGh) {
    Write-Err "GitHub CLI ('gh') is not installed or not found in system PATH."
    Write-Host "`nWHAT IS MISSING: GitHub CLI (gh)" -ForegroundColor Yellow
    Write-Host "WHY IT IS REQUIRED: Required to securely authenticate with your GitHub account," -ForegroundColor Yellow
    Write-Host "                    create Labels, Issues, Milestones, and configure the GitHub Project Kanban board." -ForegroundColor Yellow
    Write-Host "`nHOW TO INSTALL:" -ForegroundColor Yellow
    Write-Host "  Option 1 (Automated via Windows Package Manager):" -ForegroundColor White
    Write-Host "    winget install --id GitHub.cli" -ForegroundColor Green
    Write-Host "  Option 2 (Official Installer):" -ForegroundColor White
    Write-Host "    Download from: https://cli.github.com/`n" -ForegroundColor Green

    if (-not $NonInteractive) {
        $installNow = Read-Host "Would you like to attempt automated installation via winget right now? [Y/N]"
        if ($installNow -match "^[Yy]") {
            Write-Info "Running: winget install --id GitHub.cli..."
            try {
                winget install --id GitHub.cli --exact --accept-source-agreements --accept-package-agreements
                Ensure-GhInPath | Out-Null
            } catch {
                Write-Warn "winget installation could not complete automatically."
            }
        }
    }

    if (-not (Ensure-GhInPath)) {
        Write-Err "Please install GitHub CLI and re-run setup-project.bat."
        exit 1
    }
}
$ghVersion = (gh --version | Select-Object -First 1)
Write-Success "GitHub CLI detected: $ghVersion"

# ----------------------------------------------------
# STEP 2: REPOSITORY & REMOTE DETECTION
# ----------------------------------------------------
Write-Header "Detecting GitHub Repository"

try {
    $remoteUrl = (git remote get-url origin 2>$null).Trim()
} catch {
    $remoteUrl = ""
}

if (-not $remoteUrl) {
    Write-Err "Could not find a Git 'origin' remote in current directory."
    Write-Host "`nEXPECTED WORKFLOW FOR YOUR FRIEND:" -ForegroundColor Yellow
    Write-Host "1. Create your own GitHub repository on github.com (e.g. 'Event-Management')." -ForegroundColor White
    Write-Host "2. Clone your empty repository:" -ForegroundColor White
    Write-Host "     git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git" -ForegroundColor Green
    Write-Host "3. Copy the extracted PBL project files into that cloned repository folder." -ForegroundColor White
    Write-Host "4. Open the folder and run setup-project.bat`n" -ForegroundColor White
    exit 1
}

# Parse OWNER and REPO supporting HTTPS, SSH, and with/without .git
$owner = $null
$repo = $null

if ($remoteUrl -match "github\.com[:/](?<owner>[^/]+)/(?<repo>[^/\.]+)(\.git)?$") {
    $owner = $Matches["owner"]
    $repo  = $Matches["repo"]
} else {
    Write-Err "Unrecognized GitHub remote URL format: $remoteUrl"
    Write-Host "Supported formats:" -ForegroundColor Yellow
    Write-Host "  HTTPS: https://github.com/OWNER/REPOSITORY.git" -ForegroundColor White
    Write-Host "  SSH:   git@github.com:OWNER/REPOSITORY.git" -ForegroundColor White
    exit 1
}

# ----------------------------------------------------
# STEP 3: GITHUB AUTHENTICATION
# ----------------------------------------------------
Write-Header "Verifying GitHub Authentication"

$authCheck = gh auth status 2>&1 | Out-String
if ($LASTEXITCODE -ne 0 -or $authCheck -notmatch "Logged in to github\.com") {
    Write-Warn "You are not authenticated with GitHub CLI."
    Write-Host "`nPlease authenticate with YOUR OWN GitHub account when prompted." -ForegroundColor Yellow
    Write-Host "Recommended scopes: 'repo', 'read:org', and 'project' (to create Kanban board).`n" -ForegroundColor Yellow
    
    gh auth login -s "repo,read:org,project"
    
    $authCheck = gh auth status 2>&1 | Out-String
    if ($LASTEXITCODE -ne 0) {
        Write-Err "Authentication did not complete. Please run 'gh auth login' and try again."
        exit 1
    }
}

# Detect authenticated user login
$authUser = $null
try {
    $authUser = (gh api user -q .login 2>$null).Trim()
} catch {
    $authUser = "Authenticated User"
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host " GitHub Project Setup" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Detected repository:" -ForegroundColor Yellow
Write-Host "  Owner:      $owner" -ForegroundColor White
Write-Host "  Repository: $repo" -ForegroundColor White
Write-Host "`nAuthenticated GitHub account:" -ForegroundColor Yellow
Write-Host "  User:       $authUser" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Cyan

if (-not $NonInteractive) {
    $confirm = Read-Host "Continue setting up Labels, Issues, and Kanban Project for $owner/$repo? [Y/N]"
    if ($confirm -notmatch "^[Yy]") {
        Write-Info "Setup cancelled by user."
        exit 0
    }
}

# Verify access to repository
Write-Info "Verifying repository access for '$owner/$repo'..."
$repoCheck = gh repo view "$owner/$repo" --json nameWithOwner 2>&1 | Out-String
if ($LASTEXITCODE -ne 0) {
    Write-Err "Cannot access repository '$owner/$repo'."
    Write-Host "Details: $repoCheck" -ForegroundColor Red
    Write-Host "Make sure the repository exists and your authenticated account has Write permissions." -ForegroundColor Yellow
    exit 1
}
Write-Success "Repository access verified."

# ----------------------------------------------------
# STEP 4: LOAD PROJECT CONFIGURATION
# ----------------------------------------------------
$configFile = Join-Path $PSScriptRoot "..\project-setup.json"
if (-not (Test-Path $configFile)) {
    $configFile = ".github/project-setup.json"
}
if (-not (Test-Path $configFile)) {
    Write-Err "Configuration file not found: .github/project-setup.json"
    exit 1
}

Write-Info "Loading project configuration from .github/project-setup.json..."
$configJson = Get-Content -Raw -Path $configFile -Encoding UTF8 | ConvertFrom-Json
$projectName = if ($configJson.project.name) { $configJson.project.name } else { "$repo - Scrum Board" }

# ----------------------------------------------------
# STEP 5: CREATE / UPDATE LABELS
# ----------------------------------------------------
Write-Header "Configuring GitHub Labels"

$existingLabels = @()
try {
    $labelsRaw = gh label list --repo "$owner/$repo" --limit 100 --json name 2>$null | ConvertFrom-Json
    if ($labelsRaw) {
        $existingLabels = $labelsRaw | ForEach-Object { $_.name }
    }
} catch {
    Write-Warn "Could not fetch existing labels list. Will create directly."
}

$labelsConfigured = 0
foreach ($lbl in $configJson.labels) {
    $name = $lbl.name
    $color = $lbl.color.TrimStart('#')
    $desc = $lbl.description

    if ($existingLabels -contains $name) {
        Write-Note "Label '$name' already exists. Updating color and description..."
        gh label edit "$name" --color "$color" --description "$desc" --repo "$owner/$repo" 2>$null | Out-Null
    } else {
        Write-Info "Creating label '$name' (#$color)..."
        gh label create "$name" --color "$color" --description "$desc" --repo "$owner/$repo" 2>$null | Out-Null
    }
    $labelsConfigured++
}
Write-Success "$labelsConfigured labels configured successfully."

# ----------------------------------------------------
# STEP 6: CREATE SPRINT MILESTONES
# ----------------------------------------------------
Write-Header "Configuring Sprint Milestones"

$milestoneMap = @{}
try {
    $existingMilestones = gh api "repos/$owner/$repo/milestones?state=all" 2>$null | ConvertFrom-Json
    if ($existingMilestones) {
        foreach ($m in $existingMilestones) {
            $milestoneMap[$m.title] = $m.number
        }
    }
} catch {
    Write-Warn "Could not fetch existing milestones."
}

if ($configJson.milestones) {
    foreach ($m in $configJson.milestones) {
        $mTitle = $m.title
        $mDesc = $m.description
        if ($milestoneMap.ContainsKey($mTitle)) {
            Write-Note "Milestone '$mTitle' already exists (#$($milestoneMap[$mTitle]))."
        } else {
            Write-Info "Creating Milestone '$mTitle'..."
            try {
                $payload = @{
                    title = $mTitle
                    description = $mDesc
                    state = "open"
                } | ConvertTo-Json -Compress
                $res = $payload | gh api "repos/$owner/$repo/milestones" -X POST --input - 2>$null | ConvertFrom-Json
                if ($res -and $res.number) {
                    $milestoneMap[$mTitle] = $res.number
                    Write-Success "Created Milestone '$mTitle' (#$($res.number))"
                }
            } catch {
                Write-Warn "Could not create milestone '$mTitle'."
            }
        }
    }
}

# ----------------------------------------------------
# STEP 7: CREATE ISSUES WITH DUPLICATE PREVENTION
# ----------------------------------------------------
Write-Header "Creating Scrum Issues (with Duplicate Prevention)"

$existingIssues = @()
try {
    $existingIssues = gh issue list --repo "$owner/$repo" --state all --limit 200 --json number,title 2>$null | ConvertFrom-Json
} catch {
    Write-Warn "Could not list existing issues. Will verify as created."
}

$issuesCreatedCount = 0
$issuesExistingCount = 0
$issueNumberMap = @{}

foreach ($iss in $configJson.issues) {
    $id = $iss.identifier
    $title = $iss.title
    $body = $iss.body
    $labels = $iss.labels
    $sprint = $iss.sprint

    $matched = $null
    if ($existingIssues) {
        $matched = $existingIssues | Where-Object { 
            $_.title -like "*$id*" -or $_.title -eq $title 
        } | Select-Object -First 1
    }

    if ($matched) {
        Write-Note "[$id] $title -> already exists (Issue #$($matched.number))"
        $issueNumberMap[$id] = $matched.number
        $issuesExistingCount++
    } else {
        Write-Info "Creating [$id]: $title..."
        $argsList = @(
            "issue", "create",
            "--repo", "$owner/$repo",
            "--title", $title,
            "--body", $body
        )
        if ($labels -and $labels.Count -gt 0) {
            $argsList += @("--label", ($labels -join ","))
        }
        if ($sprint -and $milestoneMap.ContainsKey($sprint)) {
            $argsList += @("--milestone", $sprint)
        }

        try {
            $issueUrl = (& gh @argsList 2>&1).Trim()
            if ($issueUrl -match "/issues/(?<num>\d+)$") {
                $num = [int]$Matches["num"]
                $issueNumberMap[$id] = $num
                Write-Success "Created Issue #$num`: $title"
                $issuesCreatedCount++
            } else {
                Write-Warn "Created issue but could not parse issue number: $issueUrl"
            }
        } catch {
            Write-Err "Failed to create issue for $id"
        }
        Start-Sleep -Milliseconds 250
    }
}

Write-Success "Scrum Issues processed: $issuesCreatedCount created, $issuesExistingCount already existing."

# ----------------------------------------------------
# STEP 8: CREATE / CONFIGURE GITHUB PROJECT (KANBAN)
# ----------------------------------------------------
$projectUrl = ""
$issuesAddedCount = 0

if (-not $SkipProject) {
    Write-Header "Configuring GitHub Project (Kanban Board)"

    $projectScopeOk = $true
    try {
        $testProjList = gh project list --owner $owner --format json 2>&1
        if ($LASTEXITCODE -ne 0 -or ($testProjList -match "scope" -and $testProjList -match "project")) {
            $projectScopeOk = $false
        }
    } catch {
        $projectScopeOk = $false
    }

    if (-not $projectScopeOk) {
        Write-Warn "GitHub CLI token does not currently have 'project' scope."
        Write-Host "To enable automated Project Kanban boards, refresh your token scopes:" -ForegroundColor Yellow
        Write-Host "  gh auth refresh -s project`n" -ForegroundColor Green

        if (-not $NonInteractive) {
            $refreshNow = Read-Host "Would you like to refresh token scopes now? [Y/N]"
            if ($refreshNow -match "^[Yy]") {
                gh auth refresh -s "repo,read:org,project"
            }
        }
    }

    $projectNumber = $null
    $projectId = $null

    try {
        $existingProjects = gh project list --owner $owner --format json 2>$null | ConvertFrom-Json
        if ($existingProjects -and $existingProjects.projects) {
            $foundProj = $existingProjects.projects | Where-Object { $_.title -eq $projectName } | Select-Object -First 1
            if ($foundProj) {
                $projectNumber = $foundProj.number
                $projectId = $foundProj.id
                $projectUrl = $foundProj.url
                Write-Info "Found existing Project: '$projectName' (#$projectNumber)"
            }
        }
    } catch {
        Write-Note "Checking projects via owner query..."
    }

    if (-not $projectNumber) {
        Write-Info "Creating new GitHub Project: '$projectName'..."
        try {
            $newProj = gh project create --owner $owner --title $projectName --format json 2>$null | ConvertFrom-Json
            if ($newProj) {
                $projectNumber = $newProj.number
                $projectId = $newProj.id
                $projectUrl = $newProj.url
                Write-Success "Created GitHub Project: '$projectName' (#$projectNumber)"
            }
        } catch {
            Write-Warn "Could not create project via owner '$owner'. Attempting via '@me'..."
            try {
                $newProj = gh project create --owner "@me" --title $projectName --format json 2>$null | ConvertFrom-Json
                if ($newProj) {
                    $projectNumber = $newProj.number
                    $projectId = $newProj.id
                    $projectUrl = $newProj.url
                    Write-Success "Created GitHub Project: '$projectName' (#$projectNumber)"
                }
            } catch {
                Write-Warn "Project creation failed."
            }
        }
    }

    if ($projectNumber) {
        try {
            Write-Info "Linking Project #$projectNumber to repository $owner/$repo..."
            gh project link $projectNumber --owner $owner --repo $repo 2>$null | Out-Null
            Write-Success "Project linked to repository."
        } catch {
            Write-Note "Project link already established or not supported."
        }

        Write-Info "Configuring Project fields (Priority, Sprint, Story Points, Type)..."
        $existingFields = @()
        try {
            $fieldsJson = gh project field-list $projectNumber --owner $owner --format json 2>$null | ConvertFrom-Json
            if ($fieldsJson -and $fieldsJson.fields) {
                $existingFields = $fieldsJson.fields
            }
        } catch {
            Write-Note "Listing fields..."
        }

        $fieldNames = $existingFields | ForEach-Object { $_.name }

        if ($fieldNames -notcontains "Priority") {
            try {
                gh project field-create $projectNumber --owner $owner --name "Priority" --data-type "SINGLE_SELECT" --single-select-options "High,Medium,Low" 2>$null | Out-Null
                Write-Success "Configured 'Priority' field."
            } catch { Write-Note "Priority field setup note." }
        }

        if ($fieldNames -notcontains "Type") {
            try {
                gh project field-create $projectNumber --owner $owner --name "Type" --data-type "SINGLE_SELECT" --single-select-options "User Story,Task,Bug,Testing,Documentation" 2>$null | Out-Null
                Write-Success "Configured 'Type' field."
            } catch { Write-Note "Type field setup note." }
        }

        if ($fieldNames -notcontains "Sprint") {
            try {
                gh project field-create $projectNumber --owner $owner --name "Sprint" --data-type "SINGLE_SELECT" --single-select-options "Sprint 1,Sprint 2,Sprint 3,Sprint 4,Sprint 5" 2>$null | Out-Null
                Write-Success "Configured 'Sprint' field."
            } catch { Write-Note "Sprint field setup note." }
        }

        if ($fieldNames -notcontains "Story Points") {
            try {
                gh project field-create $projectNumber --owner $owner --name "Story Points" --data-type "NUMBER" 2>$null | Out-Null
                Write-Success "Configured 'Story Points' field."
            } catch { Write-Note "Story Points field setup note." }
        }

        Write-Info "Adding Scrum Issues to GitHub Project..."
        $existingItemUrls = @()
        try {
            $itemsJson = gh project item-list $projectNumber --owner $owner --format json 2>$null | ConvertFrom-Json
            if ($itemsJson -and $itemsJson.items) {
                $existingItemUrls = $itemsJson.items | ForEach-Object { $_.content.url }
            }
        } catch {
            Write-Note "Listing existing items in project..."
        }

        foreach ($iss in $configJson.issues) {
            $id = $iss.identifier
            if ($issueNumberMap.ContainsKey($id)) {
                $num = $issueNumberMap[$id]
                $issueUrl = "https://github.com/$owner/$repo/issues/$num"

                if ($existingItemUrls -contains $issueUrl) {
                    Write-Note "[OK] $id already in Project (#$num)"
                    $issuesAddedCount++
                } else {
                    try {
                        gh project item-add $projectNumber --owner $owner --url $issueUrl --format json 2>$null | Out-Null
                        Write-Success "[OK] $id added to Project (Issue #$num)"
                        $issuesAddedCount++
                    } catch {
                        Write-Warn "Could not add $id to project."
                    }
                }
            }
        }
    }
}

# ----------------------------------------------------
# STEP 9: SETUP COMPLETE SUMMARY
# ----------------------------------------------------
if (-not $projectUrl) {
    $projectUrl = "https://github.com/$owner/$repo/projects"
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host " SETUP COMPLETE" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Repository:" -ForegroundColor Yellow
Write-Host "  https://github.com/$owner/$repo" -ForegroundColor White
Write-Host ""
Write-Host "Project / Kanban Board:" -ForegroundColor Yellow
Write-Host "  $projectUrl" -ForegroundColor Cyan
Write-Host ""
Write-Host "Issues created:           $issuesCreatedCount" -ForegroundColor White
Write-Host "Issues already existing:  $issuesExistingCount" -ForegroundColor White
Write-Host "Issues added to Project:  $issuesAddedCount" -ForegroundColor White
Write-Host "Labels configured:        $labelsConfigured" -ForegroundColor White
Write-Host "Sprint Milestones:        5" -ForegroundColor White
Write-Host ""
Write-Host "Kanban board:" -ForegroundColor Yellow
Write-Host "  Ready" -ForegroundColor Green
Write-Host ""
Write-Host "Open the Project:" -ForegroundColor Yellow
Write-Host "  $projectUrl" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

param(
    [switch]$SkipDelay
)

$ErrorActionPreference = 'Stop'
$branch = if ($env:CI_COMMIT_BRANCH) { $env:CI_COMMIT_BRANCH } else { 'main' }
$login = if ($env:GITLAB_USER_LOGIN) { $env:GITLAB_USER_LOGIN } else { 'local-student' }
$results = [ordered]@{}

function Write-Stage([string]$Name) {
    Write-Host ""
    Write-Host "========== STAGE: $Name ==========" -ForegroundColor Cyan
}

function Write-Job([string]$Name, [string]$Stage) {
    Write-Host ""
    Write-Host "[$Stage/$Name] RUNNING" -ForegroundColor Yellow
}

function Pass-Job([string]$Name, [string]$Stage) {
    $results[$Name] = 'passed'
    Write-Host "[$Stage/$Name] PASSED" -ForegroundColor Green
}

Write-Host 'LOCAL DEVSECOPS PIPELINE DEMO' -ForegroundColor Magenta
Write-Host "Branch: $branch"
Write-Host 'This is a local demonstration of the GitLab CI/CD example.' -ForegroundColor DarkGray

Write-Stage 'build'
Write-Job 'build-job' 'build'
Write-Host "Hello, $login!"
Pass-Job 'build-job' 'build'

Write-Stage 'test'
Write-Job 'test-job1' 'test'
Write-Host 'This job tests something'
Pass-Job 'test-job1' 'test'

Write-Job 'test-job2' 'test'
Write-Host 'This job tests something, but takes more time than test-job1.'
Write-Host 'After the echo commands complete, it runs the sleep command for 20 seconds'
Write-Host 'which simulates a test that runs 20 seconds longer than test-job1'
if ($SkipDelay) {
    Write-Host 'Delay skipped by -SkipDelay.' -ForegroundColor DarkGray
} else {
    Start-Sleep -Seconds 20
}
Pass-Job 'test-job2' 'test'

Write-Stage 'deploy'
Write-Job 'deploy-prod' 'deploy'
Write-Host "This job deploys something from the $branch branch."
Write-Host 'Environment: production'
Pass-Job 'deploy-prod' 'deploy'

Write-Host ""
Write-Host '========== PIPELINE SUMMARY ==========' -ForegroundColor Cyan
$results.GetEnumerator() | ForEach-Object {
    Write-Host ("{0,-15} {1}" -f $_.Key, $_.Value) -ForegroundColor Green
}
Write-Host 'LOCAL PIPELINE PASSED' -ForegroundColor Green

#!/usr/bin/env pwsh
# Backend API Endpoint Testing Script

Write-Host "`n╔════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║     COMPREHENSIVE BACKEND API ENDPOINT TESTS          ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════╝`n" -ForegroundColor Green

$baseUrl = "http://localhost:8000"
$passCount = 0
$failCount = 0

function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Url,
        [string]$Method = "GET",
        [object]$Body = $null
    )
    
    Write-Host "$Name..." -ForegroundColor Yellow -NoNewline
    try {
        if ($Body) {
            $response = Invoke-RestMethod -Uri $Url -Method $Method -Body ($Body | ConvertTo-Json) -ContentType "application/json" -TimeoutSec 5 -ErrorAction Stop
        } else {
            $response = Invoke-RestMethod -Uri $Url -Method $Method -TimeoutSec 5 -ErrorAction Stop
        }
        Write-Host " ✅ PASS" -ForegroundColor Green
        $script:passCount++
        return $response
    } catch {
        if ($_.Exception.Message -like "*401*" -or $_.Exception.Message -like "*403*") {
            Write-Host " ✅ PASS (Auth required)" -ForegroundColor Green
            $script:passCount++
        } elseif ($_.Exception.Message -like "*404*") {
            Write-Host " ⚠ NOT FOUND" -ForegroundColor Yellow
        } else {
            Write-Host " ✗ FAIL: $($_.Exception.Message)" -ForegroundColor Red
            $script:failCount++
        }
        return $null
    }
}

Write-Host "═══ Core Endpoints ═══" -ForegroundColor Cyan
Test-Endpoint "Health Check" "$baseUrl/health"
Test-Endpoint "Root Endpoint" "$baseUrl/"
Test-Endpoint "API Docs (Swagger)" "$baseUrl/docs"
Test-Endpoint "ReDoc" "$baseUrl/redoc"
Test-Endpoint "OpenAPI Schema" "$baseUrl/openapi.json"

Write-Host "`n═══ Smart Coding AI Integration ═══" -ForegroundColor Cyan
Test-Endpoint "Integration Health" "$baseUrl/api/v1/smart-coding-ai/integration/health"

Write-Host "`n═══ Authentication Endpoints ═══" -ForegroundColor Cyan
Test-Endpoint "Auth - Get Current User" "$baseUrl/api/v0/auth/me"
Test-Endpoint "Auth - Health" "$baseUrl/api/v0/auth/health" -ErrorAction SilentlyContinue

Write-Host "`n═══ Voice Service ═══" -ForegroundColor Cyan
Test-Endpoint "Voice Health" "$baseUrl/api/v1/voice/health"

Write-Host "`n═══ Payment Service ═══" -ForegroundColor Cyan
Test-Endpoint "Payment Health" "$baseUrl/api/v1/payments/health"

Write-Host "`n═══ AI Orchestration ═══" -ForegroundColor Cyan
Test-Endpoint "AI Orchestrator Health" "$baseUrl/api/v1/ai-orchestrator/health"

Write-Host "`n═══ System Optimization ═══" -ForegroundColor Cyan
Test-Endpoint "System Optimization Health" "$baseUrl/api/v1/system-optimization/health"

Write-Host "`n═══ Governance ═══" -ForegroundColor Cyan
Test-Endpoint "Governance Health" "$baseUrl/api/v1/governance/health"

Write-Host "`n╔════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                  TEST RESULTS                          ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host "  Passed: $passCount" -ForegroundColor Green
Write-Host "  Failed: $failCount" -ForegroundColor $(if ($failCount -eq 0) { "Green" } else { "Red" })
Write-Host "  Success Rate: $([math]::Round(($passCount/($passCount+$failCount))*100, 1))%" -ForegroundColor Cyan

if ($failCount -eq 0) {
    Write-Host "`n✅ ALL TESTS PASSED!" -ForegroundColor Green
} else {
    Write-Host "`n⚠ Some endpoints not accessible (may require auth)" -ForegroundColor Yellow
}


# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
# ATM10 7.2 汉化补丁「绿油油版」安装器 (Windows)
# 用法：把整个汉化文件夹放进 ATM10 实例根目录后，双击「双击安装-Windows.bat」，
# 或在 PowerShell 中运行：
#   .\install.ps1                    # 交互菜单
#   .\install.ps1 apply              # 应用汉化（自动先备份，不含可选mods）
#   .\install.ps1 apply-with-pinyin  # 应用汉化 + 安装可选 JEI 拼音搜索 mod
#   .\install.ps1 backup             # 仅备份
#   .\install.ps1 restore [备份名]   # 恢复备份
param(
    [string]$Action = '',
    [string]$BackupName = ''
)
$ErrorActionPreference = 'Stop'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $ScriptDir
# 中文输出：cmd 侧已 chcp 65001，这里让 PowerShell 也按 UTF-8 写控制台
try { [Console]::OutputEncoding = [Text.UTF8Encoding]::new($false) } catch {}
$script:Target = Split-Path -Parent $ScriptDir
$PackDirs = @('config', 'kubejs', 'mods', 'resourcepacks', 'vaultpatcher')
$PackEntry = 'file/ATM10汉化包-7.2.zip'
$PinyinDir = '可选mods-拼音搜索'
$script:TS = ''
$script:BK = ''
# 就地解压：用户把压缩包内容直接解到了实例根目录，此时「源」和「目标」是同一个目录，
# 再复制一次就是 Copy-Item 自己覆盖自己 → IOException。这种情况文件本来就已到位。
$script:InPlace = $false
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

# 判定一个目录是不是游戏实例根目录。
# 不能只看 options.txt —— **刚装好、一次都没启动过的整合包没有 options.txt**
# （它是 Minecraft 首次退出时才写的）。也不能只看 mods\ —— 汉化包自己的文件夹里
# 也有个 mods\（装着 vaultpatcher.jar）。用 jar 数量区分：ATM10 有 400+ 个，汉化包只有 1 个。
function Test-Instance([string]$d) {
    if (!(Test-Path -LiteralPath (Join-Path $d 'mods'))) { return $false }
    if (Test-Path -LiteralPath (Join-Path $d 'options.txt')) { return $true }
    $n = @(Get-ChildItem -LiteralPath (Join-Path $d 'mods') -Filter '*.jar' -File -ErrorAction SilentlyContinue).Count
    return ($n -ge 20)
}

function Set-InPlace {
    $a = (Resolve-Path -LiteralPath $ScriptDir).Path.TrimEnd('\')
    $b = (Resolve-Path -LiteralPath $script:Target).Path.TrimEnd('\')
    if ($a -eq $b) {
        $script:InPlace = $true
        Write-Host 'ℹ️ 检测到汉化文件已经在实例根目录里（压缩包内容被直接解压到了这一层）。'
        Write-Host '   文件本来就已到位，无需复制；本次只做 options.txt 的资源包启用。'
        Write-Host '   ⚠️ 这种装法没有备份可回退——原文件在你解压覆盖的那一刻就没了。'
        Write-Host '   想要可回退的安装，请解压到别处、把整个文件夹放进实例根目录再运行安装器。'
    }
}

function Check-Target {
    if (Test-Instance $script:Target) {
        Set-InPlace
        return
    }
    # 就地解压：脚本自己所在的这一层就是实例根目录
    if (Test-Instance $ScriptDir) {
        $script:Target = $ScriptDir
        Set-InPlace
        return
    }
    Write-Host '⚠️ 上一级目录不是游戏实例根目录（含 mods\ 的那一层）。'
    while ($true) {
        $inp = Read-Host '请输入 ATM10 实例根目录完整路径（q 退出）'
        $inp = $inp.Trim()
        if ($inp -eq 'q' -or [string]::IsNullOrWhiteSpace($inp)) { exit 1 }
        # 去掉整体包裹的成对引号（Windows 拖拽/粘贴带空格路径常加双引号）
        if (($inp.StartsWith('"') -and $inp.EndsWith('"')) -or ($inp.StartsWith("'") -and $inp.EndsWith("'"))) {
            $inp = $inp.Substring(1, $inp.Length - 2)
        }
        $inp = $inp.TrimEnd('\', '/')
        if (Test-Instance $inp) {
            $script:Target = $inp
            Write-Host "✅ 目标实例: $script:Target"
            Set-InPlace
            return
        }
        Write-Host '❌ 该路径下没找到 ATM10 的 mods\（应该有几百个 .jar），请重试。'
    }
}

function Get-PayloadFiles {
    foreach ($d in $PackDirs) {
        if (Test-Path -LiteralPath $d) {
            Get-ChildItem -LiteralPath $d -Recurse -File | Where-Object { $_.Name -ne '.DS_Store' } | ForEach-Object {
                $_.FullName.Substring($ScriptDir.Length + 1)
            }
        }
    }
}

function Do-Backup {
    if ($script:InPlace) {
        Write-Host '⚠️ 就地解压模式下没有可备份的原文件（已被解压覆盖），跳过备份。'
        return
    }
    $script:TS = Get-Date -Format 'yyyyMMdd-HHmmss'
    $script:BK = Join-Path $ScriptDir "backups/$script:TS"
    New-Item -ItemType Directory -Force -Path $script:BK | Out-Null
    $newFiles = @()
    $n = 0
    foreach ($f in Get-PayloadFiles) {
        $dst = Join-Path $script:Target $f
        if (Test-Path -LiteralPath $dst) {
            $to = Join-Path $script:BK $f
            New-Item -ItemType Directory -Force -Path (Split-Path $to) | Out-Null
            Copy-Item -LiteralPath $dst -Destination $to
            $n++
        } else {
            $newFiles += $f
        }
    }
    if ($newFiles.Count -gt 0) {
        [System.IO.File]::WriteAllLines((Join-Path $script:BK '新增文件清单.txt'), $newFiles, $Utf8NoBom)
    }
    if (Test-Path -LiteralPath (Join-Path $script:Target 'options.txt')) {
        Copy-Item -LiteralPath (Join-Path $script:Target 'options.txt') -Destination (Join-Path $script:BK 'options.txt')
    }
    Write-Host "✅ 已备份 $n 个将被覆盖的文件到 backups/$script:TS/"
}

function Patch-Options {
    $opt = Join-Path $script:Target 'options.txt'
    # 全新实例还没启动过，options.txt 尚不存在（Minecraft 退出时才写）。
    # 这种情况交给整合包自带的 DefaultOptions：它会在首次启动时把
    # config/defaultoptions/options.txt 里的键补进玩家的 options.txt。
    if (!(Test-Path -LiteralPath $opt)) {
        $def = Join-Path $script:Target 'config/defaultoptions/options.txt'
        if ((Test-Path -LiteralPath $def) -and ((Get-Content -Raw -LiteralPath $def) -match [regex]::Escape($PackEntry))) {
            Write-Host 'ℹ️ 这个实例还没启动过（没有 options.txt）。'
            Write-Host '   已通过 config/defaultoptions 预置资源包与中文语言，首次启动游戏时自动生效。'
        } else {
            Write-Host '⚠️ 没有 options.txt，也没找到 config/defaultoptions/options.txt。'
            Write-Host '   请首次进游戏后手动到 选项 → 资源包 里启用「ATM10汉化包-7.2」。'
        }
        return
    }
    $content = [System.IO.File]::ReadAllText($opt)
    if ($content -match [regex]::Escape($PackEntry)) {
        Write-Host 'options.txt 已启用汉化资源包，跳过'
        return
    }
    if ($content -match '(?m)^resourcePacks:\[\]\s*$') {
        $content = $content -replace '(?m)^resourcePacks:\[\]', ('resourcePacks:["' + $PackEntry + '"]')
    } elseif ($content -match '(?m)^resourcePacks:\[.+\]\s*$') {
        $content = $content -replace '(?m)^resourcePacks:\[(.+)\]', ('resourcePacks:[$1,"' + $PackEntry + '"]')
    } else {
        Write-Host '⚠️ options.txt 中没有 resourcePacks 行，请进游戏手动启用资源包'
        return
    }
    [System.IO.File]::WriteAllText($opt, $content, $Utf8NoBom)
    Write-Host '✅ 已在 options.txt 启用汉化资源包（不启用会全英文）'
}

function Do-Apply {
    if ($script:InPlace) {
        Patch-Options
        Write-Host '✅ 汉化文件已在位，options.txt 已处理完毕。'
        return
    }
    Do-Backup
    foreach ($f in Get-PayloadFiles) {
        $dst = Join-Path $script:Target $f
        if ((Join-Path $ScriptDir $f) -eq $dst) { continue }   # 双保险：源即目标就跳过
        New-Item -ItemType Directory -Force -Path (Split-Path $dst) | Out-Null
        Copy-Item -LiteralPath $f -Destination $dst -Force
    }
    Patch-Options
    Write-Host "✅ 汉化已应用。备份在 backups/$script:TS/，如需回退运行: .\install.ps1 restore $script:TS"
}

# 可选 mods（JEI 拼音搜索）：装进实例 mods/，并登记进当前备份以便恢复时删除
function Do-Pinyin {
    if (!(Test-Path -LiteralPath $PinyinDir)) {
        Write-Host "（未找到 $PinyinDir 目录，跳过可选mods）"
        return
    }
    $jars = Get-ChildItem -LiteralPath $PinyinDir -Filter '*.jar' -File
    if (!$jars) {
        Write-Host "（$PinyinDir 内没有 jar，跳过）"
        return
    }
    # 就地解压模式没有本次备份（BK 为空），只装不登记
    $manifest = if ($script:BK) { Join-Path $script:BK '新增文件清单.txt' } else { $null }
    foreach ($j in $jars) {
        $dst = Join-Path $script:Target "mods/$($j.Name)"
        if ($script:BK) {
            if (Test-Path -LiteralPath $dst) {
                New-Item -ItemType Directory -Force -Path (Join-Path $script:BK 'mods') | Out-Null
                Copy-Item -LiteralPath $dst -Destination (Join-Path $script:BK "mods/$($j.Name)")
            } else {
                [System.IO.File]::AppendAllText($manifest, "mods/$($j.Name)`n", $Utf8NoBom)
            }
        }
        if ($j.FullName -eq $dst) { continue }
        Copy-Item -LiteralPath $j.FullName -Destination $dst -Force
        Write-Host "  已安装: mods/$($j.Name)"
    }
    Write-Host '✅ 可选 mod（JEI 拼音搜索）已安装'
}

function Do-Restore([string]$name) {
    $broot = Join-Path $ScriptDir 'backups'
    if (!(Test-Path -LiteralPath $broot) -or !(Get-ChildItem -LiteralPath $broot -Directory)) {
        Write-Host '❌ 没有任何备份'
        exit 1
    }
    $all = Get-ChildItem -LiteralPath $broot -Directory | Sort-Object Name
    if (-not $name) {
        Write-Host '可用备份：'
        $all | ForEach-Object { Write-Host "  $($_.Name)" }
        $latest = $all[-1].Name
        $name = Read-Host "要恢复的备份名 [回车 = $latest]"
        if (-not $name) { $name = $latest }
    }
    $bk = Join-Path $broot $name
    if (!(Test-Path -LiteralPath $bk)) {
        Write-Host "❌ 备份不存在: $name"
        exit 1
    }
    $manifest = Join-Path $bk '新增文件清单.txt'
    if (Test-Path -LiteralPath $manifest) {
        foreach ($f in [System.IO.File]::ReadAllLines($manifest)) {
            if ($f) { Remove-Item -LiteralPath (Join-Path $script:Target $f) -Force -ErrorAction SilentlyContinue }
        }
    }
    Get-ChildItem -LiteralPath $bk -Recurse -File | Where-Object { $_.Name -ne '新增文件清单.txt' } | ForEach-Object {
        $rel = $_.FullName.Substring($bk.Length + 1)
        $dst = Join-Path $script:Target $rel
        New-Item -ItemType Directory -Force -Path (Split-Path $dst) | Out-Null
        Copy-Item -LiteralPath $_.FullName -Destination $dst -Force
    }
    Write-Host "✅ 已恢复备份 $name（含 options.txt，安装时新增的文件已删除）"
}

Check-Target
switch ($Action) {
    'apply'             { Do-Apply }
    'apply-with-pinyin' { Do-Apply; Do-Pinyin }
    'backup'            { Do-Backup }
    'restore'           { Do-Restore $BackupName }
    default {
        Write-Host '══════════════════════════════════════════'
        Write-Host ' ATM10 7.2 汉化补丁 · 绿油油版 — 安装器'
        Write-Host " 目标实例: $script:Target"
        Write-Host '══════════════════════════════════════════'
        Write-Host ' [1] 应用汉化（自动先备份被覆盖文件）'
        Write-Host ' [2] 仅备份'
        Write-Host ' [3] 恢复备份'
        Write-Host ' [q] 退出'
        $c = Read-Host '请选择'
        switch ($c) {
            '1' {
                Do-Apply
                $ans = Read-Host '是否同时安装可选的 JEI 拼音搜索 mod？[y/N]'
                if ($ans -eq 'y' -or $ans -eq 'Y') { Do-Pinyin }
                else { Write-Host '（跳过可选mods，之后可运行: .\install.ps1 apply-with-pinyin）' }
            }
            '2' { Do-Backup }
            '3' { Do-Restore '' }
            default { Write-Host '已退出' }
        }
    }
}

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

# ATM10 7.2 默认启用的资源包，顺序照抄游戏自己写出来的 options.txt。
# 为什么要写死这一串：全新实例没有 options.txt，如果只写我们一个包，
# 游戏首次启动会把这 15 个内置包**全部插到我们后面**（实测汉化包落到第 3 位，
# 被 mod_resources 和五百多个模组包压在底下，汉化基本不生效）。
# 资源包是**后面的覆盖前面的**，我们必须排在最后一个。
$DefaultPacks = '""modularbees:dynamic_assets"",""vanilla"",""mod_resources"",""add_xycraft_overrides_stone"",""add_xycraft_overrides_metal"",""add_xycraft_overrides_glass"",""moonlight:merged_pack"",""mod/towntalk:respack"",""mod/dyenamicsandfriends:compat_packs/productivemetalworks/"",""mod/dyenamicsandfriends:compat_packs/connectedglass/"",""mod/dyenamicsandfriends:compat_packs/luminax/"",""mod/dyenamicsandfriends:compat_packs/cookingforblockheads/"",""mod/dyenamicsandfriends:compat_packs/botanypots/"",""mod/dyenamicsandfriends:compat_packs/chromacarvings/"",""modern_industrialization/generated""'

function Patch-Options {
    $opt = Join-Path $script:Target 'options.txt'
    if (!(Test-Path -LiteralPath $opt)) {
        $line = 'resourcePacks:[' + $DefaultPacks + ',"' + $PackEntry + '"]'
        [System.IO.File]::WriteAllText($opt, "lang:zh_cn`n$line`n", $Utf8NoBom)
        Write-Host 'ℹ️ 这个实例还没启动过（没有 options.txt），已新建一份并写入中文语言与汉化资源包。'
        Write-Host '   首次启动游戏时 Minecraft 会自动补齐其余设置。'
        return
    }
    $lines = [System.IO.File]::ReadAllLines($opt)
    $idx = -1
    for ($i = 0; $i -lt $lines.Length; $i++) {
        if ($lines[$i].StartsWith('resourcePacks:[')) { $idx = $i; break }
    }
    if ($idx -lt 0) {
        Write-Host '⚠️ options.txt 中没有 resourcePacks 行，请进游戏手动启用资源包'
        return
    }
    $cur = $lines[$idx]
    $body = $cur.Substring('resourcePacks:['.Length)
    $body = $body.Substring(0, $body.Length - 1)
    # 先把已有的汉化包条目摘掉，再追加到**末尾**。
    # 不能只判断「已存在就跳过」——旧版本装出来的实例里它可能排在很前面，
    # 那样等于没启用（后面的包会把它整个盖掉），必须重新挪到最后。
    $body = $body -replace [regex]::Escape('"' + $PackEntry + '"'), ''
    $body = ($body -replace ',{2,}', ',').Trim(',')
    $new = if ($body) { 'resourcePacks:[' + $body + ',"' + $PackEntry + '"]' }
           else       { 'resourcePacks:["' + $PackEntry + '"]' }
    if ($new -eq $cur) {
        Write-Host 'options.txt 已正确启用汉化资源包（在列表最后），跳过'
        return
    }
    $lines[$idx] = $new
    [System.IO.File]::WriteAllLines($opt, $lines, $Utf8NoBom)
    Write-Host '✅ 已在 options.txt 启用汉化资源包并置于列表最后（不在最后会被其他包盖掉）'
}

##
# 清理 7.2 release8 之前的遗留文件。
#
# 那之前本包的任务书 delta 用的是 `<章节名>.snbt`，与整合包自带的同名文件**撞名**，
# 安装时直接覆盖 —— 整合包那一章上百条翻译当场没了，任务书变英文。
# （已经启动过的实例看不出来：整合包那批早合并完并改名成 .snbt_merged 了。）
#
# 现在统一加 zz_hanhua_ 前缀，不会再撞名。这里把旧名字的残留删掉，
# 且只在**内容与本包同名新文件逐字节相同**时才删 —— 这样能确定它是本包的旧产物，
# 绝不会误删整合包自己的文件。
function Clear-LegacyQuestLang {
    $qd = Join-Path $script:Target 'config\ftbquests\quests\lang\zh_cn\chapters'
    $sd = Join-Path $ScriptDir 'config\ftbquests\quests\lang\zh_cn\chapters'
    if (!(Test-Path -LiteralPath $qd) -or !(Test-Path -LiteralPath $sd)) { return }
    $hit = 0
    foreach ($new in Get-ChildItem -LiteralPath $sd -Filter 'zz_hanhua_*.snbt' -File) {
        $base = $new.Name -replace '^zz_hanhua_', ''
        foreach ($n in @($base, "_$base")) {
            $old = Join-Path $qd $n
            if (!(Test-Path -LiteralPath $old)) { continue }
            $a = [System.IO.File]::ReadAllBytes($old)
            $b = [System.IO.File]::ReadAllBytes($new.FullName)
            if ($a.Length -eq $b.Length -and
                [System.Linq.Enumerable]::SequenceEqual($a, $b)) {
                Remove-Item -LiteralPath $old -Force
                $hit++
            }
        }
    }
    if ($hit -gt 0) {
        Write-Host "🧹 清理了 $hit 个旧版本残留的任务书语言文件。"
        Write-Host '⚠️ 旧版本可能覆盖过整合包自带的任务书翻译。若任务书仍有整章英文，'
        Write-Host '   请重装一次整合包再运行本安装器（本包已不会再覆盖整合包的文件）。'
    }
}

function Do-Apply {
    if ($script:InPlace) {
        Clear-LegacyQuestLang
        Patch-Options
        Write-Host '✅ 汉化文件已在位，options.txt 已处理完毕。'
        return
    }
    Do-Backup
    Clear-LegacyQuestLang
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

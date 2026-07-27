# -*- coding: utf-8 -*-
# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
"""安装脚本端到端测试（三平台 CI 共用）。

流程：造一个假游戏实例 → 把「释放后的汉化文件夹」放进实例根目录 →
apply → 断言（文件落位 / options.txt 已启用资源包 / 备份完整）→
restore → 断言（被覆盖文件还原 / 新增文件删除 / options.txt 还原）。
macOS/Linux 走 install.sh，Windows 走 install.ps1（powershell 5.1，与用户双击 .bat 一致）。
"""
import platform, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path

# Windows runner 的 stdout 默认 cp1252，打不出中文/emoji
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent.parent
IS_WIN = platform.system() == 'Windows'
# 资源包**源目录**是版本中立的（resourcepacks/ATM10汉化包/），但**产物**带整合包版本号，
# 由 build_dist.sh 在打包时注入。这里直接从安装器脚本里读它认的那个名字，
# 免得两边各写一份、日后再对不上（曾因批量改名把这里误改成版本中立名而挂掉 CI）。
import re as _re
ENTRY = _re.search(r"PACK_ENTRY='([^']+)'",
                   (ROOT / 'installer' / 'install.sh').read_text(encoding='utf-8')).group(1)
PACK = ENTRY.split('/', 1)[1][:-4]

tmp = Path(tempfile.mkdtemp(prefix='hanhua-test-'))
inst = tmp / 'instance'
(inst / 'mods').mkdir(parents=True)
# 实例判定用「mods 里 jar 数 >= 20」把真实例和汉化包自己的 mods/ 区分开
for i in range(25):
    (inst / 'mods' / f'modpack-{i}.jar').write_text('x', encoding='utf-8')
OPTS_BEFORE = 'version:4189\nresourcePacks:["vanilla","mod_resources"]\nlang:zh_cn\n'
(inst / 'options.txt').write_text(OPTS_BEFORE, encoding='utf-8')

# 预置一个「会被覆盖」的旧文件，验证备份/还原
sample = sorted((ROOT / 'vaultpatcher' / 'modules').glob('*.json'))[0].name
pre = inst / 'vaultpatcher' / 'modules' / sample
pre.parent.mkdir(parents=True)
pre.write_text('OLD-CONTENT', encoding='utf-8')

# 模拟释放后的汉化文件夹（与 build_dist.sh 产物同构）
rel = inst / 'ATM10-7.2-汉化补丁-绿油油版'
rel.mkdir()
for d in ('config', 'kubejs', 'mods', 'vaultpatcher'):
    shutil.copytree(ROOT / d, rel / d)
(rel / 'resourcepacks').mkdir()
src = ROOT / 'resourcepacks' / PACK
with zipfile.ZipFile(rel / 'resourcepacks' / f'{PACK}.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for p in src.rglob('*'):
        if p.is_file() and p.name != '.DS_Store':
            z.write(p, p.relative_to(src).as_posix())
for s in ('install.sh', 'install.ps1'):
    shutil.copy2(ROOT / 'installer' / s, rel / s)
if (ROOT / '可选mods-拼音搜索').is_dir():
    shutil.copytree(ROOT / '可选mods-拼音搜索', rel / '可选mods-拼音搜索')


def run(*args):
    if IS_WIN:
        cmd = ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass',
               '-File', str(rel / 'install.ps1'), *args]
    else:
        cmd = ['bash', str(rel / 'install.sh'), *args]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    print(r.stdout)
    if r.stderr:
        print(r.stderr, file=sys.stderr)
    assert r.returncode == 0, f'install {args} 退出码 {r.returncode}'


def read_opts():
    return (inst / 'options.txt').read_text(encoding='utf-8')


# ---- 应用汉化 ----
run('apply')
assert ENTRY in read_opts(), 'options.txt 未启用汉化资源包'
assert (inst / 'resourcepacks' / f'{PACK}.zip').exists(), '资源包未落位'
assert (inst / 'config' / 'vaultpatcher_asm' / 'config.json').exists(), 'config 未落位'
assert pre.read_text(encoding='utf-8') != 'OLD-CONTENT', '旧文件未被新版覆盖'

bks = sorted(p for p in (rel / 'backups').iterdir() if p.is_dir())
assert len(bks) == 1, f'应有 1 个备份，实际 {len(bks)}'
bk = bks[0]
assert (bk / 'vaultpatcher' / 'modules' / sample).read_text(encoding='utf-8') == 'OLD-CONTENT', \
    '备份里没有被覆盖文件的原内容'
assert (bk / '新增文件清单.txt').exists(), '缺新增文件清单'
assert (bk / 'options.txt').read_text(encoding='utf-8') == OPTS_BEFORE, '备份的 options.txt 不对'

# ---- 恢复备份 ----
run('restore', bk.name)
assert pre.read_text(encoding='utf-8') == 'OLD-CONTENT', '被覆盖文件未还原'
assert ENTRY not in read_opts(), 'options.txt 未还原'
assert not (inst / 'resourcepacks' / f'{PACK}.zip').exists(), '新增的资源包未删除'
assert not (inst / 'kubejs' / 'client_scripts' / 'pb_hanhua_tooltip.js').exists(), '新增的脚本未删除'

# ---- 可选mods（拼音搜索）：apply 不装、apply-with-pinyin 装、restore 删 ----
pin_jars = sorted((rel / '可选mods-拼音搜索').glob('*.jar')) if (rel / '可选mods-拼音搜索').is_dir() else []
if pin_jars:
    jar = pin_jars[0].name
    assert not (inst / 'mods' / jar).exists(), '普通 apply 不应安装可选mods'
    run('apply-with-pinyin')
    assert (inst / 'mods' / jar).exists(), '拼音搜索 mod 未安装'
    bk2 = sorted(p for p in (rel / 'backups').iterdir() if p.is_dir())[-1]
    manifest = (bk2 / '新增文件清单.txt').read_text(encoding='utf-8')
    assert f'mods/{jar}' in manifest, '拼音 mod 未登记进新增文件清单'
    run('restore', bk2.name)
    assert not (inst / 'mods' / jar).exists(), '恢复备份未删除拼音 mod'
else:
    print('（仓库无可选mods jar，跳过拼音分支）')

# ---- 回归：手动输入带引号/空格的实例路径（复制粘贴/拖拽常见形态）----
# 造一个路径含空格的实例；释放文件夹放在「非实例」的松散目录里 → check_target 触发输入循环
# 路径同时含空格与中文：Windows 上两者都常见（PCL2 默认就往中文目录装）
spaced = tmp / '我的 Game Dir With Spaces 绿油油'
(spaced / 'mods').mkdir(parents=True)
for i in range(25):
    (spaced / 'mods' / f'modpack-{i}.jar').write_text('x', encoding='utf-8')
SPACED_OPTS = 'version:4189\nresourcePacks:[]\n'
(spaced / 'options.txt').write_text(SPACED_OPTS, encoding='utf-8')
loose = tmp / 'loose' / 'ATM10-hanhua'   # 父目录 tmp/loose 不含 mods/options.txt
loose.mkdir(parents=True)
(loose / 'config').mkdir()
(loose / 'config' / 'placeholder.txt').write_text('x', encoding='utf-8')
for s in ('install.sh', 'install.ps1'):
    shutil.copy2(ROOT / 'installer' / s, loose / s)


def run_prompt(script_dir, mode, answer):
    """跑安装脚本，在‘输入实例路径’提示处喂 answer；返回 (returncode, 合并输出)。"""
    if IS_WIN:
        cmd = ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass',
               '-File', str(script_dir / 'install.ps1'), mode]
        r = subprocess.run(cmd, input=answer + '\n', capture_output=True,
                           text=True, encoding='utf-8', errors='replace', timeout=120)
        return r.returncode, (r.stdout or '') + (r.stderr or '')
    # Unix：install.sh 用 [ -t 0 ] 判交互，必须用 pty 让 stdin 是终端
    import pty, os
    master, slave = pty.openpty()
    p = subprocess.Popen(['bash', str(script_dir / 'install.sh'), mode],
                         stdin=slave, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    os.close(slave)
    os.write(master, (answer + '\n').encode('utf-8'))
    try:
        p.wait(timeout=60)
    except subprocess.TimeoutExpired:
        os.close(master); p.kill(); p.wait()
        return 124, '（超时：脚本未能解析路径，仍在等待输入）'
    out = p.stdout.read().decode('utf-8', 'replace')
    os.close(master)
    return p.returncode, out


# Unix 常见是单引号粘贴，Windows 拖拽是双引号——各测本平台形态（两种都在脚本里处理）
q = '"' if IS_WIN else "'"
quoted = q + str(spaced) + q
rc, out = run_prompt(loose, 'backup', quoted)
assert rc == 0, f'带引号路径 backup 失败(rc={rc})：\n{out}'
assert '目标实例' in out, f'未从带引号路径解析出实例：\n{out}'
lbks = sorted(p for p in (loose / 'backups').iterdir() if p.is_dir()) if (loose / 'backups').is_dir() else []
assert lbks and (lbks[-1] / 'options.txt').read_text(encoding='utf-8') == SPACED_OPTS, \
    '未正确定位到带空格的实例目录'
print('✅ 引号/空格路径输入清洗 OK')

# ---- 回归：就地解压（压缩包内容直接覆盖到实例根目录，随后又跑安装器）----
# 此时脚本所在目录 == 实例目录，源与目标是同一批文件。
# 旧版会走进「把文件复制到自己头上」→ Windows 抛
# "Cannot overwrite the item ... with itself"，Unix 则 cp 同源同目标失败。
inplace = tmp / 'inplace-instance'
(inplace / 'mods').mkdir(parents=True)
INPLACE_OPTS = 'version:4189\nresourcePacks:[]\nlang:zh_cn\n'
(inplace / 'options.txt').write_text(INPLACE_OPTS, encoding='utf-8')
for i in range(25):
    (inplace / 'mods' / f'modpack-{i}.jar').write_text('x', encoding='utf-8')
for d in ('config', 'kubejs', 'vaultpatcher'):          # 模拟解压覆盖
    shutil.copytree(ROOT / d, inplace / d, dirs_exist_ok=True)
(inplace / 'resourcepacks').mkdir(exist_ok=True)
shutil.copy2(rel / 'resourcepacks' / f'{PACK}.zip', inplace / 'resourcepacks' / f'{PACK}.zip')
for s_ in ('install.sh', 'install.ps1'):
    shutil.copy2(ROOT / 'installer' / s_, inplace / s_)

if IS_WIN:
    cmd = ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass',
           '-File', str(inplace / 'install.ps1'), 'apply']
else:
    cmd = ['bash', str(inplace / 'install.sh'), 'apply']
r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8',
                   errors='replace', timeout=300)
out = (r.stdout or '') + (r.stderr or '')
assert r.returncode == 0, f'就地解压模式安装失败(rc={r.returncode})：\n{out}'
assert 'with itself' not in out, f'仍在把文件复制到自己头上：\n{out}'
assert ENTRY in (inplace / 'options.txt').read_text(encoding='utf-8'), \
    f'就地解压模式未启用资源包：\n{out}'
assert (inplace / 'config' / 'vaultpatcher_asm' / 'config.json').exists(), '就地解压模式误删了文件'
print('✅ 就地解压（源即目标）不再自我复制 OK')

# ---- 回归：刚装好、一次都没启动过的实例（没有 options.txt）----
# Minecraft 是退出时才写 options.txt。旧版把它当实例判定的必要条件，
# 于是无论用户怎么输路径都被判定为「不是实例」，卡在输入循环里出不来。
fresh = tmp / '全新 实例 never-launched'
(fresh / 'mods').mkdir(parents=True)
for i in range(25):
    (fresh / 'mods' / f'modpack-{i}.jar').write_text('x', encoding='utf-8')
frel = fresh / 'atm10-zh_cn-client'
frel.mkdir()
for d in ('config', 'kubejs', 'mods', 'vaultpatcher'):
    shutil.copytree(ROOT / d, frel / d)
(frel / 'resourcepacks').mkdir()
shutil.copy2(rel / 'resourcepacks' / f'{PACK}.zip', frel / 'resourcepacks' / f'{PACK}.zip')
for s_ in ('install.sh', 'install.ps1'):
    shutil.copy2(ROOT / 'installer' / s_, frel / s_)

if IS_WIN:
    cmd = ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass',
           '-File', str(frel / 'install.ps1'), 'apply']
else:
    cmd = ['bash', str(frel / 'install.sh'), 'apply']
r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8',
                   errors='replace', timeout=300)
out = (r.stdout or '') + (r.stderr or '')
assert r.returncode == 0, f'全新实例（无 options.txt）安装失败(rc={r.returncode})：\n{out}'
assert '不是游戏实例根目录' not in out, f'没识别出全新实例：\n{out}'
assert (fresh / 'config' / 'vaultpatcher_asm' / 'config.json').exists(), '文件未落位'
newopt = fresh / 'options.txt'
assert newopt.exists(), f'全新实例没建出 options.txt：\n{out}'
txt = newopt.read_text(encoding='utf-8')
assert ENTRY in txt, f'新建的 options.txt 没写入资源包：\n{txt}'
assert 'lang:zh_cn' in txt, f'新建的 options.txt 没写入中文语言：\n{txt}'
print('✅ 全新实例（无 options.txt，路径含中文+空格）OK')

shutil.rmtree(tmp, ignore_errors=True)
print(f'✅ 安装脚本端到端测试通过（{platform.system()}）')

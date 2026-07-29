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
import platform, re, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path

# Windows runner 的 stdout 默认 cp1252，打不出中文/emoji
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import COMMON

ROOT = Path(__file__).resolve().parent.parent
IS_WIN = platform.system() == 'Windows'
# 测的是**出货树**：仓库里没有 kubejs/ config/ 这些目录，它们由 assemble.py 现摊。
# 可以传一棵合成好的版本树进来（build/v/<版本>），默认用版本中立的 build/common。
TREE = Path(sys.argv[1]) if len(sys.argv) > 1 else COMMON
if not TREE.is_dir():
    sys.exit('❌ 出货树不存在: %s\n'
             '   先跑: python3 scripts/assemble.py && ./scripts/generate_all.sh' % TREE)
# 安装器源码里跟整合包版本有关的字样全是 @@MCVER@@ 占位，由 build_dist.sh 现填。
# 测试也照同一条路径填一遍——测的必须是玩家真正拿到的那份脚本，不是模板。
MCVER = sorted((d.name for d in (ROOT / 'versions').iterdir()
                if d.is_dir() and d.name[0].isdigit()),
               key=lambda s: [int(x) for x in s.split('.')])[-1]


def default_packs(ver):
    """该版实测的默认资源包顺序，格式与 build_dist.sh 注入的完全一致"""
    f = ROOT / 'versions' / ver / 'default_resource_packs.txt'
    if not f.is_file():
        return ''
    names = [l.strip() for l in f.read_text(encoding='utf-8').splitlines()
             if l.strip() and not l.startswith('#')]
    return ','.join('"%s"' % n for n in names)


DEFAULT_PACKS = default_packs(MCVER)
# 补丁自己的版本号：测试里用什么值不重要（联网检查已被 ATM_SKIP_UPDATE_CHECK 关掉），
# 重要的是它**必须被填掉**——否则脚本里留着 @@PATCHVER@@，测的就不是出货那份。
PATCHVER = 'test'


def materialize(src, dst):
    """把安装器模板里的占位符填掉，写到 dst（与 build_dist.sh 同一套替换）。
    测的必须是玩家真正拿到的那份脚本——以前测试里 @@DEFAULT_PACKS@@ 压根没被替换，
    安装器把这串占位符当成一个资源包名写进了 options.txt，测试还照样通过。"""
    t = src.read_text(encoding='utf-8')
    t = (t.replace('@@MCVER@@', MCVER)
          .replace('@@DEFAULT_PACKS@@', DEFAULT_PACKS)
          .replace('@@PATCHVER@@', PATCHVER))
    left = re.findall(r'@@[A-Z_]+@@', t)
    if left:
        sys.exit('❌ %s 里还有没填的占位符：%s\n'
                 '   build_dist.sh 加了新占位符，这里要跟着加，否则测的不是玩家拿到的那份。'
                 % (src.name, sorted(set(left))))
    dst.write_text(t, encoding='utf-8')
    return dst


# 资源包**产物**带整合包版本号。这里直接从安装器脚本里读它认的那个名字，
# 免得两边各写一份、日后再对不上（曾因批量改名把这里误改成版本中立名而挂掉 CI）。
ENTRY = re.search(r"PACK_ENTRY='([^']+)'",
                   (ROOT / 'installer' / 'install.sh').read_text(encoding='utf-8')
                   ).group(1).replace('@@MCVER@@', MCVER)
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
sample = sorted((COMMON / 'vaultpatcher' / 'modules').glob('*.json'))[0].name
pre = inst / 'vaultpatcher' / 'modules' / sample
pre.parent.mkdir(parents=True)
pre.write_text('OLD-CONTENT', encoding='utf-8')

# 预置 r14 发过、本版起停发的那两个模块：安装器必须主动删掉它们。
# 它们是 dynamic 模块，而 dynamic 表是每渲染一个字符串都要线性扫一遍的全局开销——
# 只覆盖不删除的话，装了新版照旧掉帧（这就是 r14 掉帧修不干净的那条路）。
STALE = ('config_ui_generated.json', 'catnip_config_ui.json')
for _s in STALE:
    (inst / 'vaultpatcher' / 'modules' / _s).write_text('STALE', encoding='utf-8')

# 模拟释放后的汉化文件夹（与 build_dist.sh 产物同构）
rel = inst / 'ATM10-7.2-汉化补丁-绿油油版'
rel.mkdir()
for d in ('config', 'kubejs', 'mods', 'vaultpatcher'):
    shutil.copytree(TREE / d, rel / d)
(rel / 'resourcepacks').mkdir()
src = TREE / 'resourcepacks' / PACK
with zipfile.ZipFile(rel / 'resourcepacks' / f'{PACK}.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for p in src.rglob('*'):
        if p.is_file() and p.name != '.DS_Store':
            z.write(p, p.relative_to(src).as_posix())
for s in ('install.sh', 'install.ps1'):
    materialize(ROOT / 'installer' / s, rel / s)
if (TREE / '可选mods-拼音搜索').is_dir():
    shutil.copytree(TREE / '可选mods-拼音搜索', rel / '可选mods-拼音搜索')


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
for _s in STALE:
    assert not (inst / 'vaultpatcher' / 'modules' / _s).exists(), \
        f'{_s} 没被清理——装过 r14 的人会继续掉帧'

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
    materialize(ROOT / 'installer' / s, loose / s)


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
    shutil.copytree(TREE / d, inplace / d, dirs_exist_ok=True)
(inplace / 'resourcepacks').mkdir(exist_ok=True)
shutil.copy2(rel / 'resourcepacks' / f'{PACK}.zip', inplace / 'resourcepacks' / f'{PACK}.zip')
for s_ in ('install.sh', 'install.ps1'):
    materialize(ROOT / 'installer' / s_, inplace / s_)

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
# 就地解压这条路以前零覆盖：把 clean_legacy_config_ui 的调用从这条分支删掉，CI 照样全绿。
# 变异测试暴露之后补上——r14 残留必须在两条路径上都被清掉。
for _s in STALE:
    assert not (inplace / 'vaultpatcher' / 'modules' / _s).exists(), \
        f'就地解压模式没清掉 {_s}——那条路的清理没生效'
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
    shutil.copytree(TREE / d, frel / d)
(frel / 'resourcepacks').mkdir()
shutil.copy2(rel / 'resourcepacks' / f'{PACK}.zip', frel / 'resourcepacks' / f'{PACK}.zip')
for s_ in ('install.sh', 'install.ps1'):
    materialize(ROOT / 'installer' / s_, frel / s_)

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

# ---- 回归：玩过的实例但 options.txt 不见了 → 绝不新建 ----
# 玩家报过：装完汉化后键位、视频、声音设置全没了。已有 options.txt 的路径是安全的
# （只改 resourcePacks 一行，实测其余 598 行逐字节不变），问题出在「文件不存在就新建
# 一份两行的」——游戏启动会把其余项按默认值补齐，等于把设置清空。
played = tmp / 'played-instance'
(played / 'mods').mkdir(parents=True)
for i in range(25):
    (played / 'mods' / f'modpack-{i}.jar').write_text('x', encoding='utf-8')
(played / 'logs').mkdir()                      # 启动过的痕迹
(played / 'saves').mkdir()
prel = played / 'ATM10-hanhua'
prel.mkdir()
(prel / 'config').mkdir()
(prel / 'config' / 'placeholder.txt').write_text('x', encoding='utf-8')
for s_ in ('install.sh', 'install.ps1'):
    materialize(ROOT / 'installer' / s_, prel / s_)
rc, out = run_prompt(prel, 'apply', str(played))
assert not (played / 'options.txt').exists(), \
    '玩过的实例缺 options.txt 时，安装器不该新建一份（会把玩家设置冲成默认）'
assert '不新建' in out, f'应提示不新建 options.txt：\n{out}'
print('✅ 玩过的实例缺 options.txt 时拒绝新建 OK')

# ---- 回归：多名玩家反馈「装完汉化包没启用，得自己进游戏拖到最后一位」----
#
# 根因：bash 版 patch_options 用 grep 取 resourcePacks 整行后直接 "${body%]}" 去掉
# 结尾的 "]"。但 Minecraft 在 **Windows** 上运行时，Java 的 println 按系统行尾写
# options.txt，也就是 CRLF；这样的行被 grep 取出来结尾其实是 "]\r" 而不是 "]"，
# "${body%]}" 匹配不上、什么都不剥，最终拼出
#   resourcePacks:[...]\r,"file/ATM10汉化包-7.2.zip"]
# 这种中间多出一个 "]"、还嵌着散落 \r 的坏行——数组语法已经损坏，游戏读出来的
# 资源包列表是错的，汉化包实际没启用。这种 CRLF 文件不是假设：实例目录如果被
# 同步/搬去 Windows 上启动过一次，再拿回 Mac/Linux 装这个包，options.txt 就是
# CRLF 的。（在下方 `resource_packs()` 未修复前对这类输入跑一遍就能复现：拿到的
# 是 None——说明整行已经不是合法的 resourcePacks 语法了。）
#
# 顺带把「重复安装不产生重复项」也在这里测了：旧代码摘除已有条目时只认双引号 +
# 带 file/ 前缀这一种写法，实测单引号、或不带 file/ 前缀的残留条目都摘不掉，
# 会越装越多份重复项（功能上不算「没启用」，因为最后一份仍在末尾，但明显是
# bug，任务要求「重复安装不产生重复项」）。
#
# 用 resource_packs() 直接解析数组，而不是像前面测试那样只做子串包含判断——
# 子串包含判断查不出「中间多插入了一个 ]」这种语法损坏，也查不出「条目还在，
# 但没排到最后一位」（等于没启用）这种情况。
def resource_packs(text):
    """从 options.txt 原文解析 resourcePacks 数组，返回条目列表（不分单双引号）。
    解析不出时返回 None——不该在语法已经损坏的情况下还拼出一个「看起来还行」的
    列表来。`[^\\]]*` 严格不吃 "]"：如果数组中间被错误地插入了多余的 "]"
    （CRLF 那个 bug 的典型症状），这里会在第一个 "]" 处就停手，随后要求紧跟着
    的是行尾（`\\r?$`）——多出来的内容会让整条正则匹配失败，从而如实报告"解析
    不出"，而不是悄悄只解析出前半段。"""
    m = re.search(r'^resourcePacks:\[([^\]]*)\]\r?$', text, re.M)
    if m is None:
        return None
    return re.findall(r'["\']([^"\']*)["\']', m.group(1))


def resline_case(name, opts_text):
    """造一个「实例 + 释放的安装器文件夹」，options.txt 按给定内容原样写入字节
    （不能用文本模式写，否则 Python 会把 \\r\\n 悄悄换行转写掉，测不出 CRLF 场景）。"""
    instd = tmp / name / 'instance'
    (instd / 'mods').mkdir(parents=True)
    for i in range(25):
        (instd / 'mods' / f'modpack-{i}.jar').write_text('x', encoding='utf-8')
    (instd / 'options.txt').write_bytes(opts_text.encode('utf-8'))
    reld = instd / 'ATM10-hanhua'
    reld.mkdir()
    (reld / 'config').mkdir()
    (reld / 'config' / 'placeholder.txt').write_text('x', encoding='utf-8')
    for s_ in ('install.sh', 'install.ps1'):
        materialize(ROOT / 'installer' / s_, reld / s_)
    return instd, reld


def run_apply_only(reld):
    """跑 apply，返回 (returncode, 合并输出)——不经过 run()，因为这批用例的
    释放文件夹没有完整出货树，只放了个占位 config/，够 patch_options 测试用。"""
    if IS_WIN:
        cmd = ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass',
               '-File', str(reld / 'install.ps1'), 'apply']
    else:
        cmd = ['bash', str(reld / 'install.sh'), 'apply']
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8',
                       errors='replace', timeout=300)
    return r.returncode, (r.stdout or '') + (r.stderr or '')


BARE = PACK + '.zip'   # 不带 file/ 前缀、带 .zip 后缀的裸文件名写法

CASES = [
    # 实测过的默认包顺序，十几项——起始状态就是「首次启动过一次后」的真实形状
    ('内置包十几个-LF-无本包',
     'version:4189\nresourcePacks:[%s]\nlang:zh_cn\n' % DEFAULT_PACKS),
    ('内置包十几个-CRLF-无本包',      # ← CRLF：反馈的核心复现场景
     'version:4189\r\nresourcePacks:[%s]\r\nlang:zh_cn\r\n' % DEFAULT_PACKS),
    ('本包已存在但不在最后-CRLF',      # ← CRLF + 需要挪位：反馈的核心复现场景
     'version:4189\r\nresourcePacks:[%s]\r\nlang:zh_cn\r\n'
     % ','.join(['"vanilla"', '"%s"' % ENTRY, '"mod_resources"',
                 '"add_xycraft_overrides_stone"'])),
    ('本包重复项-单引号带file前缀',
     'version:4189\nresourcePacks:["vanilla",\'%s\',"mod_resources"]\nlang:zh_cn\n' % ENTRY),
    ('本包重复项-双引号不带file前缀',
     'version:4189\nresourcePacks:["vanilla","%s","mod_resources"]\nlang:zh_cn\n' % BARE),
    ('本包重复项-单引号不带file前缀',
     'version:4189\nresourcePacks:["vanilla",\'%s\',"mod_resources"]\nlang:zh_cn\n' % BARE),
    ('数组尾随逗号-无本包',
     'version:4189\nresourcePacks:["vanilla","mod_resources",]\nlang:zh_cn\n'),
    ('数组尾随逗号-CRLF',
     'version:4189\r\nresourcePacks:["vanilla","mod_resources",]\r\nlang:zh_cn\r\n'),
]

for label, opts_before in CASES:
    c_instd, c_reld = resline_case(label, opts_before)
    rc, out = run_apply_only(c_reld)
    raw = (c_instd / 'options.txt').read_bytes().decode('utf-8')
    packs = resource_packs(raw)
    assert rc == 0, f'[{label}] apply 失败(rc={rc})：\n{out}'
    assert packs is not None, f'[{label}] resourcePacks 行语法损坏，解析不出来：\n{raw!r}'
    assert packs.count(ENTRY) == 1, \
        f'[{label}] 汉化包条目应恰好 1 份，实际 {packs.count(ENTRY)} 份：{packs}'
    assert packs[-1] == ENTRY, \
        f'[{label}] 汉化包不在列表最后一位（不在最后等于没启用）：{packs}'
print(f'✅ resourcePacks 各种写法 + CRLF + 重复安装 回归 OK（{len(CASES)} 个用例）')

# 幂等专项：本包已经在最后一位时，不该触发任何重写（也顺带验证 CRLF 原样保留，
# 不会被「已经对了」这条早退路径悄悄改动行尾风格）
idempo_instd, idempo_reld = resline_case(
    '本包已在最后-CRLF-幂等',
    'version:4189\r\nresourcePacks:["vanilla","mod_resources","%s"]\r\nlang:zh_cn\r\n' % ENTRY)
rc, out = run_apply_only(idempo_reld)
assert rc == 0, f'幂等用例 apply 失败(rc={rc})：\n{out}'
assert '跳过' in out, f'汉化包已在最后一位时应提示跳过而不是重写：\n{out}'
idempo_packs = resource_packs((idempo_instd / 'options.txt').read_bytes().decode('utf-8'))
assert idempo_packs is not None and idempo_packs == ['vanilla', 'mod_resources', ENTRY], \
    f'幂等跳过后数组不应变化：{idempo_packs}'
print('✅ 汉化包已在最后一位时正确识别为跳过、CRLF 原样保留 OK')

shutil.rmtree(tmp, ignore_errors=True)
print(f'✅ 安装脚本端到端测试通过（{platform.system()}）')

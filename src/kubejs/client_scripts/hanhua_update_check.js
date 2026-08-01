// ATM10 汉化补丁「绿油油版」客户端更新提示。
// 仅在本次客户端会话首次进入世界/服务器时异步读取 GitHub 最新正式 Release。
// 请求失败时保持静默；绝不下载或写入任何文件。

const HANHUA_VERSION = '@@PATCHVER@@'
const RELEASES_URL = 'https://github.com/chiba233/atm10-zh-cn/releases/latest'
const API_URL = 'https://api.github.com/repos/chiba233/atm10-zh-cn/releases/latest'
let updateCheckStarted = false

function releaseVersion(tag) {
  // 发布工作流允许 12、v12、r12、vr12 及其 12.1 这种多段版本号，
  // 也允许 -release11、-beta2、-rc3 这类后缀。release 的序号同样是版本的一部分。
  const match = String(tag).match(/^v?r?(\d+(?:\.\d+)*)(?:-(release|beta|rc)(\d+))?$/i)
  if (!match) return null
  return {
    parts: match[1].split('.').map(part => Number(part)),
    // 同一数字版本下，beta < rc < 正式版；没有后缀也按正式版处理。
    stage: match[2] ? { beta: 1, rc: 2, release: 3 }[match[2].toLowerCase()] : 3,
    serial: match[3] ? Number(match[3]) : 0
  }
}

function isNewerVersion(latest, current) {
  const length = Math.max(latest.parts.length, current.parts.length)
  for (let i = 0; i < length; i++) {
    const diff = (latest.parts[i] || 0) - (current.parts[i] || 0)
    if (diff !== 0) return diff > 0
  }
  if (latest.stage !== current.stage) return latest.stage > current.stage
  return latest.serial > current.serial
}

function tellUpdate($Minecraft, latest) {
  const message = Text.gold('[ATM10 汉化] ')
    .append(Text.yellow(`发现新版本 ${latest}（当前 ${HANHUA_VERSION}）。`))
    .append(Text.green(' [点击下载]').clickOpenUrl(RELEASES_URL)
      .hover('打开 GitHub Releases 最新正式版页面'))

  // HTTP 回调不在客户端主线程中；切回主线程再写聊天栏。
  $Minecraft.getInstance().execute(() => {
    const player = Client.player
    if (player) player.tell(message)
  })
}

ClientEvents.loggedIn(event => {
  if (updateCheckStarted) return
  updateCheckStarted = true

  try {
    // 所有 Java 类都在回调的保护范围内加载：某个运行环境不允许访问时静默跳过，
    // 不让 KubeJS 在加载脚本阶段报错，更不影响进入游戏。
    const $System = Java.loadClass('java.lang.System')
    if (String($System.getenv('ATM_SKIP_UPDATE_CHECK')) === '1') return
    const $HttpClient = Java.loadClass('java.net.http.HttpClient')
    const $HttpRequest = Java.loadClass('java.net.http.HttpRequest')
    const $HttpResponse = Java.loadClass('java.net.http.HttpResponse')
    const $URI = Java.loadClass('java.net.URI')
    const $Duration = Java.loadClass('java.time.Duration')
    const $Minecraft = Java.loadClass('net.minecraft.client.Minecraft')
    const current = releaseVersion(HANHUA_VERSION)
    if (current === null) return

    const request = $HttpRequest.newBuilder($URI.create(API_URL))
      .timeout($Duration.ofSeconds(6))
      .header('Accept', 'application/vnd.github+json')
      .header('User-Agent', 'atm10-zh-cn-update-checker')
      .GET()
      .build()

    $HttpClient.newBuilder().connectTimeout($Duration.ofSeconds(6)).build()
      .sendAsync(request, $HttpResponse.BodyHandlers.ofString())
      .thenAccept(response => {
        if (response.statusCode() !== 200) return
        const match = String(response.body()).match(/"tag_name"\s*:\s*"([^"]+)"/)
        if (!match) return
        const latest = match[1]
        const latestVersion = releaseVersion(latest)
        if (latestVersion !== null && isNewerVersion(latestVersion, current)) {
          tellUpdate($Minecraft, latest)
        }
      })
      .exceptionally(error => null)
  } catch (error) {
    // 类被运行环境限制等异常也不应影响正常进游戏。
  }
})

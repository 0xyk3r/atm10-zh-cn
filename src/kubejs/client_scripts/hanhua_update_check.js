// ATM10 汉化补丁「绿油油版」客户端更新提示。
// 仅在本次客户端会话首次进入世界/服务器时异步读取 GitHub 最新正式 Release。
// 请求失败时保持静默；绝不下载或写入任何文件。

const $HttpClient = Java.loadClass('java.net.http.HttpClient')
const $HttpRequest = Java.loadClass('java.net.http.HttpRequest')
const $HttpResponse = Java.loadClass('java.net.http.HttpResponse')
const $URI = Java.loadClass('java.net.URI')
const $Duration = Java.loadClass('java.time.Duration')
const $Minecraft = Java.loadClass('net.minecraft.client.Minecraft')

const HANHUA_VERSION = '@@PATCHVER@@'
const RELEASES_URL = 'https://github.com/chiba233/atm10-zh-cn/releases/latest'
const API_URL = 'https://api.github.com/repos/chiba233/atm10-zh-cn/releases/latest'
let updateCheckStarted = false

function releaseVersion(tag) {
  // 发布工作流允许 12、v12、r12、vr12 及其 12.1 这种多段版本号。
  // beta/rc 等后缀不参与正式版之间的数字比较。
  const match = String(tag).match(/^v?r?(\d+(?:\.\d+)*)(?:$|-)/i)
  return match ? match[1].split('.').map(part => Number(part)) : null
}

function isNewerVersion(latest, current) {
  const length = Math.max(latest.length, current.length)
  for (let i = 0; i < length; i++) {
    const diff = (latest[i] || 0) - (current[i] || 0)
    if (diff !== 0) return diff > 0
  }
  return false
}

function tellUpdate(latest) {
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

  const current = releaseVersion(HANHUA_VERSION)
  if (current === null) return

  try {
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
        if (latestVersion !== null && isNewerVersion(latestVersion, current)) tellUpdate(latest)
      })
      .exceptionally(error => null)
  } catch (error) {
    // 类被运行环境限制等异常也不应影响正常进游戏。
  }
})

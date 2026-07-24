let $TreeMap = Java.loadClass("java.util.TreeMap")
/** @type {import("org.apache.maven.artifact.versioning.DefaultArtifactVersion").$DefaultArtifactVersion$$Type} */
let $DefaultArtifactVersion = Java.loadClass("org.apache.maven.artifact.versioning.DefaultArtifactVersion")
/** @type {import("java.util.TreeMap").$TreeMap$$Type<(import("org.apache.maven.artifact.versioning.DefaultArtifactVersion").$DefaultArtifactVersion$$Original), (import("java.util.List").$List$$Type<(import("net.minecraft.network.chat.MutableComponent").$MutableComponent$$Original) >) >} */
let announcements = new $TreeMap()
/** @type {import("org.apache.maven.artifact.versioning.DefaultArtifactVersion").$DefaultArtifactVersion$$Original} */
let currentVersion = null

// files related:
// kubejs/assets/atm/lang/en_us.json

// Add your announcements here
function initAnnouncements(){
  addAnnouncement("4.0", "新增模组：奥术创造、冰与火之歌、Oritech")
  addAnnouncement("4.1", "新增模组：Oritech")
  addAnnouncement("4.2", "已移除模组：Oritech")
  addAnnouncement("4.3", "新增模组：奥术控制、机械动力：海洋雄心、机械动力：超级管道、通用机械：更多机器")
  addAnnouncement("4.5", "新增模组：AE2扩展、工业化过载和RF工具：存储")
  addAnnouncement("4.6", "新增模组：天境、植物盆、植树盆栽和精致存储：类型扩展")
  addAnnouncement("4.6", "已移除模组：轻松收获，该功能现由FTB终极挖掘实现")
  addAnnouncement("4.7", "新增模组：龙之进化和神秘植物盆")
  addAnnouncement("4.12", "新增模组：模块化蜜蜂")
  addAnnouncement("4.13", "新增模组：戴森立方计划")
  addAnnouncement("5.0", "已移除模组：模块化机械重生，请改用现代工业化")
  addAnnouncement("5.3", Text.of("我们正在准备 ").append(Text.red("REMOVE")).append(" mods ").append(Text.blue("永恒星光")).append(" and ").append(Text.blue("超立方盒")).append("，更新至6.0+版本时请做好准备！"))
  addAnnouncement("5.5", Text.of("我们刚刚启动了 ").append(Text.green("全部宝可梦（ATM10 + 方块宝可梦）").clickOpenUrl("https://www.curseforge.com/minecraft/modpacks/all-the-mons").hover(Text.translatable("mco.notification.visitUrl.buttonText.default"))).append(" 进行公开测试！"))
}

ServerEvents.loaded(event => {
  if (!Platform.isLoaded("bcc")) return
  announcements.clear()
  /** @type {import("dev.wuffs.bcc.BetterCompatibilityChecker").$BetterCompatibilityChecker$$Original} */
  let $BccInstance = Java.loadClass("dev.wuffs.bcc.BetterCompatibilityChecker")
  currentVersion = new $DefaultArtifactVersion($BccInstance.betterStatus.version())
  initAnnouncements()
})

function addAnnouncement(/** @type {string} */version, /** @type {import("net.minecraft.network.chat.MutableComponent").$MutableComponent$$Original} */ component) {
  announcements.computeIfAbsent(new $DefaultArtifactVersion(version), (key) => Utils.newList()).addLast(typeof component == "string" ? Text.of(component) : component)
}

PlayerEvents.loggedIn(event => {
  if (currentVersion == null) return
  let currentDismissed = event.player.persistentData.getString("LastDismissedAnnouncementVersion")
  if (currentDismissed == null) {
    currentDismissed = new $DefaultArtifactVersion("0.0.0")
  } else {
    currentDismissed = new $DefaultArtifactVersion(currentDismissed)
  }
  let ableToDismiss = false
  let printHeader = true
  announcements.forEach((key, listComponents) => {
    if (currentDismissed.compareTo(key) < 0 && currentVersion.compareTo(key) >= 0) {
      ableToDismiss = true
      if (printHeader) {
        event.player.tell(Text.translatable("=====[  %s  ]=====", Text.yellow("All The Mods Announcements").bold()).gold().bold())
        printHeader = false
      }
      for (let component of listComponents) {
        let message = Text.translatable("[%s] - %s", Text.gold(key.toString()), component.yellow()).yellow()
        event.player.tell(message)
      }            
    }
  })
    
  if (ableToDismiss) {
    let message = Text.translatable("announcements.atm.dismiss_up_to_version", Text.blue(currentVersion.toString()))
      .green()
      .hover(Text.translatable("kubejs.atm.click_here"))
      .clickRunCommand("/dismiss_announcements")
        
    event.player.tell(message)
  }
})

ServerEvents.basicPublicCommand("dismiss_announcements", event => {
  let player = event.player
  if (player == null) {
    event.cancel("未找到玩家！")
  } else {
    let pData = player.getPersistentData()
    if (event.input == "clear") {
      pData.putString("LastDismissedAnnouncementVersion", "0.0.0")
      event.respond(Text.yellow("已清除忽略的版本！"))
    } else {
      if (currentVersion == null) {
        event.cancel("整合包当前版本为空，是否已安装BetterCompatibilityCheck？")
      } else {
        pData.putString("LastDismissedAnnouncementVersion", currentVersion.toString())
        event.respond(Text.translatable("announcements.atm.dismissed_up_to_version", currentVersion.toString()).yellow())
      }
    }
  }
})
NativeEvents.onEvent("net.neoforged.neoforge.event.entity.player.PlayerEvent$PlayerChangedDimensionEvent", event => {
    if (event.to.location().getNamespace().equals("hyperbox")){
        event.entity.tell("Hyperboxes will be removed on version 6.0+, please move to Compact Machines")
        if (Platform.clientEnvironment) {
            Client["submit(java.lang.Runnable)"](() => {
                Client.gui.setTitle(Text.blue("超立方盒").append(Text.red(" 将被移除！")))
                Client.gui.setSubtitle(Text.white("请将你的物品转移到新模组 ").append(Text.blue("紧凑机械")))
            })
        }
    }
})
// This File has been authored by AllTheMods Staff, or a Community contributor for use in AllTheMods - AllTheMods 10.
// As all AllTheMods packs are licensed under All Rights Reserved, this file is not allowed to be used in any public packs not released by the AllTheMods Team, without explicit permission.

KubeJSTweaks.checkCompatibility(event => {
  event.checkModVersion("jei", "19.22.0.316", "此版本会导致工具耐久出现问题")
  event.checkModVersion("uranus", "[2.3.1-bugfix,2.3.1-bugfix2]", "此版本会导致 TPS 和内存泄漏问题")
  event.checkModVersion("octolib", "0.6.0.2", "此版本会导致 CPU 占用过高")
  event.checkModVersion("utilitarian", "1.21.1-0.15.0", "当前版本在对小型花朵使用骨粉时会崩溃")
  event.checkModVersion("amendments", "1.21-2.0.4", "此版本在打开讲台时会崩溃")

  event.checkModLoaded("accessories_compat_layer", "该模组可能与其他模组产生饰品类兼容性问题")
  event.checkModLoaded("letmedespawn", "该模组可能因NBT问题导致相同物品无法堆叠")

})

// This File has been authored by AllTheMods Staff, or a Community contributor for use in AllTheMods - AllTheMods 10.
// As all AllTheMods packs are licensed under All Rights Reserved, this file is not allowed to be used in any public packs not released by the AllTheMods Team, without explicit permission.

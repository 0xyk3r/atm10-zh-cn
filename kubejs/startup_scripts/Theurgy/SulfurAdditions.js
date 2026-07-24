// This File has been authored by AllTheMods Staff, or a Community contributor for use in AllTheMods - AllTheMods 10.
// As all AllTheMods packs are licensed under All Rights Reserved, this file is not allowed to be used in any public packs not released by the AllTheMods Team, without explicit permission.

StartupEvents.registry('item', allthemods => {
    //Forbidden Arcanus
    allthemods.create('stellarite_sulfur', 'theurgy:alchemical_sulfur')
        .sourceItem('forbidden_arcanus:stellarite_piece')
        .sourceName("流星碎片")
        .derivativeTier("precious")
        .sulfurType("metals")
    allthemods.create('arcane_sulfur', 'theurgy:alchemical_sulfur')
        .sourceItem('forbidden_arcanus:arcane_crystal')
        .sourceName("神秘水晶")
        .derivativeTier("rare")
        .sulfurType("gems")
    allthemods.create('runic_sulfur', 'theurgy:alchemical_sulfur')
        .sourceItem('forbidden_arcanus:rune')
        .sourceName("基础符文")
        .derivativeTier("common")
        .sulfurType("metals")
    //AllTheOres
    allthemods.create('salt_sulfur', 'theurgy:alchemical_sulfur')
        .sourceItem('alltheores:salt')
        .sourceName("盐")
        .derivativeTier("abundant")
        .sulfurType("earthen_matters")
    allthemods.create('sulfur_sulfur', 'theurgy:alchemical_sulfur')
        .sourceItem('alltheores:sulfur')
        .sourceName("硫磺")
        .derivativeTier("common")
        .sulfurType("misc")
    //Mystical Agriculture
    allthemods.create('prosperity_sulfur', 'theurgy:alchemical_sulfur')
        .sourceItem('mysticalagriculture:prosperity_shard')
        .sourceName("活化水晶碎片")
        .derivativeTier("common")
        .sulfurType("misc")
    //Occultism
    allthemods.create('iesnium_sulfur', 'theurgy:alchemical_sulfur')
        .sourceItem('occultism:iesnium_ingot')
        .sourceName("艾瑟金属")
        .derivativeTier("precious")
        .sulfurType("metals")
    //Irons
    allthemods.create('mithril_sulfur', 'theurgy:alchemical_sulfur')
        .sourceItem('irons_spellbooks:mithril_ingot')
        .sourceName("秘银")
        .derivativeTier("precious")
        .sulfurType("metals")
    //Silent
    allthemods.create('bort_sulfur', 'theurgy:alchemical_sulfur')
        .sourceItem('silentgear:bort')
        .sourceName("圆粒金刚石")
        .derivativeTier("rare")
        .sulfurType("earthen_matters")
        
})


// This File has been authored by AllTheMods Staff, or a Community contributor for use in AllTheMods - AllTheMods 10.
// As all AllTheMods packs are licensed under All Rights Reserved, this file is not allowed to be used in any public packs not released by the AllTheMods Team, without explicit permission.
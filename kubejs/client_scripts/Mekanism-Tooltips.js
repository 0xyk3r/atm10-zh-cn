// This File has been authored by AllTheMods Staff, or a Community contributor for use in AllTheMods - AllTheMods 10.
// As all AllTheMods packs are licensed under All Rights Reserved, this file is not allowed to be used in any public packs not released by the AllTheMods Team, without explicit permission.

ItemEvents.modifyTooltips(allthemods => {

    // ##### Gear #####

    //Mekasuit
    allthemods.add(/mekanism:mekasuit_/, [
        Text.red('能量消耗增加！'),
        Text.green('能量容量增加')
    ])
    //Meka Tool
    allthemods.add('mekanism:meka_tool', [
        Text.red('能量消耗增加！'),
        Text.green('能量容量增加！'),
        Text.green('攻击速度和伤害提高！')
    ])

    // ##### Generators #####

    //Solar Generator
    allthemods.add('mekanismgenerators:solar_generator', [
        Text.green('能量容量和产能提高！')
    ])
    //Advanced Solar Generator
    allthemods.add('mekanismgenerators:advanced_solar_generator', [
        Text.green('能量容量和产能提高！')
    ])
    //Wind Generator
    allthemods.add('mekanismgenerators:wind_generator', [
        Text.green('能量容量和产能提高！')
    ])
    //Heat Generator
    allthemods.add('mekanismgenerators:heat_generator', [
        Text.green('能量容量和产能提高！')
    ])
    //Gas Burning Generator
    allthemods.add('mekanismgenerators:gas_burning_generator', [
        Text.red('能量产出降低！'),
        Text.red('燃料消耗增加！')
    ])
    //Fission Generator
    allthemods.add(/mekanismgenerators:fission_/, [
        Text.red('能量产出降低！'),
    ])
    //Fusion Generator
    allthemods.add(/mekanismgenerators:fusion_/, [
        Text.red('能量产出降低！'),
        Text.green('燃料消耗降低！'),
    ])
    //Turbine
    allthemods.add(/mekanismgenerators:turbine_/, [
        Text.green('生产速度提高！'),
    ])
    //Boiler
    allthemods.add(/mekanism:boiler_/, [
        Text.green('生产速度提高！'),
    ])

    // ##### Machines #####

    //Upgrades
    allthemods.add(/mekanism:upgrade_/, [
        Text.green('机器增幅提高！')
    ])
    //Waste Barrel
    allthemods.add('mekanism:radioactive_waste_barrel', [
        Text.green('衰变速率提高！')
    ])
    //Thermal Evaporation Tower
    allthemods.add(/mekanism:thermal_evaporation_/, [
        Text.green('生产速度提高！')
    ])
    //Solar Neutron Activator
    allthemods.add('mekanism:solar_neutron_activator', [
        Text.green('生产速度提高！'),
        Text.green('废料 -> 钋已增强！')
    ])
    //Isotopic Centrifuge
    allthemods.add('mekanism:isotopic_centrifuge', [
        Text.green('废料 -> 钚已增强！')
    ])
    //Electric Pump
    allthemods.add('mekanism:electric_pump', [
        Text.green('生产速度提高！')
    ])
    //SPS
    allthemods.add(/mekanism:sps_/, [
        Text.green('能量消耗降低！')
    ])
})

// This File has been authored by AllTheMods Staff, or a Community contributor for use in AllTheMods - AllTheMods 10.
// As all AllTheMods packs are licensed under All Rights Reserved, this file is not allowed to be used in any public packs not released by the AllTheMods Team, without explicit permission.
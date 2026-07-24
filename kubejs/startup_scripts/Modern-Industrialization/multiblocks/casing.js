MIMachineEvents.registerCasings(allthemods => {
    allthemods.registerBlockImitation('darkstone_casing', 'forbidden_arcanus:polished_darkstone')
})

MIRegistrationEvents.registerCableTiers(allthemods => {
    allthemods.register(
        'runic',
        '符文',
        '符文',
        262144,
        'darkstone_casing',
    );
})

MIMachineEvents.registerHatches(allthemods => {
    allthemods.energy('runic')

    allthemods  .fluid(
        '符文',
        'runic',
        'darkstone_casing',
        4096
    )

    allthemods.item(
        '符文',
        'runic',
        'darkstone_casing',
        3, 5,
        8, 17
    )
})
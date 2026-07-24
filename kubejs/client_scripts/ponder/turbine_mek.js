// This File has been authored by AllTheMods Staff, or a Community contributor for use in AllTheMods - AllTheMods 10.
// As all AllTheMods packs are licensed under All Rights Reserved, this file is not allowed to be used in any public packs not released by the AllTheMods Team, without explicit permission.

Ponder.registry((allthemods) => {
    allthemods.create([
	'mekanismgenerators:turbine_casing',
	'mekanismgenerators:turbine_valve',
	'mekanismgenerators:turbine_vent',
	'mekanismgenerators:turbine_rotor',
	'mekanismgenerators:turbine_blade',
	'mekanismgenerators:rotational_complex',
	'mekanismgenerators:saturating_condenser',
	'mekanism:pressure_disperser',
	'mekanismgenerators:electromagnetic_coil',
	])
	.scene('turbine_mek','通用机械：工业涡轮机', 'kubejs:turbine_mek',
		
	(scene, util) => {
		
				
			scene.showStructure();
            scene.idle(5);

			scene.text(60, '工业涡轮利用热冷却剂发电。', [0, 4.5, 4.5]).placeNearTarget().attachKeyFrame();
			scene.idle(65);
			
			scene.text(60, '边框必须由涡轮机外壳构成。', [0, 4.5, 4.5]).placeNearTarget().attachKeyFrame();
			scene.idle(65);
			
			scene.text(60, '各面可采用涡轮外壳、结构玻璃、阀门或排气口。', [0, 2.5, 2.5]).placeNearTarget().attachKeyFrame();
			scene.idle(65);
			
			scene.text(60, '涡轮阀门用于泵入蒸汽或输出电力。', [0, 1.5, 2.5]).placeNearTarget().attachKeyFrame();
			scene.idle(65);

			//hide top
			scene.world.hideSection([0, 4, 0, 4, 6, 4], Facing.up);
			scene.idle(5);	
			
			//hide walls
			scene.world.hideSection([0, 4, 0, 4, 6, 4], Facing.up);
			scene.world.hideSection([0, 1, 0, 3, 6, 0], Facing.up);
			scene.world.hideSection([0, 1, 0, 0, 6, 3], Facing.up);
			scene.idle(10);	
			
			//Turbine Rotor
			
			scene.text(80, '涡轮转子必须放置在中央。每个转子消耗2个涡轮叶片。', [2, 3.5, 2.5]).placeNearTarget().attachKeyFrame();
			scene.idle(85);
			
			//show next layer
			scene.world.showSection([2, 4, 2], Facing.up);
			scene.idle(10);	
			
			scene.text(80, '复杂旋钮装置必须放置在涡轮转子上方。', [2, 4.5, 2.5]).placeNearTarget().attachKeyFrame();
			scene.idle(85);
			
			scene.world.showSection([1, 4, 1, 3, 4, 1], Facing.up);
			scene.world.showSection([3, 4, 2], Facing.up);
			scene.world.showSection([1, 4, 2], Facing.up);
			scene.world.showSection([1, 4, 3, 3, 4, 3], Facing.up);
			scene.idle(10);	
			
			scene.text(80, '分压元件必须填满围绕复杂旋钮装置的整层。', [1, 4.5, 2.5]).placeNearTarget().attachKeyFrame();
			scene.idle(85);
			
			//Show Layer Vents
			
			scene.world.showSection([0, 4, 0, 4, 4, 0], Facing.up);
			scene.world.showSection([0, 4, 4, 4, 4, 4], Facing.up);
			scene.world.showSection([0, 4, 1, 0, 4, 3], Facing.up);
			scene.world.showSection([4, 4, 0, 4, 4, 4], Facing.up);
			
			scene.world.showSection([0, 1, 0, 3, 3, 0], Facing.up);
			scene.world.showSection([0, 1, 1, 0, 3, 3], Facing.up);
			
			scene.text(120, '从此层开始，外侧表面可使用涡轮排气口。这些排气口还可导出涡轮内的水。', [0, 4.5, 3.5]).placeNearTarget().attachKeyFrame();
			scene.idle(125);
			
			//Show Electromagnetic Coil
			
			scene.world.showSection([2, 5, 2], Facing.up);
			scene.idle(5);
			
			scene.text(60, '电磁线圈需放置在复杂旋钮装置顶部。', [2, 5.5, 2.5]).placeNearTarget().attachKeyFrame();
			scene.idle(65);
			
			scene.world.setBlock([2, 5, 1], 'mekanismgenerators:electromagnetic_coil', true);
			scene.world.setBlock([1, 5, 2], 'mekanismgenerators:electromagnetic_coil', true);
			scene.world.setBlock([2, 5, 3], 'mekanismgenerators:electromagnetic_coil', true);
			scene.world.setBlock([3, 5, 2], 'mekanismgenerators:electromagnetic_coil', true);
			scene.world.showSection([2, 5, 1], Facing.up);
			scene.world.showSection([1, 5, 2], Facing.up);
			scene.world.showSection([2, 5, 3], Facing.up);
			scene.world.showSection([3, 5, 2], Facing.up);
			scene.idle(10);
						
			scene.text(100, '最多可放置5个。它们必须彼此相连，或直接接触复杂旋钮装置。', [2, 5.5, 2.5]).placeNearTarget().attachKeyFrame();
			scene.idle(105);
			
			//Saturating Condensers
			
			scene.world.showSection([3, 5, 3], Facing.up);
			scene.world.showSection([1, 5, 1], Facing.up);
			scene.world.showSection([1, 5, 3], Facing.up);
			scene.world.showSection([3, 5, 1], Facing.up);
			
			scene.text(120, '饱和冷凝器用于将蒸汽重新转化为水。非必需，但必须放置在或高于线圈层。', [1, 5.5, 1.5]).placeNearTarget().attachKeyFrame();
			scene.idle(130);
			
			//Show other layers
			
			scene.world.showSection([0, 5, 0, 4, 5, 0], Facing.up);
			scene.world.showSection([0, 5, 4, 4, 5, 4], Facing.up);
			scene.world.showSection([0, 5, 1, 0, 5, 3], Facing.up);
			scene.world.showSection([4, 5, 0, 4, 5, 3], Facing.up);
			scene.idle(5);
			
			scene.world.showSection([0, 6, 0, 4, 6, 4], Facing.up);
			scene.idle(20);
			
			scene.world.hideSection([1, 6, 1, 3, 6, 3], Facing.up);
			scene.idle(15);
			scene.world.setBlock([1, 6, 1], 'mekanismgenerators:turbine_vent', false);
			scene.world.setBlock([2, 6, 1], 'mekanismgenerators:turbine_vent', false);
			scene.world.setBlock([3, 6, 1], 'mekanismgenerators:turbine_vent', false);
			scene.world.setBlock([1, 6, 2], 'mekanismgenerators:turbine_vent', false);
			scene.world.setBlock([2, 6, 2], 'mekanismgenerators:turbine_vent', false);
			scene.world.setBlock([3, 6, 2], 'mekanismgenerators:turbine_vent', false);
			scene.world.setBlock([1, 6, 3], 'mekanismgenerators:turbine_vent', false);
			scene.world.setBlock([2, 6, 3], 'mekanismgenerators:turbine_vent', false);
			scene.world.setBlock([3, 6, 3], 'mekanismgenerators:turbine_vent', false);
			scene.idle(10);
			
			scene.world.showSection([1, 6, 1, 3, 6, 3], Facing.down);
			scene.idle(10);
			
			scene.text(80, '如需，顶面可用涡轮排气口替代。', [2.5, 6.5, 2.5]).placeNearTarget().attachKeyFrame();
			scene.idle(85);
			
			
    });
});

// This File has been authored by AllTheMods Staff, or a Community contributor for use in AllTheMods - AllTheMods 10.
// As all AllTheMods packs are licensed under All Rights Reserved, this file is not allowed to be used in any public packs not released by the AllTheMods Team, without explicit permission.

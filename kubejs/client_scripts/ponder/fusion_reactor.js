// This File has been authored by AllTheMods Staff, or a Community contributor for use in AllTheMods - AllTheMods 10.
// As all AllTheMods packs are licensed under All Rights Reserved, this file is not allowed to be used in any public packs not released by the AllTheMods Team, without explicit permission.

Ponder.registry((allthemods) => {
    allthemods.create([
	'mekanismgenerators:fusion_reactor_frame',
	'mekanismgenerators:fusion_reactor_port',
	'mekanismgenerators:fusion_reactor_controller',
	'mekanismgenerators:fusion_reactor_logic_adapter'
	])
	.scene('fusion_reactor','通用机械聚变反应堆', 'kubejs:fusion_mek',
		
	(scene, util) => {
		
				
			scene.world.showSection([0, 0, 0, 4, 4, 4], Facing.down);
            scene.idle(10);
			
			scene.text(60, '聚变反应堆可用于每刻生成数百万RF能量。', [0, 2.5, 4.5]).placeNearTarget().attachKeyFrame();
			scene.idle(80)
			
			scene.text(60, '端口可使用配置器进行更改', [1.5, 2.5, 0]).placeNearTarget().attachKeyFrame();
			scene.showControls(60, [1.5, 3.5, 0], 'down').rightClick().withItem('mekanism:configurator').whileSneaking();
			scene.idle(10);
			scene.world.modifyBlock([1, 2, 0], (curState) => curState.with("active", "true"), true);
			scene.idle(20);
			scene.world.modifyBlock([1, 2, 0], (curState) => curState.with("active", "false"), true);
			scene.idle(40);
			
			//hide front
			scene.world.hideSection([0, 0, 0, 4, 4, 3], Facing.up);
			scene.idle(10);
			
			scene.text(80, '聚变反应堆需按此结构逐面搭建。', [2.5, 2, 4.5]).attachKeyFrame();
			scene.idle(90);
			
			//east face
			scene.world.showSection([4, 0, 0, 4, 4, 3], Facing.down);
			scene.idle(10);
			
			//power port
			scene.text(60, '你需要一个用于输出电力的端口。', [4, 2.5, 2.5]).placeNearTarget().attachKeyFrame();
			scene.idle(70);
			
			//west face
			scene.world.showSection([0, 0, 0, 0, 4, 3], Facing.down);
			scene.idle(30);
			
			//Laser
			scene.text(60, '激光矩阵用于启动反应堆。', [0, 2.5, 2.5]).placeNearTarget().attachKeyFrame();
			scene.idle(70);
			
			//bottom face
			scene.world.showSection([1, 0, 0, 3, 0, 3], Facing.down);
			scene.idle(30);
			
			//top face
			scene.world.showSection([0, 4, 0, 3, 4, 3], Facing.down);
			scene.idle(30);
			
			//controller
			scene.text(60, '聚变堆控制器必须放置在顶面正中央。', [2.5, 4.5, 3.5]).placeNearTarget().attachKeyFrame();
			scene.idle(70);
			
			//north face
			scene.world.showSection([1, 1, 0, 3, 3, 0], Facing.down);
			scene.idle(30);
			
			//fuel input
			
			scene.text(30, '你需要两个端口来输入氘', [3.5, 2.5, 0]).placeNearTarget().attachKeyFrame();
			scene.idle(40);
			scene.text(40, '和氚。', [1.5, 2.5, 0]).placeNearTarget().attachKeyFrame();
			scene.idle(50);
			

			


    });
});

// This File has been authored by AllTheMods Staff, or a Community contributor for use in AllTheMods - AllTheMods 10.
// As all AllTheMods packs are licensed under All Rights Reserved, this file is not allowed to be used in any public packs not released by the AllTheMods Team, without explicit permission.

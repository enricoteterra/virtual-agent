import * as BABYLON from 'babylonjs';

export const createScene = (
    engine:BABYLON.Engine, canvas:HTMLCanvasElement): BABYLON.Scene => {

    const scene = new BABYLON.Scene(engine);
    // scene.clearColor = BABYLON.Color3.Purple();

    const camera = new BABYLON.FreeCamera("Camera", new BABYLON.Vector3(0, -2, -20), scene);
    camera.checkCollisions = true;
    camera.applyGravity = true;
    camera.setTarget(new BABYLON.Vector3(0, 0, 0));
    camera.attachControl(canvas,true);

    const light = new BABYLON.DirectionalLight("dir02", new BABYLON.Vector3(0.2, -1, 0), scene);
    light.position = new BABYLON.Vector3(0, 80, 0);

    // Shadows
    const shadowGenerator = new BABYLON.ShadowGenerator(2048, light);

    // Physics
    // scene.enablePhysics(null, new BABYLON.CannonJSPlugin());
    scene.enablePhysics(null, new BABYLON.OimoJSPlugin());

    const boxMaterial = new BABYLON.StandardMaterial('mat', scene);
    boxMaterial.alpha = 1;
    boxMaterial.backFaceCulling = true;
    boxMaterial.specularPower = 64;
    boxMaterial.useSpecularOverAlpha = true;
    boxMaterial.useAlphaFromDiffuseTexture = false;
    boxMaterial.diffuseColor = new BABYLON.Color3(0.41, 0.92, 1.00);
    boxMaterial.emissiveColor = new BABYLON.Color3(0.00, 0.74, 0.95);
    boxMaterial.ambientColor = new BABYLON.Color3(0.00, 0.00, 0.00);
    boxMaterial.specularColor = new BABYLON.Color3(1.00, 1.00, 1.00);

    const specialBox = new BABYLON.StandardMaterial('specialBox', scene);
    specialBox.alpha = 1;
    specialBox.backFaceCulling = true;
    specialBox.specularPower = 64;
    specialBox.useSpecularOverAlpha = true;
    specialBox.useAlphaFromDiffuseTexture = false;
    specialBox.diffuseColor = new BABYLON.Color3(0.76, 0.00, 0.32);
    specialBox.emissiveColor = new BABYLON.Color3(0.76, 0.00, 0.32);
    specialBox.ambientColor = new BABYLON.Color3(0.00, 0.00, 0.00);
    specialBox.specularColor = new BABYLON.Color3(1.00, 1.00, 1.00);

    let y = 0;
    let boxSent = false;

    for (let index = 0; index < 100; index++) {

        const box = BABYLON.Mesh.CreateBox("Box0", 3, scene);
        box.material = boxMaterial;
        box.position = new BABYLON.Vector3(Math.random() * 20 - 10, y, Math.random() * 10 - 5);
        shadowGenerator.getShadowMap()!.renderList!.push(box);
        box.physicsImpostor = new BABYLON.PhysicsImpostor(box, BABYLON.PhysicsImpostor.BoxImpostor, { mass: 1 }, scene);
 
        y += 2;

        if ( Math.random() > .95 && boxSent === false ) {
            box.material = specialBox;
            boxSent = true;
        }
    }

    // Playground
    const ground = BABYLON.Mesh.CreateBox("Ground", 1, scene);
    ground.scaling = new BABYLON.Vector3(100, 1, 100);
    ground.position.y = -5.0;
    ground.checkCollisions = true;

    const border0 = BABYLON.Mesh.CreateBox("border0", 1, scene);
    border0.scaling = new BABYLON.Vector3(1, 100, 100);
    border0.position.y = -5.0;
    border0.position.x = -50.0;
    border0.checkCollisions = true;

    const border1 = BABYLON.Mesh.CreateBox("border1", 1, scene);
    border1.scaling = new BABYLON.Vector3(1, 100, 100);
    border1.position.y = -5.0;
    border1.position.x = 50.0;
    border1.checkCollisions = true;

    const border2 = BABYLON.Mesh.CreateBox("border2", 1, scene);
    border2.scaling = new BABYLON.Vector3(100, 100, 1);
    border2.position.y = -5.0;
    border2.position.z = 50.0;
    border2.checkCollisions = true;

    const border3 = BABYLON.Mesh.CreateBox("border3", 1, scene);
    border3.scaling = new BABYLON.Vector3(100, 100, 1);
    border3.position.y = -5.0;
    border3.position.z = -50.0;
    border3.checkCollisions = true;

    const groundMat = new BABYLON.StandardMaterial("groundMat", scene);
    groundMat.diffuseColor = new BABYLON.Color3(0.5, 0.5, 0.5);
    groundMat.emissiveColor = new BABYLON.Color3(0.2, 0.2, 0.2);
    groundMat.backFaceCulling = false;
    ground.material = groundMat;
    border0.material = groundMat;
    border1.material = groundMat;
    border2.material = groundMat;
    border3.material = groundMat;
    ground.receiveShadows = true;

    // Physics
    ground.physicsImpostor = new BABYLON.PhysicsImpostor(ground, BABYLON.PhysicsImpostor.BoxImpostor, { mass: 0, friction: 0.5, restitution: 0.7 }, scene);
    border0.physicsImpostor = new BABYLON.PhysicsImpostor(border0, BABYLON.PhysicsImpostor.BoxImpostor, { mass: 0 }, scene);
    border1.physicsImpostor = new BABYLON.PhysicsImpostor(border1, BABYLON.PhysicsImpostor.BoxImpostor, { mass: 0 }, scene);
    border2.physicsImpostor = new BABYLON.PhysicsImpostor(border2, BABYLON.PhysicsImpostor.BoxImpostor, { mass: 0 }, scene);
    border3.physicsImpostor = new BABYLON.PhysicsImpostor(border3, BABYLON.PhysicsImpostor.BoxImpostor, { mass: 0 }, scene);

    camera.keysUp.push(87); // "w"
    camera.keysDown.push(83); // "s"
    camera.keysLeft.push(65); // "a"
    camera.keysRight.push(68); // "d"

    return scene;
}
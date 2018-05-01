(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const io = require("socket.io-client");
const socket = io('http://localhost:5000');
var events = [
    "click", "mousedown", "mouseup", "keydown", "change", "mouseup",
    "click", "dblclick", "mousemove", "mouseover", "mouseout", "mousewheel", "keydown",
    "keyup", "keypress", "textInput", "touchstart", "touchmove", "touchend", "touchcancel",
    "resize", "scroll", "zoom", "select", "change", "submit", "reset"
];
events.forEach(function (eventName) {
    document.getElementById("canvas").addEventListener(eventName, function (e) {
        let message = {
            "type": e.type,
            "timeStamp": e.timeStamp,
            "unixTimeStamp": +new Date()
        };
        if (e instanceof MouseEvent) {
            message['x'] = e.x;
            message['y'] = e.y;
            message['movementX'] = e.movementX;
            message['movementY'] = e.movementY;
        }
        else if (e instanceof KeyboardEvent) {
            message['code'] = e.code;
            message['key'] = e.key;
            message['keyCode'] = e.keyCode;
        }
        socket.emit('message', message);
    });
});

},{"socket.io-client":"socket.io-client"}],2:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const BABYLON = require("babylonjs");
var canvas = document.getElementById('canvas');
var engine = new BABYLON.Engine(canvas, true);
var createScene = function () {
    var scene = new BABYLON.Scene(engine);
    var camera = new BABYLON.FreeCamera("Camera", new BABYLON.Vector3(0, -2, -20), scene);
    camera.checkCollisions = true;
    camera.applyGravity = true;
    camera.setTarget(new BABYLON.Vector3(0, 0, 0));
    camera.attachControl(canvas, true);
    var light = new BABYLON.DirectionalLight("dir02", new BABYLON.Vector3(0.2, -1, 0), scene);
    light.position = new BABYLON.Vector3(0, 80, 0);
    var shadowGenerator = new BABYLON.ShadowGenerator(2048, light);
    scene.enablePhysics(null, new BABYLON.OimoJSPlugin());
    var boxMaterial = new BABYLON.StandardMaterial('mat', scene);
    boxMaterial.alpha = 1;
    boxMaterial.backFaceCulling = true;
    boxMaterial.specularPower = 64;
    boxMaterial.useSpecularOverAlpha = true;
    boxMaterial.useAlphaFromDiffuseTexture = false;
    boxMaterial.diffuseColor = new BABYLON.Color3(0.41, 0.92, 1.00);
    boxMaterial.emissiveColor = new BABYLON.Color3(0.00, 0.74, 0.95);
    boxMaterial.ambientColor = new BABYLON.Color3(0.00, 0.00, 0.00);
    boxMaterial.specularColor = new BABYLON.Color3(1.00, 1.00, 1.00);
    var specialBox = new BABYLON.StandardMaterial('specialBox', scene);
    specialBox.alpha = 1;
    specialBox.backFaceCulling = true;
    specialBox.specularPower = 64;
    specialBox.useSpecularOverAlpha = true;
    specialBox.useAlphaFromDiffuseTexture = false;
    specialBox.diffuseColor = new BABYLON.Color3(0.76, 0.00, 0.32);
    specialBox.emissiveColor = new BABYLON.Color3(0.76, 0.00, 0.32);
    specialBox.ambientColor = new BABYLON.Color3(0.00, 0.00, 0.00);
    specialBox.specularColor = new BABYLON.Color3(1.00, 1.00, 1.00);
    var y = 0;
    var boxSent = false;
    for (var index = 0; index < 100; index++) {
        var box = BABYLON.Mesh.CreateBox("Box0", 3, scene);
        box.material = boxMaterial;
        box.position = new BABYLON.Vector3(Math.random() * 20 - 10, y, Math.random() * 10 - 5);
        shadowGenerator.getShadowMap().renderList.push(box);
        box.physicsImpostor = new BABYLON.PhysicsImpostor(box, BABYLON.PhysicsImpostor.BoxImpostor, { mass: 1 }, scene);
        y += 2;
        if (Math.random() > .95 && boxSent === false) {
            box.material = specialBox;
            boxSent = true;
        }
    }
    var ground = BABYLON.Mesh.CreateBox("Ground", 1, scene);
    ground.scaling = new BABYLON.Vector3(100, 1, 100);
    ground.position.y = -5.0;
    ground.checkCollisions = true;
    var border0 = BABYLON.Mesh.CreateBox("border0", 1, scene);
    border0.scaling = new BABYLON.Vector3(1, 100, 100);
    border0.position.y = -5.0;
    border0.position.x = -50.0;
    border0.checkCollisions = true;
    var border1 = BABYLON.Mesh.CreateBox("border1", 1, scene);
    border1.scaling = new BABYLON.Vector3(1, 100, 100);
    border1.position.y = -5.0;
    border1.position.x = 50.0;
    border1.checkCollisions = true;
    var border2 = BABYLON.Mesh.CreateBox("border2", 1, scene);
    border2.scaling = new BABYLON.Vector3(100, 100, 1);
    border2.position.y = -5.0;
    border2.position.z = 50.0;
    border2.checkCollisions = true;
    var border3 = BABYLON.Mesh.CreateBox("border3", 1, scene);
    border3.scaling = new BABYLON.Vector3(100, 100, 1);
    border3.position.y = -5.0;
    border3.position.z = -50.0;
    border3.checkCollisions = true;
    var groundMat = new BABYLON.StandardMaterial("groundMat", scene);
    groundMat.diffuseColor = new BABYLON.Color3(0.5, 0.5, 0.5);
    groundMat.emissiveColor = new BABYLON.Color3(0.2, 0.2, 0.2);
    groundMat.backFaceCulling = false;
    ground.material = groundMat;
    border0.material = groundMat;
    border1.material = groundMat;
    border2.material = groundMat;
    border3.material = groundMat;
    ground.receiveShadows = true;
    ground.physicsImpostor = new BABYLON.PhysicsImpostor(ground, BABYLON.PhysicsImpostor.BoxImpostor, { mass: 0, friction: 0.5, restitution: 0.7 }, scene);
    border0.physicsImpostor = new BABYLON.PhysicsImpostor(border0, BABYLON.PhysicsImpostor.BoxImpostor, { mass: 0 }, scene);
    border1.physicsImpostor = new BABYLON.PhysicsImpostor(border1, BABYLON.PhysicsImpostor.BoxImpostor, { mass: 0 }, scene);
    border2.physicsImpostor = new BABYLON.PhysicsImpostor(border2, BABYLON.PhysicsImpostor.BoxImpostor, { mass: 0 }, scene);
    border3.physicsImpostor = new BABYLON.PhysicsImpostor(border3, BABYLON.PhysicsImpostor.BoxImpostor, { mass: 0 }, scene);
    camera.keysUp.push(87);
    camera.keysDown.push(83);
    camera.keysLeft.push(65);
    camera.keysRight.push(68);
    return scene;
};
var scene = createScene();
engine.runRenderLoop(function () {
    scene.render();
});
window.addEventListener('resize', function () {
    engine.resize();
});
var canvas = document.getElementById('canvas');
canvas.setAttribute('tabindex', '0');
canvas.focus();

},{"babylonjs":"babylonjs"}]},{},[1,2]);

import * as BABYLON from 'babylonjs';

// Get the canvas DOM element
var canvas = document.getElementById('canvas') as HTMLCanvasElement;

// Load the 3D engine
var engine = new BABYLON.Engine(canvas, true, {preserveDrawingBuffer: true, stencil: true});

// CreateScene function that creates and return the scene
var createScene = function(){

    // Create a basic BJS Scene object
    var scene = new BABYLON.Scene(engine);

    // Create Camera
    var camera = new BABYLON.ArcRotateCamera("camera", 0, 0, 0, new BABYLON.Vector3(0, 0, 0), scene);
    scene.activeCamera = camera;
    camera.setPosition(new BABYLON.Vector3(0, 20, 30));
    camera.attachControl(canvas, true);

    // Create a basic light, aiming 0, 1, 0 - meaning, to the sky
    var light = new BABYLON.HemisphericLight('light1', new BABYLON.Vector3(0, 1, 0), scene);
    
    // Create a built-in "sphere" shape; its constructor takes 6 params: name, segment, diameter, scene, updatable, sideOrientation
    var sphere = BABYLON.Mesh.CreateSphere('sphere1', 64, 2, scene, false, BABYLON.Mesh.FRONTSIDE);
    
    // Move the sphere upward 1/2 of its height
    sphere.position.y = 1;
    
    // Create a built-in "ground" shape; its constructor takes 6 params : name, width, height, subdivision, scene, updatable
    var ground = BABYLON.Mesh.CreateGround('ground1', 12, 12, 2, scene, false);
    
    // Return the created scene
    return scene;
}

// call the createScene function
var scene = createScene();

// run the render loop
engine.runRenderLoop(function(){
    scene.render();
});

// the canvas/window resize event handler
window.addEventListener('resize', function(){
    engine.resize();
});
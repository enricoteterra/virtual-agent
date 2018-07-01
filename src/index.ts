import * as BABYLON from 'babylonjs';
import { createScene } from './scenes/boxRoom';

const canvas = document.getElementById('canvas') as HTMLCanvasElement;
const engine = new BABYLON.Engine(canvas, true);

const scene = createScene(engine, canvas);
// scene.debugLayer.show();

engine.runRenderLoop(() => scene.render());

window.addEventListener('resize', () => engine.resize());

canvas.setAttribute('tabindex','0');
canvas.focus();
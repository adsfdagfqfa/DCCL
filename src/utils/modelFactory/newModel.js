import * as THREE from 'three'
import { CSG } from 'three-csg-ts';
const glassMaterial = new THREE.MeshPhysicalMaterial({
  metalness: 0.0,//玻璃非金属  金属度设置0
  roughness: 0.0,//玻璃表面光滑  
  envMapIntensity:1.0,
  transmission:1.0,//透射度(透光率)
  ior:1.5,//折射率
})
/**
 * 创建介质模型（创建一个圆柱体3d模型）
 * @returns {THREE.Mesh} 返回一个threejs中的mesh对象
 */
export function newMedium(){
  var geometry = new THREE.CylinderGeometry( 20, 20, 10, 32 );
  var material = new THREE.MeshBasicMaterial( {color:0x0727F1} );
  var cylinder = new THREE.Mesh( geometry, material );
  cylinder.rotation.z=Math.PI/2
  return cylinder;
}

/**
 * 创建透镜
 * @returns {THREE.Mesh} 返回一个threejs中的mesh对象
 */
export function newLens(){
  // 创建两个球体
  
  const radius = 40;
  const widthSegments = 32;
  const heightSegments = 32;
  let distance=1.5*radius
  const sphere1 = new THREE.SphereGeometry(radius, widthSegments, heightSegments);
  const sphere2 = new THREE.SphereGeometry(radius, widthSegments, heightSegments);
  const sphereMesh1=new THREE.Mesh(sphere1,glassMaterial)
  const sphereMesh2=new THREE.Mesh(sphere2,glassMaterial)
  // 移动第二个球体以形成凸透镜
  sphereMesh2.position.set(distance,0,0)
  
  sphereMesh1.updateMatrix();
  sphereMesh2.updateMatrix();
  const lens =  CSG.intersect(sphereMesh1, sphereMesh2);
  
  const geometry = lens.geometry;
  geometry.translate(-distance/2, 0, 0); // 将几何体沿 x 轴负方向移动,修改其重心位置
  
  return lens;
}

/**
 * 创建平面镜
 * @returns {THREE.Mesh} 返回一个threejs中的mesh对象
 */
export function newMirror(){
  const geometry = new THREE.BoxGeometry(5, 50, 50); // 宽度、高度、深度
  
  var box = new THREE.Mesh( geometry, glassMaterial );
  return box;
}
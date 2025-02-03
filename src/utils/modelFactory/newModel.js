import * as THREE from 'three'
/**
 * 创建介质模型（创建一个圆柱体3d模型）
 * @returns {THREE.Mesh} 返回一个threejs中的mesh对象
 */
export function newMedium(){
  var geometry = new THREE.CylinderGeometry( 5, 5, 20, 32 );
  var material = new THREE.MeshBasicMaterial( {color:rgb(7, 39, 241) } );
  var cylinder = new THREE.Mesh( geometry, material );
  return cylinder;
}

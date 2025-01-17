// Mirror.js
export class Mirror {
    constructor(id, reflectivity=1,radius=0.012, position= { x: 0, y: 0, z: 0 }) {
      this.id = id;
      this.type = 'Mirror';
      this.reflectivity = reflectivity;
      this.radius=radius;
      this.position = position;
   }
}
// Medium.js
export class Medium {
    constructor(id, length=0.001,radius=0.003,position= { x: 0, y: 0, z: 0 }) {
      this.id = id;
      this.type = 'Medium';
      this.length = length;
      this.radius=radius
      this.position = position;
   }
}
// Lens.js
export class Lens {
    constructor(id, focalLength=0.03,radius=0.012,position= { x: 0, y: 0, z: 0 }) {
      this.id = id;
      this.type = 'Lens';
      this.focalLength = focalLength;
      this.radius=radius
      this.position = position;
   }
}
// store.js
import { defineStore } from "pinia";

export const useThreeInstanceStore = defineStore("threeInstance", {
  state: () => ({
    threeInstance: null,//threejs的实例
    components:[],//储存的元素属性
    selectedElement: null,//当前选择的元素的名称
    distance:[],//储存的元素之间的距离
    angle:[]//储存的元素之间的角度，具体而言是其连线与主光轴的夹角
  }),
  getters: {
    
  },
  actions: {
    setThreeInstance(threeInstance){
      this.threeInstance=threeInstance
    },
    setSelectedElement(name){
      this.selectedElement=name
    }

  }
});
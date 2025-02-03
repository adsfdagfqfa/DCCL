// store.js
import { defineStore } from "pinia";

export const useThreeInstanceStore = defineStore("threeInstance", {
  state: () => ({
    threeInstance: null,//threejs的实例
    components:[],//储存的元素属性
    selectedElement: null//当前选择的元素
  }),
  getters: {
    //selectMeshUuid: state => state.selectMesh.uuid
  },
  actions: {
    setThreeInstance(threeInstance){
      this.threeInstance=threeInstance
    },

  }
});
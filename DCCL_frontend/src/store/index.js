// store.js
import { opticalModelList } from "@/utils/constant/model";
import threeInstance from "@/utils/threeInstance";
import { defineStore } from "pinia";
import axios from "axios";
export const useThreeInstanceStore = defineStore("threeInstance", {
  state: () => ({
    threeInstance: null,//threejs的实例
    components:[],//储存的元素属性
    selectedElement: "",//当前选择的元素的名称
    distance:[],//储存的元素之间的距离
    angle:[],//储存的元素之间的角度，具体而言是其连线与主光轴的夹角
    resonatorParam : {
      lambda:1064,//光的波长
      pumpWatt:100,//泵浦功率
      pumpEfficiency:0.72,//泵浦效率
      
    },
    fastFourierTransformParam:{
      sampleNumber:8192,//采样点数量
      windowExpandFactor:3//窗口扩展因子
    }
  }),
  getters: {
    
  },
  actions: {
    setThreeInstance(threeInstance){
      this.threeInstance=threeInstance
    },
    setSelectedElement(name){
      this.selectedElement=name
    },
    async uploadParameter(data){
      
      //上传参数
      await axios.post('/flask/api/v1/uploadParameter',data,{
        headers: {
          'Content-Type': 'application/json'  // 显式指定内容类型为 JSON
        },
        'withCredentials':true //携带cookie
      }).then(res=>{
        console.log(res)
      }).catch(err=>{
        console.log(err)
      })
    },
    async simulation(param){
      console.log(param)
      //模拟
      await axios.post('/flask/api/v1/simulation',param,{
        headers: {
          'Content-Type': 'application/json'  // 显式指定内容类型为 JSON
        },
        'withCredentials':true //携带cookie
      }).then(res=>{
        console.log(res)
      }).catch(err=>{
        console.log(err)
      })
    }
  }
});
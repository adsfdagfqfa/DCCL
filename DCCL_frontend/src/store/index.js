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
    },
    simulationResult:['迭代次数: 2 传输系数main: 0.904157280921936 传输系数free: 4.078216552734375 输出功率: 2.8363040804890716e-09 终止判定1: 0.09057203680276871 终止判定2: 0.8563631176948547'
    ,'迭代次数: 3 传输系数main: 0.904157280921936 传输系数free: 4.078216552734375 输出功率: 2.8363040804890716e-09 终止判定1: 0.09057203680276871 终止判定2: 0.8563631176948547'
    ,'迭代次数: 4 传输系数main: 0.904157280921936 传输系数free: 4.078216552734375 输出功率: 2.8363040804890716e-09 终止判定1: 0.09057203680276871 终止判定2: 0.8563631176948547'
    ,'迭代次数: 15 传输系数main: 0.904157280921936 传输系数free: 4.078216552734375 输出功率: 2.8363040804890716e-09 终止判定1: 0.09057203680276871 终止判定2: 0.8563631176948547'
    ,'迭代次数: 115 传输系数main: 0.904157280921936 传输系数free: 4.078216552734375 输出功率: 2.8363040804890716e-09 终止判定1: 0.09057203680276871 终止判定2: 0.8563631176948547'
    ,'迭代次数: 1115 传输系数main: 0.904157280921936 传输系数free: 4.078216552734375 输出功率: 2.8363040804890716e-09 终止判定1: 0.09057203680276871 终止判定2: 0.8563631176948547'
    ,'迭代次数: 11115 传输系数main: 0.904157280921936 传输系数free: 4.078216552734375 输出功率: 2.8363040804890716e-09 终止判定1: 0.09057203680276871 终止判定2: 0.8563631176948547'
    ,
  ]//输出结果
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
    async simulation(param,dom){
      this.simulationResult=[]
      console.log(param)
      const encodedJsonString = encodeURIComponent(param);
      
      const sseUrl = `/flask/api/v1/simulation?data=${encodedJsonString}`;
      // 创建 EventSource 实例
      const eventSource = new EventSource(sseUrl);
       // 监听消息事件
      var that=this//保存上下文 
      eventSource.onmessage = function(event) {
        console.log("Received data:", event.data);
        that.simulationResult.push(event.data)
        dom.scrollToBottom()
        //更新数据
      };

      // 监听错误事件
      eventSource.onerror = function(err) {
        console.error("EventSource failed:", err);
        eventSource.close(); // 关闭连接
      };

    }
  }
});
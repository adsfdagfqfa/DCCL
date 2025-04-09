// store.js
import { opticalModelList } from "@/utils/constant/model";
import threeInstance from "@/utils/threeInstance";
import { defineStore } from "pinia";
import axios from "axios";
import { v4 as uuidv4 } from 'uuid'; // 引入 uuid 库
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
    pictureKey:"4d26940b-fb2e-4773-a039-a332830954fd79faca",
    opticalFieldDialogVisible:false,//是否显示光场图的modal
    plotDialogVisible:false,//是否展示统计图的modal
    // simulationResult:['{"iterationCount": 1, "transmissionCoefficientMain": 0.12488810380845108, "transmissionCoefficientFree": 1.3597301688242887, "outputPower": 1.3844463502127228e-08, "selectedAttribute": {"pumpWatt": 100}}',
    //   '{"iterationCount": 2, "transmissionCoefficientMain": 4.394131158750255, "transmissionCoefficientFree": 0.28927424014929864, "outputPower": 1.889652435807665e-08, "selectedAttribute": {"pumpWatt": 100}}',
    //   '{"iterationCount": 3, "transmissionCoefficientMain": 1.6079267344310049, "transmissionCoefficientFree": 0.3671436057957992, "outputPower": 5.457417415780011e-09, "selectedAttribute": {"pumpWatt": 100}}',
    //   '{"iterationCount": 4, "transmissionCoefficientMain": 0.4587180653843628, "transmissionCoefficientFree": 4.697790443555496, "outputPower": 1.995544242408198e-09, "selectedAttribute": {"pumpWatt": 100}}',
    //   '{"iterationCount": 5, "transmissionCoefficientMain": 0.5116639631999548, "transmissionCoefficientFree": 0.8729980650419275, "outputPower": 9.441116321692685e-09, "selectedAttribute": {"pumpWatt": 100}}',
    //   '{"iterationCount": 6, "transmissionCoefficientMain": 2.6011093223635466, "transmissionCoefficientFree": 0.2333651375509338, "outputPower": 8.241264818278385e-09, "selectedAttribute": {"pumpWatt": 100}}',
    //   '{"iterationCount": 6, "fieldDistributionMain": "ef83f993-f5f2-4e87-885b-c88d3413023efe13be", "fieldDistributionFree": "ef83f993-f5f2-4e87-885b-c88d3413023e03e54a", "outputPower": 8.241264818278385e-09, "isEnd": true}',
    // ]
    simulationResult:[{id:'asdgaka',content:'{"iterationCount": 1, "transmissionCoefficientMain": 0.12488810380845108, "transmissionCoefficientFree": 1.3597301688242887, "outputPower": 1.3844463502127228e-08, "selectedAttribute": {"pumpWatt": 100}}',
    }],
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
      //将查询参数对象转换为 JSON 字符串
      const encodedJsonString = encodeURIComponent(param);
      
      const sseUrl = `/flask/api/v1/simulation?data=${encodedJsonString}`;
      // 创建 EventSource 实例
      const eventSource = new EventSource(sseUrl);
       // 监听消息事件
      var that=this//保存上下文 
      eventSource.onmessage = function(event) {
        console.log("Received data:", event.data);
        console.log(event.data);
        that.simulationResult.push({
          id: uuidv4(),
          content: event.data
        })
        dom.scrollToBottom()
        //更新数据
      };
     
      // 监听错误事件
      eventSource.onerror = function(err) {
        console.error("EventSource failed:", err);
        eventSource.close(); // 关闭连接
      };
      
    },
    async getPicture() {
      console.log("getPicture")
      try {
        const response = await axios.get(`/flask/api/v1/picture/${this.pictureKey}`);
        return response.data; // 返回数据，供组件使用
      } catch (error) {
        console.error('Request failed:', error);
        throw error; // 重新抛出错误，让调用者知道请求失败
      }
    }
  }
});
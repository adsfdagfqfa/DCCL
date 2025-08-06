// store.js
import { opticalModelList } from "@/utils/constant/model";
import threeInstance from "@/utils/threeInstance";
import { defineStore } from "pinia";
import axios from "axios";
import { v4 as uuidv4 } from 'uuid'; // 引入 uuid 库
import { th } from "element-plus/es/locale";
export const useThreeInstanceStore = defineStore("threeInstance", {
  state: () => ({
    tokenInitialized: false, // 是否初始化了token
    threeInstance: null,//threejs的实例
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
    // pictureKey:"5281bd60-6d64-4ee4-9f11-25948f8e5da4276dbd",
    opticalFieldDialogVisible:false,//是否显示光场图的modal
    plotDialogVisible:false,//是否展示统计图的modal
    currentTaskID:"",//当前任务的ID
    fileName:"",//当前要获取的文件名
    eventSource: null, // 用于存储 EventSource 实例
    // simulationResult:['{"iterationCount": 1, "transmissionCoefficientMain": 0.12488810380845108, "transmissionCoefficientFree": 1.3597301688242887, "outputPower": 1.3844463502127228e-08, "selectedAttribute": {"pumpWatt": 100}}',
    //   '{"iterationCount": 2, "transmissionCoefficientMain": 4.394131158750255, "transmissionCoefficientFree": 0.28927424014929864, "outputPower": 1.889652435807665e-08, "selectedAttribute": {"pumpWatt": 100}}',
    //   '{"iterationCount": 3, "transmissionCoefficientMain": 1.6079267344310049, "transmissionCoefficientFree": 0.3671436057957992, "outputPower": 5.457417415780011e-09, "selectedAttribute": {"pumpWatt": 100}}',
    //   '{"iterationCount": 4, "transmissionCoefficientMain": 0.4587180653843628, "transmissionCoefficientFree": 4.697790443555496, "outputPower": 1.995544242408198e-09, "selectedAttribute": {"pumpWatt": 100}}',
    //   '{"iterationCount": 5, "transmissionCoefficientMain": 0.5116639631999548, "transmissionCoefficientFree": 0.8729980650419275, "outputPower": 9.441116321692685e-09, "selectedAttribute": {"pumpWatt": 100}}',
    //   '{"iterationCount": 6, "transmissionCoefficientMain": 2.6011093223635466, "transmissionCoefficientFree": 0.2333651375509338, "outputPower": 8.241264818278385e-09, "selectedAttribute": {"pumpWatt": 100}}',
    //   '{"iterationCount": 6, "fieldDistributionMain": "ef83f993-f5f2-4e87-885b-c88d3413023efe13be", "fieldDistributionFree": "ef83f993-f5f2-4e87-885b-c88d3413023e03e54a", "outputPower": 8.241264818278385e-09, "isEnd": true}',
    // ]
    simulationResult:[{id:'asdgaka',content:'{"iterationCount": 1, "transmissionCoefficientMain": 0.598172448859426, "transmissionCoefficientFree": 1.0467823194621835, "outputPower": 1.36186823910903e-08, "isEnd": false, "selectedAttribute": {"lambda": 1064.1}}',}
    ,{id:'1111',content:'{"iterationCount": 2, "transmissionCoefficientMain": 2.1774218242786127, "transmissionCoefficientFree": 0.21662303832812996, "outputPower": 1.4299165644251156e-08, "isEnd": false, "selectedAttribute": {"lambda": 1064.1}}',},
    
    {id:'2222',content:'{"iterationCount": 3, "transmissionCoefficientMain": 0.9774801348234873, "transmissionCoefficientFree": 2.5120109677046387, "outputPower": 3.0801227115969505e-09, "isEnd": false, "selectedAttribute": {"lambda": 1064.1}}',},
    {id:'3333',content:'{"iterationCount": 4, "transmissionCoefficientMain": 0.7856474450095124, "transmissionCoefficientFree": 1.5535101704999157, "outputPower": 7.786699866076718e-09, "isEnd": false, "selectedAttribute": {"lambda": 1064.1}}',},
    {id:'4444',content:'{"iterationCount": 5, "transmissionCoefficientMain": 1.3952515792149736, "transmissionCoefficientFree": 0.5707095893986177, "outputPower": 1.2117033671122183e-08, "isEnd": false, "selectedAttribute": {"lambda": 1064.1}}',},
    {id:'5555',content:'{"iterationCount": 6, "transmissionCoefficientMain": 1.1374454011432196, "transmissionCoefficientFree": 1.171414700310216, "outputPower": 6.910340588242904e-09, "isEnd": false, "selectedAttribute": {"lambda": 1064.1}}',},
    {id:'6666',content:'{"iterationCount": 7, "transmissionCoefficientMain": 0.949813934162312, "transmissionCoefficientFree": 1.5032604221678725, "outputPower": 8.095587938440452e-09, "isEnd": false, "selectedAttribute": {"lambda": 1064.1}}',},
    {id:'7777',content:'{"iterationCount": 8, "transmissionCoefficientMain": 1.2077731534934137, "transmissionCoefficientFree": 0.8466666863557571, "outputPower": 1.2179056297915608e-08, "isEnd": false, "selectedAttribute": {"lambda": 1064.1}}',},
    {id:'8888',content:'{"iterationCount": 9, "transmissionCoefficientMain": 1.1681646578449236, "transmissionCoefficientFree": 1.0576713825207311, "outputPower": 1.03146712818499e-08, "isEnd": false, "selectedAttribute": {"lambda": 1064.1}}',}
  ],
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
    async uploadParameter(data) {
      try {
        const res = await axios.post('/flask/api/v1/uploadParameter', data, {
          headers: {
            'Content-Type': 'application/json'
          },
          withCredentials: true
        });
        console.log(res.data);
        this.currentTaskID = res.data.task_id; // 保存任务ID
        return res.data.task_id; //  正确返回
      } catch (err) {
        console.error(err);
        throw err; // 或者返回 null，取决于你业务逻辑
      }
    },

    async simulation(param,dom){
     
      /**
       * 仿真计算参数
       * @typedef {Object} param
       * @property {Object} variable      - 变量定义
       * @property {string} variable.path - JSONPath，指向需要扫描/变化的模型属性 例："$.modelAttributeList[0].reflectivity"
       * @property {number[]} variable.vectors - 该变量要取的离散值序列 例：[1, 2]
       * @property {number} iterationCount - 总迭代（采样）次数，正整数 例：1000
       * @property {string} taskID - 任务ID，上传参数时返回的任务ID
       */
      
      const sseUrl = `/flask/api/v1/stream?taskID=${param.taskID}`;
      // 创建 EventSource 实例
      const es = new EventSource(sseUrl);
       // 监听消息事件
      var that=this//保存上下文 
      es.onmessage = function(event) {
        console.log("Received data:", event.data);
        console.log(event.data);
        that.simulationResult.push({
          //vue-virtual-scroller组件需要一个不重复的id用来表示各项
          id: uuidv4(),
          content: event.data
        })
        dom.scrollToBottom()
        //更新数据
      };
     
      // 监听错误事件
      es.onerror = function(err) {
        console.error("EventSource failed:", err);
        es.close(); // 关闭连接
      };
      this.eventSource = es; // 保存 EventSource 实例到 store 中
      // 清空之前的结果
      this.simulationResult=[]
      /** @type {param} */
      param=JSON.stringify(param) //将查询参数对象转换为 JSON 字符串
      //将查询参数对象转换为 JSON 字符串
      await axios.post('/flask/api/v1/simulation',param,{
        headers: {
          'Content-Type': 'application/json'  // 显式指定内容类型为 JSON
        },
        'withCredentials':true //携带cookie
      }).then(res=>{
        console.log(res.data)
      }).catch(err=>{
        console.log(err)
      })
    },
    async getPicture() {
      console.log("getPicture")
      try {
        const response = await axios.get(`/flask/api/v1/picture/${this.taskID}/${this.fileName}`);
        return response.data; // 返回数据，供组件使用
      } catch (error) {
        console.error('Request failed:', error);
        throw error; 
      }
    },
    async downloadData(){
      console.log("downloadData")
      try {
        const a = document.createElement('a');
        a.href = `/flask/api/v1/download/${this.taskID}/${this.fileName}`;
        a.download = 'file.mat';
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      } catch (error) {
        console.error('Request failed:', error);
      }
    },
    async initToken() {
      try {
        await axios.post('/flask/api/v1/token/init',null,{
          'withCredentials':true //携带cookie
        })
        this.tokenInitialized = true
        console.log('Token 初始化成功')
      } catch (error) {
        console.error('Token 初始化失败', error)
      }
    },
    async continueTask(taskID) {
      console.log("continueTask", taskID);
      try {
        const response = await axios.get(
          `/flask/api/v1/task/continue?taskID=${encodeURIComponent(taskID)}`
        );
        console.log(response.data);
      } catch (error) {
        console.error('Request failed:', error);
        throw error;
      }
    },
    async pauseTask(taskID) {
      console.log("pauseTask",taskID)
      try {
        const response = await axios.get(`/flask/api/v1/task/pause?taskID=${encodeURIComponent(taskID)}`);
        console.log(response.data); 
      } catch (error) {
        console.error('Request failed:', error);
        throw error; 
      }
    },
    async cancelTask(taskID) {
      console.log("cancelTask",taskID)
      try {
        this.eventSource.close(); // 关闭 EventSource 连接
        this.eventSource = null; // 清空 EventSource 实例
        this.simulationResult = []; // 清空模拟结果
        this.currentTaskID = ""; // 清空当前任务ID
        // 发送取消请求
        const response = await axios.get(`/flask/api/v1/task/cancel?taskID=${encodeURIComponent(taskID)}`);
        console.log(response.data); 
      } catch (error) {
        console.error('Request failed:', error);
        throw error; 
      }
    },
  }
});
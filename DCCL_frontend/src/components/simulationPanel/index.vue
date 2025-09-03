<template>
    <div class="flex">
      <div style="flex:0 0 30%">
        <el-card class="h-full">
            <el-cascader class="mb-5" clearable 
                    v-model="selectedElement" 
                    :options="jsonpath" 
                    :show-all-levels="false" 
                    placeholder="请选择参数"
                    @expand-change="handleExpandChange"
                    @clear="handleClear"/>    
            <RangeGenerator @get-result-array="getResultArray"  ref="rangeGenerator"/>
            <div class="flex items-center mb-5">
              <label class="whitespace-nowrap min-w-20">迭代次数:</label>
              <el-input type="number" v-model.number="iterationCount"
                placeholder="请输入迭代次数"
                title="" clearable/>
            </div>
            <!-- <el-button type="primary" @click="onUploadParameter">上传参数</el-button> -->
            <el-button type="primary" @click="onSimulation">开始仿真</el-button>
            <el-button type="primary" @click="store.plotDialogVisible=true">分析结果</el-button>
        </el-card>
      </div>
      <!-- <div class="flex-1">
        <DynamicScroller
          ref="virtualScroller"
          class="list"
          :items="visibleItems"
          :min-item-size="150">
          <template v-slot="{ item }">
            <DynamicScrollerItem :item="item" :active="true" :size-dependencies="[item.content]">
              <div class="list-item" :key="item.id">
                <ResultItem :item="item.content" :only_final_result="store.onlyFinalResult" />
              </div>
            </DynamicScrollerItem>
          </template>
        </DynamicScroller>
        <div class="flex justify-between items-center p-4">
          <el-checkbox v-model="store.onlyFinalResult" label="只显示结果" size="large" />
          <div class="flex items-center space-x-2">
            <el-button :type="isPaused?'success':'warning'" @click="onTogglePauseTask">{{ isPaused ? '继续' : '暂停' }}</el-button>
            <el-button type="danger" @click="onCancelTask">取消</el-button>
          </div>
        </div>
      </div> -->

    </div>
  </template>
  
  <script setup>
  // import {JSONPath} from 'jsonpath-plus';
  import { onMounted,getCurrentInstance,onBeforeMount, ref ,computed} from 'vue';
  import { useThreeInstanceStore } from '@/store';
  import RangeGenerator from './rangeGenerator.vue';
  // import ResultItem from '../outputPanel/resultItem.vue'; 
  const rangeGenerator = ref();//引用的rangeGenerator组件
  // const isPaused = ref(false)
  const taskID = ref(null);
  var jp = require('jsonpath');
  const data = computed(() => ({
    distance: store.distance,
    angle: store.angle,
    resonatorParam: store.resonatorParam,
    fastFTParam: store.fastFourierTransformParam,
    modelAttributeList: store.threeInstance.modelAttributeList
  }));
  const store = useThreeInstanceStore();
  //selectedElement为数组，记录选中的元素的路径
  const selectedElement = ref()
  const vectors=ref([])
  const iterationCount=ref(1000); //迭代次数
  const jsonpath=ref([
    {
      value: '$.modelAttributeList[*].focalLength',
      label:'焦距(m)',
      children:[],
      leaf:false
    },
    {
      value: '$.modelAttributeList[*].reflectivity',
      label:'反射率',
      children:[],
      leaf:false
    },
    {
      value:'$.angle[*]',
      label:'角度(deg)',
      children:[],
      leaf:false
    },
    {
      value:'$.distance[*]',
      label:'距离(m)',
      children:[],
      leaf:false
    },
    {
      value:'$.resonatorParam.lambda',
      label:'波长(nm)',
      leaf:true
    },
    {
      value:'$.resonatorParam.pumpWatt',
      label:'泵浦功率(W)',
      leaf:true
    },
  ])
  
  const resultList = computed(() => {
    return store.simulationResult;
  });
  // async function getAllParameter() {
  //   data.distance=store.distance;
  //   data.angle=store.angle;
  //   data.resonatorParam=store.resonatorParam;
  //   data.fastFTParam=store.fastFourierTransformParam;
  //   data.modelAttributeList=store.threeInstance.modelAttributeList;
  //   // var nodes=jp.nodes(data,'$..focalLength');
  //   // console.log(nodes)
  // }
  
  function handleExpandChange(activePath){
    if(activePath.length==0){
      //当activePath为空时直接退出
      return
    } 
    console.log('当前展开的路径：', activePath);
    console.log('当前数据：',data.value );
    // 获取当前展开的节点
    const currentNode = getNodeByPath(jsonpath.value, activePath);
    // 动态加载子节点数据
    try {
      loadChildren(currentNode).then((children) => {
        console.log('加载子节点成功：', children);
        currentNode.children = children;
      });
    } catch (error) {
      console.error('加载子节点失败：', error);
    }
    
  }
  function getNodeByPath(tree, path) {
    // 根据路径获取节点,对path中的每一项（currentValue）进行递进查找
    return path.reduce((acc, currentValue) => {
      return acc.find((node) => node.value === currentValue);
    }, tree);
  }
  async function loadChildren(node) {
    // 模拟异步加载,如果有需要可以使用await
    // await  new Promise((resolve) => setTimeout(resolve, 1000));
    console.log('加载子节点：', node.value);
    var dataList=jp.nodes(data.value, node.value);
    console.log(dataList)
    //生成children结点数组
    var nodes = Array.from(dataList).map((item) => ({
      value: jp.stringify(item.path),
      label: label(item),
      //只生成一级菜单
      leaf: true,
    }))
    return nodes;
   
  }
  //将jsonpath转换可现实的选项标签
  function label(item){
    console.log(item)
    let length=item.path.length;
    switch(item.path[1]){
      case 'modelAttributeList':
        let a=jp.query(data.value,jp.stringify(item.path.slice(0,length-1)));
        return a[0].model+"_"+item.path[length-1];
      case 'angle':
        return item.path[1]+'_'+item.path[length-1];
      case 'distance':
        return item.path[1]+'_'+item.path[length-1];
    }
    return jp.stringify(item.path);
  }
  onMounted(async () => {
    // await getAllParameter();
    console.log('Component is mounted');
  })
  async function onSimulation(){
    // let length=selectedElement.value.length;
    // console.log(selectedElement.value);
    // console.log(jp.query(data,selectedElement.value[length-1]));
    // console.log(iterationCount.value)
    //判断是否设置参数
    if(iterationCount.value===undefined || iterationCount.value<=0){
      alert("请输入有效的迭代次数")
      return
    }
    const param={}
    console.log(vectors.value.length)
    if(selectedElement.value!==undefined  && vectors.value.length>0){
      let length=selectedElement.value.length;
      param.variable={};
      param.variable.path=selectedElement.value[length-1]
      param.variable.vectors=vectors.value
    }
    param.iterationCount=iterationCount.value;

    taskID.value=await store.uploadParameter(JSON.stringify(data.value))

    param.taskID=taskID.value;
    console.log('taskID', taskID.value);
    console.log(param)
    console.log('上传参数')
    
    // var virtualScroller=pageInstance.refs.virtualScroller;
    await store.simulation(param)
    // console.log(data)
    console.log('开始仿真')
   
  }
  async function onUploadParameter(){
    console.log(store.distance)
    console.log(data.value)
    // console.log(iterationCount.value)
    await store.uploadParameter(JSON.stringify(data.value))
    console.log('上传参数')
  }
  function getResultArray(value){
    console.log(value)
    vectors.value=value
  }
  function handleClear(){
    //清除rangeGenerator里面的输入
    console.log("清除输入")
    if (rangeGenerator.value) {
      rangeGenerator.value.clearInput();
    }
  }
  // function onTogglePauseTask(){
  //   if(isPaused.value){
  //     isPaused.value=false;
  //     store.continueTask(taskID.value);
  //   }
  //   else{
  //     isPaused.value=true;
  //     store.pauseTask(taskID.value);
  //   }
  // }
  // function onCancelTask(){
  //   store.cancelTask(taskID.value);
  //   isPaused.value=false;
  //   console.log("取消任务")
  //   //清空结果列表
  //   store.simulationResult=[];
  //   //清空rangeGenerator里面的输入
  //   if (rangeGenerator.value) {
  //     rangeGenerator.value.clearInput();
  //   }
  // }
  const onTest=()=>{
    const now=new Date();
    resultList.value.push(now.toLocaleTimeString())
    console.log(resultList.value)
    var virtualScroller=pageInstance.refs.virtualScroller;
    console.log(virtualScroller)
    virtualScroller.scrollToBottom();
    // virtualScroller.scrollToItem(resultList.value.length-1);
  }
  </script>
  
<style scoped>

</style>
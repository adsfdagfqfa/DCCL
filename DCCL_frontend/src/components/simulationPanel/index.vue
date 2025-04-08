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
            <el-button type="primary" @click="onUploadParameter">上传参数</el-button>
            <el-button type="primary" @click="onSimulation">开始仿真</el-button>
            <el-button type="primary" @click="onTest">测试</el-button>
        </el-card>
      
      
      </div>
      <div class="flex-1">
        <!-- <el-scrollbar >
          
        </el-scrollbar> -->
        <DynamicScroller
          ref="virtualScroller"
          class="list"
          :items="resultList"
          :min-item-size="150">
          <template v-slot="{ item }">
            <div class="list-item">
              <ResultItem :item="item" ></ResultItem>
            </div>
          </template>
        </DynamicScroller>
        <!-- <div v-for="(item,index) in resultList" :key="index" >
          <div class="list-item">
            <ResultItem :item="item" ></ResultItem>
          </div>
          
        </div> -->
      </div>
    </div>
  </template>
  
  <script setup>
  // import {JSONPath} from 'jsonpath-plus';
  import { onMounted,getCurrentInstance,onBeforeMount, ref ,computed} from 'vue';
  import { useThreeInstanceStore } from '@/store';
  import RangeGenerator from './rangeGenerator.vue';
  import { dateTableEmits } from 'element-plus/es/components/calendar/src/date-table';
  import ResultItem from './resultItem.vue'; 
  const rangeGenerator = ref();//引用的rangeGenerator组件
  
  var jp = require('jsonpath');
  const data={};
  const store = useThreeInstanceStore();
  //selectedElement为数组，记录选中的元素的路径
  const selectedElement = ref()
  const vectors=ref([])
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
  const pageInstance = getCurrentInstance();
  
  const resultList = computed(() => {
    return store.simulationResult;
  });
  
  async function getAllParameter() {
    data.distance=store.distance;
    data.angle=store.angle;
    data.resonatorParam=store.resonatorParam;
    data.fastFTParam=store.fastFourierTransformParam;
    data.modelAttributeList=store.threeInstance.modelAttributeList;
    // var nodes=jp.nodes(data,'$..focalLength');
    // console.log(nodes)
  }
  
  function handleExpandChange(activePath){
    if(activePath.length==0){
      //当activePath为空时直接退出
      return
    } 
    console.log('当前展开的路径：', activePath);
    console.log('当前数据：',data );
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
    var dataList=jp.nodes(data, node.value);
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
        let a=jp.query(data,jp.stringify(item.path.slice(0,length-1)));
        return a[0].model+"_"+item.path[length-1];
      case 'angle':
        return item.path[1]+'_'+item.path[length-1];
      case 'distance':
        return item.path[1]+'_'+item.path[length-1];
    }
    return jp.stringify(item.path);
  }
  onMounted(async () => {
    await getAllParameter();
    console.log('Component is mounted');
  })
  async function onSimulation(){
    // let length=selectedElement.value.length;
    // console.log(selectedElement.value);
    // console.log(jp.query(data,selectedElement.value[length-1]));
    
    //判断是否设置参数
    const param={}
    
    if(selectedElement.value!==undefined){
      let length=selectedElement.value.length;
      param.path=selectedElement.value[length-1]
      param.vectors=vectors.value
    }
    var virtualScroller=pageInstance.refs.virtualScroller;
    await store.simulation(JSON.stringify(param),virtualScroller)
    // console.log(data)
    console.log('开始仿真')
   
  }
  async function onUploadParameter(){
    await store.uploadParameter(JSON.stringify(data))
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
  const onTest=()=>{
    
    // const sseUrl = `/flask/api/v1/sse`;
    // // 创建 EventSource 实例
    // const eventSource = new EventSource(sseUrl);
    //   // 监听消息事件
    // eventSource.onmessage = function(event) {
    //   console.log("Received data:", event.data);
    //   //更新数据
    // };
  
    // // 监听错误事件
    // eventSource.onerror = function(err) {
    //   console.error("EventSource failed:", err);
    //   eventSource.close(); // 关闭连接
    // };
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
/* Your component-specific styles go here */
.list {
  height: 300px;
  border: 5px solid #eeeeeee9;
  border-radius: 8px;
}

.list-item {
  height:150px;
  padding: 12px;
  border-bottom: 1px dashed #020817;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>
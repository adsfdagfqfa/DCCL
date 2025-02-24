<template>
  <div class="flex">
    <div style="flex:0 0 30%">
      <el-card class="h-full">
        
        
          <el-cascader class="mb-5" clearable 
                  v-model="selectedElement" 
                  :options="jsonpath" 
                  :show-all-levels="false" 
                  placeholder="请选择参数"
                  @expand-change="handleExpandChange"/>
          
          <RangeGenerator @get-result-array="getResultArray" />
          <el-button type="primary" @click="onUploadParameter">上传参数</el-button>
          <el-button type="primary" @click="onEmulation">开始仿真</el-button>
        
      </el-card>
    
    
    </div>
    <div class="flex-1">
      <el-scrollbar >

      </el-scrollbar>
    </div>
  </div>
</template>

<script setup>
// import {JSONPath} from 'jsonpath-plus';
import { onMounted,onBeforeMount, ref ,computed} from 'vue';
import { useThreeInstanceStore } from '@/store';
import RangeGenerator from './rangeGenerator.vue';
var jp = require('jsonpath');
const data={};
const store = useThreeInstanceStore();
//selectedElement为数组，记录选中的元素的路径
const selectedElement = ref([])

const jsonpath=ref([
  {
    value: '$.modelAttributeList[*].focalLength',
    label:'焦距',
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
    label:'角度',
    children:[],
    leaf:false
  },
  {
    value:'$.distance[*]',
    label:'距离',
    children:[],
    leaf:false
  },
  {
    value:'$.resonatorParam.lamada',
    label:'波长',
    leaf:true
  },
  {
    value:'$.resonatorParam.pumpPower',
    label:'泵浦功率',
    leaf:true
  },
])



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
  console.log('当前展开的路径：', activePath);
  console.log('当前数据：',data );
  // 获取当前展开的节点
  const currentNode = getNodeByPath(jsonpath.value, activePath);
  // 动态加载子节点数据
  try {
    loadChildren(currentNode).then((children) => {
      console.log('加载子节点成功：', children);
      // 使用 $set 确保响应式
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
function onEmulation(){
  // let length=selectedElement.value.length;
  // console.log(selectedElement.value);
  // console.log(jp.query(data,selectedElement.value[length-1]));

  console.log('开始仿真')
}
function onUploadParameter(){

  console.log('上传参数')
}
function getResultArray(value){
  console.log(value)
}
</script>

<style scoped>
/* Your component-specific styles go here */
</style>
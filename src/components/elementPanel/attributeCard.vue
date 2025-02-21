<template>
  <div>
    <div class="flex items-center">
      <el-icon size="20"><List/></el-icon>
      <span> 模型列表 </span>
    </div>
    <el-scrollbar max-height="150">
      <div  v-for="item in modelAttributeList"
            :key="item.model">
        <div  class="flex justify-between items-center"
              :class="item.model===store.selectedElement?'choose':''" 
              @click="setSelectedElement(item.model)">
          <span>{{ item.model }} </span>
          <el-space>
            <div v-show="item.model===store.selectedElement">
              <el-icon size="20" color="#0c5df2">
                <Check/>
              </el-icon>
            </div>
            <div>
              <el-icon size="20" color="#FA8072" @click.stop="deleteModel(item.model)">
                <Delete/>
              </el-icon>
            </div>
          </el-space>
        </div>
      </div>
    </el-scrollbar>
  </div>
  <div>
    <div class="flex items-center">
      <el-icon size="20"><Edit/></el-icon>
      <span>编辑面板</span>
    </div>
    <div v-for="(value, key) in attribute" :key="key">
      <div v-if="isEditableType(key)" class="flex justify-between gap-2"> 
        <label class="no-wrap" :for="key">{{keyMappings[key] }} </label>
        <el-input type="number"  v-model.number="attribute[key]"  placeholder="请输入"
                  :min="rangeLimits[key]?.min" :max="rangeLimits[key]?.max"/>
      </div>
    </div>
  </div>
  <div class="flex flex-col">
    <div class="flex items-center">
        <el-icon size="20"><Location /></el-icon>
        <span> 模型位置 </span>
    </div>
    <div class="flex" v-if="store.selectedElement"> 
      <el-button class="mx-2" type="primary" link>X 轴</el-button>
      <el-slider class="mx-2" v-model="position.x"/>   
    </div>
    <div class="flex" v-if="store.selectedElement">
      <el-button class="mx-2" type="primary" link>Y 轴</el-button>
      <el-slider class="mx-2" v-model="position.y"/> 
    </div>
  </div>
  <!-- <el-button  @click="handleInput">输出数据</el-button> -->
</template>
  
<script setup>
import { keyMappings  } from '@/utils/constant/model';
import { rangeLimits } from '@/utils/constant/model';
import { computed, ref ,reactive} from 'vue';
import { onMounted } from 'vue';
import { watch } from 'vue';
import { useThreeInstanceStore } from '@/store';
//icon相应的图表需要重新引入
import {List,Delete,Check,Edit,Location} from '@element-plus/icons-vue'
import { storeToRefs } from 'pinia';
const store=useThreeInstanceStore();



function isEditableType(key) {
  //判断是否可编辑 
  const readOnlyTypes = [ 'model' ,'type','name'];
  return !readOnlyTypes.includes(key);
}
// function updateComponent() {
//   // 通知父组件对象已更新
//   console.log(component.value)
//   emits('update:component', component.value);
// }
function setSelectedElement(name){
  if(name){
    store.setSelectedElement(name)
  }
  console.log("当前点击元素",store.selectedElement)
}


//可选链运算符?.
const modelAttributeList = computed(() => store.threeInstance?.modelAttributeList);
const modelList = computed(() => store.threeInstance?.modelList);
const attribute=ref({})
const position=ref({})
watch(()=>store.selectedElement,(newVal)=>{

  const foundItem=modelList.value?.filter(item=>item.userData.attribute.model===newVal)
  
  if (foundItem.length!==0) {
    console.log("找到元素")
    // console.log(foundItem.userData)
    attribute.value = foundItem[0]?.userData.attribute;
    position.value=foundItem[0]?.position
  } else {
    console.log("未找到元素")
    //未找到时候设置为undefined
    attribute.value = undefined;
  }
  
})

watch([()=>position.value.x,()=>position.value.y],()=>{
  console.log("位置变化")
  if(modelList){
    // modelList.value.sort((a, b) => {
    //   return a.position.x-b.position.x ; // 从小到大排序
      
    // });
    const sortedIndices = modelList.value
      .map((item, index) => ({ item, index })) // 将每个 item 和它的索引绑定
      .sort((a, b) => a.item.position.x - b.item.position.x) // 按 position.x 排序
      .map(item => item.index); // 提取排序后的索引
    console.log(sortedIndices)
  
    // 2. 使用索引映射更新两个数组
    modelList.value.splice(0, modelList.value.length, ...sortedIndices.map(index => modelList.value[index]));
    modelAttributeList.value.splice(0, modelAttributeList.value.length, ...sortedIndices.map(index => modelAttributeList.value[index]));
    updateDistance()
  }
})


function updateDistance(){
  console.log("更新距离")
  store.distance.forEach((item,index)=>{
      store.distance[index]=modelList.value[index+1].position.x-modelList.value[index].position.x
    })
  console.log("更新角度")
  store.angle.forEach((item,index)=>{
    let result=Math.atan((modelList.value[index+1].position.y-modelList.value[index].position.y)/store.distance[index])*180/Math.PI
    store.angle[index]=isNaN(result)?0:result.toFixed(3)//保留三位小数
    })
}
function deleteModel(name){
  console.log("删除模型",name)
  if(name){
    store.threeInstance.deleteModel(name)
  
    // store.threeInstance.modelList=store.threeInstance.modelList.filter(v => v.userData.attribute.model !== name);
    if(store.selectedElement===name){
      store.selectedElement=""
    }
    store.distance.pop()
    store.angle.pop()
    console.log(modelAttributeList.value)
    // console.log(store.modelAttributeList)
    // console.log(store.threeInstance.modelAttributeList)
    updateDistance()
  }
}
function handleInput(){
  console.log(attribute.value)
}
</script>

<style scoped>
.choose{
  background: #eeeeee;
}
.no-wrap {
  white-space: nowrap;  
}
</style>
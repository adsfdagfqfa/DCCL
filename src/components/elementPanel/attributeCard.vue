<template>
  <div>
    <div class="flex items-center">
      <el-icon size="20"><List/></el-icon>
      <span> 模型列表 </span>
    </div>
    <el-scrollbar max-height="150">
      <div  v-for="mesh in modelList"
            :key="mesh.userData.name">
        <div  class="flex justify-between items-center"
              :class="mesh.userData.name===store.selectedElement?'choose':''" 
              @click="setSelectedElement(mesh.userData.name)">
          <span>{{ mesh.userData.name }} </span>
          <el-space>
            <div v-show="mesh.userData.name===store.selectedElement">
              <el-icon size="20" color="#0c5df2">
                <Check/>
              </el-icon>
            </div>
            <div>
              <el-icon size="20" color="#FA8072">
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
        <el-input  v-model="attribute[key]"  placeholder="请输入"/>
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
      <el-slider class="mx-2" v-model="position.x" @mouseup="handlePositionChange"/>   
    </div>
    <div class="flex" v-if="store.selectedElement">
      <el-button class="mx-2" type="primary" link>Y 轴</el-button>
      <el-slider class="mx-2" v-model="position.y" @mouseup="handlePositionChange"/> 
    </div>
  </div>
</template>
  
<script setup>
import { keyMappings } from '@/utils/constant/model';
import { computed, ref ,reactive} from 'vue';
import { onMounted } from 'vue';
import { watch } from 'vue';
import { useThreeInstanceStore } from '@/store';
//icon相应的图表需要重新引入
import {List,Delete,Check,Edit,Location} from '@element-plus/icons-vue'
const store=useThreeInstanceStore();



function isEditableType(key) {
  //判断是否可编辑 
  const readOnlyTypes = [ 'id', 'type','name'];
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
const modelList = computed(() => store.threeInstance?.modelList);

const attribute=ref({})
const position=ref({})
watch(()=>store.selectedElement,(newVal)=>{
  
  const foundItem=modelList.value?.filter(item=>item.userData.name===newVal)

  if (foundItem) {
    // console.log(foundItem.userData)
    attribute.value = foundItem[0]?.userData.attribute;
    position.value=foundItem[0]?.position
  } else {
    attribute.value = undefined;
  }
  console.log(attribute.value)
  console.log(foundItem[0].userData.attribute)
})
// watch(position,()=>{
  
//   if(modelList){
    
//     modelList.value.sort((a, b) => {
//       return a.position.x-b.position.x ; // 从小到大排序
//     });
//   }
// })
function handlePositionChange(){
  if(modelList){
    modelList.value.sort((a, b) => {
      return a.position.x-b.position.x ; // 从小到大排序
    });
    store.distance.forEach((item,index)=>{
      store.distance[index]=modelList.value[index+1].position.x-modelList.value[index].position.x
    })
    store.angle.forEach((item,index)=>{
      
      let result=Math.atan((modelList.value[index+1].position.y-modelList.value[index].position.y)/store.distance[index])*180/Math.PI
      store.angle[index]=isNaN(result)?0:result.toFixed(3)//保留三位小数
   })
  }
  console.log("位置变化")
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
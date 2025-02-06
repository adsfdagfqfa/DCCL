<template>
  <div>
    <div class="flex items-center">
      <el-icon size="20"><List/></el-icon>
      <span> 模型列表 </span>
    </div>
    <el-scrollbar>
      <div  @click="onChangeSelectedModel()"
            v-for="mesh in modelList"
            :key="mesh.userData.name">
        <div class="flex justify-between items-center" @click="setSelectedElement(mesh.userData.name)">
          <span>{{ mesh.userData.name }} </span>
          <el-space>
            <div v-if="mesh.userData.name===store.selectedElement">
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
    <div v-for="(value, key) in component" :key="key">
      <label :for="key">{{ key }}: </label>
      <!-- <el-input v-if="isEditableType(key)"  v-model="component.key" @blur="updateComponent" placeholder="请输入"/>
      <div v-else-if="key==='position'">
          <div class="flex items-center justify-center">
              <span>x:</span>
              <el-input v-model="component.position.x" @blur="updateComponent" placeholder="请输入"/>
          </div>
          <div class="flex items-center justify-center">
              <span>y:</span>
              <el-input v-model="component.position.y" @blur="updateComponent" placeholder="请输入"/>
          </div>
          <div class="flex items-center justify-center">
              <span>z:</span>
              <el-input v-model="component.position.z" @blur="updateComponent" placeholder="请输入"/>
          </div>
      </div> -->
      <!-- <span v-else>{{ value }}</span> -->
    </div>
  </div>
</template>
  
<script setup>

import { computed, ref ,reactive} from 'vue';
import { onMounted } from 'vue';
import { watch } from 'vue';
import { useThreeInstanceStore } from '@/store';
//icon相应的图表需要重新引入
import {List,Delete,Check,Edit} from '@element-plus/icons-vue'
const store=useThreeInstanceStore();



function isEditableType(key) {
    //定义哪些属性是可以编辑的
    
    const editableTypes = [ 'length', 'focalLength','radius','reflectivity'];
    return editableTypes.includes(key);
}
function updateComponent() {
    // 通知父组件对象已更新
    console.log(component.value)
    emits('update:component', component.value);
    
}
function setSelectedElement(name){
  if(name){
    store.setSelectedElement(name)
  }
  console.log("当前点击元素",store.selectedElement)
}


//可选链运算符?.
const modelList = computed(() => store.threeInstance?.modelList);

const component=ref({})
watch(()=>store.selectedElement,(newVal)=>{
  
  const foundItem=modelList.value?.filter(item=>item.userData.name===newVal)
  if (foundItem) {
    console.log(foundItem.userData)
    component.value = foundItem[0].userData.attribute;
    
  } else {
    component.value = undefined;
  }
})
</script>
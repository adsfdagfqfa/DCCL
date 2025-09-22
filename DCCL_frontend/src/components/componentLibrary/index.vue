<template>
  <el-scrollbar class="max-h-[400px]">
    <el-collapse class="tour-component-library" v-model="activeNames" @change="handleChange">
      <el-collapse-item  name="opticalComponent">
        <template #title>
          <img src="@/assets/lens.svg"  class="w-3" />光学元件
        </template>
        <el-row>
          <el-col class="text-center" :span="12" v-for="model in opticalModelList" :key="model.type">
            <div draggable="true"
                @dragstart="e => onDragStart(e, model)"
                @drag="e => onDrag(e)">
              <div>
                <el-tooltip effect="dark" :content="`${model.name}:${model.type}`"  placement="top">
                  <b> {{ model.name }}</b>
                </el-tooltip>
              </div>
            </div>
          </el-col>
        </el-row>
      </el-collapse-item>
      <!-- <el-collapse-item title="Feedback" name="1111">
        <div>
          Operation feedback: enable the users to clearly perceive their
          operations by style updates and interactive effects;
        </div>
        <div>
          Visual feedback: reflect current state by updating or rearranging
          elements of the page.
        </div>
      </el-collapse-item> -->
      
      
    </el-collapse>
  </el-scrollbar>
</template>

<script setup>
import { ref } from 'vue';
import { opticalModelList } from '@/utils/constant/model'; 
import { useThreeInstanceStore } from '@/store';
//记录打开的折叠面板
const activeNames = ref(['opticalComponent'])
const store=useThreeInstanceStore();
const handleChange = (val) => {
  console.log(val)
}
const onDragStart=(event,model)=>{
  store.threeInstance.setDragModel(model)
}
//拖拽,关闭默认行为
const onDrag = event => {
  event.preventDefault();
};

</script>
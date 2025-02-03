<template>
  <el-scrollbar class="max-h-[500px]">
    <el-collapse v-model="activeNames" @change="handleChange">
      <el-collapse-item  name="opticalElement">
        <template #title>
          <img src="@/assets/lens.svg"  class="w-3" />光学元件
        </template>
        <el-row>
          <el-col class="text-center" :span="12" v-for="model in opticalModelList" :key="model.type">
            <div draggable="true"
                @dragstart="e => onDragstart(e, model)"
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
      <el-collapse-item title="Feedback" name="1111">
        <div>
          Operation feedback: enable the users to clearly perceive their
          operations by style updates and interactive effects;
        </div>
        <div>
          Visual feedback: reflect current state by updating or rearranging
          elements of the page.
        </div>
      </el-collapse-item>
      
      
    </el-collapse>
  </el-scrollbar>
</template>

<script setup>
import { ref } from 'vue';
import { opticalModelList } from '@/utils/models/model'; 
//记录打开的折叠面板
const activeNames = ref([ ])
const handleChange = (val) => {
  console.log(val)
}
const onDragstart=(event,model)=>{

}
//拖拽,关闭默认行为
const onDrag = event => {
  event.preventDefault();
};

</script>
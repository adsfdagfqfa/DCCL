<template>
  <div class="flex">
    <div style="flex:0 0 30%">
      <el-card>
        <el-select
        v-model="value"
        placeholder="Select"
        size="large"
        style="width: 240px">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
        <el-button type="primary" >开始仿真</el-button>
      </el-card>
    </div>
    <div class="flex-1">
      <el-scrollbar >

      </el-scrollbar>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';


const value = ref('')

const options = [
  {
    value: 'Option1',
    label: 'Option1',
  },
  {
    value: 'Option2',
    label: 'Option2',
  },
  {
    value: 'Option3',
    label: 'Option3',
  },
  {
    value: 'Option4',
    label: 'Option4',
  },
  {
    value: 'Option5',
    label: 'Option5',
  },
]
// Define your reactive variables and functions here
const message = ref('Hello, Vue 3!');
</script>

<style scoped>
/* Your component-specific styles go here */
</style>
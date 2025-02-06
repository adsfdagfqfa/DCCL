<template>
  <!-- 顶端部分 -->
  <header class="flex flex-col">
    <div class="bg-blue-200 text-gray-800 text-center leading-[60px]">分布式耦合腔激光系统仿真软件</div>
    <Menu></Menu>
  </header>
  <div class="grid grid-cols-6">
    <!-- <Steps  @update:router-view="handleClick"/> -->
    <ElementList></ElementList>
    <div class="col-span-4">
      <Resonator></Resonator>
      <router-view/>
    </div>
    <ElementPanel/>
    <!-- <test></test> -->
  </div>
</template>

<script setup>
import Menu from '@/components/menu/index.vue'
import ElementList from '@/components/elementList/index.vue'
import ElementPanel from '@/components/elementPanel/index.vue'

import Resonator from '@/components/resonator/index.vue';
import { onMounted } from 'vue';
onMounted(async()=>{
  console.log("mainView","挂载")
})
</script>

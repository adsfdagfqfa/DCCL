<template>
  <div v-for="(value, key) in constant" :key="key" >
    <div class="flex"> 
      <label class="whitespace-nowrap font-bold min-w-40"  :for="key">{{keyMappings[key] }} </label>
      <div>{{ value }}</div>
    </div>
  </div>
</template>

<script setup>
import { constant } from '@/utils/constant/constant';
import { keyMappings } from '@/utils/constant/model';
</script>

<style scoped>

</style>
<template>
  <router-view></router-view>
</template>

<script setup>
import { RouterView, useRoute, useRouter } from 'vue-router';
import { useThreeInstanceStore } from './store/index.js';
import { onMounted } from 'vue';
const store = useThreeInstanceStore();
const router =useRouter()
onMounted(() => {
  store.initToken()
})
</script>


<style scoped>

</style>

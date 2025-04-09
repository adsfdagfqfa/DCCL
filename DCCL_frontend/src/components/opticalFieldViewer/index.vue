<template>
    <div class="relative w-full min-h-100">
        <div ref="plotContainer"></div>
        <!-- 加载状态 -->
        <!-- <div v-if="loading" class="loading">Loading...</div> -->
        <!-- <el-icon class="is-loading"> -->
        <el-icon v-if="loading" class="is-loading absolute inset-x-1/2" >
            <Loading />
        </el-icon>
    </div>
</template>
  
<script setup>

import { ref,onMounted,getCurrentInstance } from 'vue';
import { useThreeInstanceStore } from '@/store';
import { storeToRefs } from "pinia";
import { Loading } from '@element-plus/icons-vue'
const store=useThreeInstanceStore();
const loading=ref(false);
//获取当前组件实例
const pageInstance = getCurrentInstance();

async function loadPlot() {
    loading.value = true
    // store.getPicture()
    try{
        const data = await store.getPicture();
        pageInstance.refs.plotContainer.innerHTML = data.html
        //执行html中的脚本
        executeScript(pageInstance.refs.plotContainer);
        console.log("plot","请求成功")
    }catch (error) {    
        error => console.error('加载失败:', error)
    }
    finally {
        loading.value = false
    }
    console.log("plot","加载完成")

}
function executeScript(container){
    const scripts = container.getElementsByTagName('script');
    Array.from(scripts).forEach(oldScript => {
        const newScript = document.createElement('script');
        newScript.type = oldScript.type || 'text/javascript';
        if (oldScript.src) {
            newScript.src = oldScript.src;
        } else {
            newScript.textContent = oldScript.textContent;
        }
        oldScript.parentNode.replaceChild(newScript, oldScript);
    });
}
onMounted(async()=>{
  console.log("opticalFieldViewer","挂载")
  await loadPlot()
})

</script>


<style scoped>

.loading {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
</style>
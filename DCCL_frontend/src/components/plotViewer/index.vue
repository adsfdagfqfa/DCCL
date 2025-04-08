<template>
    <div class="relative w-full min-h-100">
    <!-- 动态插入HTML内容 -->
        <div ref="plotContainer"></div>

        <!-- 加载状态 -->
        <div v-if="loading" class="loading">Loading...</div>
    </div>
</template>
  
<script setup>
import axios from "axios";
import { ref,onMounted,getCurrentInstance } from 'vue';
import { useThreeInstanceStore } from '@/store';
import { storeToRefs } from "pinia";
const store=useThreeInstanceStore();
const loading=ref(false);
const pageInstance = getCurrentInstance();
  

async function loadPlot() {
    // loading.value = true
    // const key=store.key
    // try{
    //     await axios.get(`/flask/api/v1/picture/${key}`).then((response) => {
    //         console.log("plot","请求成功")
    //         pageInstance.refs.plotContainer.innerHTML = response.data.html
    //         //执行html中的脚本
    //         executeScript(pageInstance.refs.plotContainer);
    //     })
    // }catch (error) {    
    //     error => console.error('加载失败:', error)
    // }
    // finally {
    //     loading.value = false
    // }
    // console.log("plot","加载完成")

    loading.value = true
    store.getPicture()
    try{
        await store.getPicture().then((data) => {
            console.log("plot","请求成功")
            pageInstance.refs.plotContainer.innerHTML = data.html
            //执行html中的脚本
            executeScript(pageInstance.refs.plotContainer);
        })
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
  console.log("plot","挂载")
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
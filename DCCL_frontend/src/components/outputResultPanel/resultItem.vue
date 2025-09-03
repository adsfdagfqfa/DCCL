<template>
    <div>
        <div v-if="itemJSON.isEnd">
             <!-- 首先显示特定的键（例如 name） -->
            <div v-if="itemJSON.selectedAttribute">
                <div v-for="(value, key) in itemJSON.selectedAttribute" :key="key">
                    <strong>{{key}}：</strong>{{value}}
                </div>
            </div>
            <div v-for="(value, key) in itemJSON" :key="key">
                <div v-if="key!=='selectedAttribute' && key!=='isEnd'&&!['fieldDistributionMain','fieldDistributionFree'].includes(key)">
                    <span>{{key}}：{{ value }}</span>
                </div>  
            </div>
            <div v-for="(value, key) in itemJSON" :key="key">
                <div v-if="['fieldDistributionMain','fieldDistributionFree'].includes(key)">
                    <el-button type="primary" @click="onGetPicture(value)">{{key}}</el-button>
                </div>  
            </div>
        </div>
        <div v-else v-show="!only_final_result" >
            <div v-if="itemJSON.selectedAttribute">
                <div v-for="(value, key) in itemJSON.selectedAttribute" :key="key">
                    <strong>{{key}}：</strong>{{value}}
                </div>
            </div>
            <div v-for="(value, key) in itemJSON" :key="key">
                <div v-if="key!=='selectedAttribute' && key!=='isEnd'">
                    <span> {{key}}：{{value}}</span>
                </div>
                <!-- <el-button type="text" @click="onTest">测试</el-button> -->
            </div>
        </div>
    </div>
</template>

<script setup>
import { useThreeInstanceStore } from '@/store';
import { defineProps, onMounted ,ref} from 'vue';
const props = defineProps({
    item: {
        type: String,
        required: true
    },
    only_final_result: {
        type: Boolean,
        default: false
    }
});
const itemJSON=ref({});
const store = useThreeInstanceStore();
function init() {
    // Add your initialization logic here if needed
    console.log("item",props.item)
    itemJSON.value = JSON.parse(props.item);
    // itemJSON.value = props.item;
    // console.log("itemJSON",itemJSON.value)
}
function onGetPicture(value) {
    // 处理获取图片的逻辑
    console.log("获取图片",value)
    console.log("opticalFieldDialogVisible",store.opticalFieldDialogVisible)
    store.fileName=value
    store.opticalFieldDialogVisible = true
    // 这里可以添加获取图片的代码
}
onMounted(() => {
    init()
})
</script>
<template>
    <el-tour
        v-model="visible"
        :steps="steps"
        :show-step-indicator="true"
        :show-close="true"
        @finish="onFinish"
        @close="onClose">
        <el-tour-step
            v-for="(step, index) in steps"
            :key="index"
            :target="step.target"
            :title="step.title"
            :description="step.description"/>
    </el-tour>
</template>

<script setup>
import { ref, defineProps, watch } from 'vue'

const props = defineProps({
    steps: {
        type: Array,
        required: true,
        // 每个step: { title: string, description: string, target: string (选择器) }
    },
    modelValue: {
        type: Boolean,
        default: false
    }
})

const visible = ref(props.modelValue)

watch(() => props.modelValue, (val) => {
    console.log("modelValue changed:", val);
    console.log("visible before change:", visible.value);
    console.log("steps:", props.steps);
    visible.value = val
})

watch(visible, (val) => {
    // 通知父组件
    emit('update:modelValue', val)
})

const emit = defineEmits(['update:modelValue'])

function onFinish() {
    visible.value = false
}

function onClose() {
    visible.value = false
}
</script>
<template>
    <el-tour
        ref="tourRef"
        v-model="visible"
        :steps="steps"
        :show-step-indicator="true"
        :show-close="true"
        @change="handleStepChange"
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
import { ref, defineProps, watch,inject } from 'vue';
import { nextTick } from 'vue';
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
const tabsRef = inject('tabsRef')
const visible = ref(props.modelValue)
const emit = defineEmits(['update:modelValue'])
const tourRef = ref(null)

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

function onFinish() {
    visible.value = false
}

function onClose() {
    visible.value = false
}
const isInViewport = (el) => {
  const rect = el.getBoundingClientRect()
  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  )
}

const handleStepChange =async (num) => {
    if('tab' in props.steps[num]&&tabsRef?.value){
        // tabsRef.value.modelValue = props.steps[num].tab
        tabsRef.value.$emit('update:modelValue', props.steps[num].tab)
        // await nextTick()
    }
    const el = document.querySelector(props.steps[num].target)
    scrollDom(el)
    await nextTick()
    tourRef?.value.updateLocation?.()
}
const scrollDom = (targetDom) => {
    console.log('指定dom元素滚动到可视窗口',targetDom);
    targetDom?.scrollIntoView({ block: 'center' ,behavior: 'auto',inline: 'center'}); 
}

</script>
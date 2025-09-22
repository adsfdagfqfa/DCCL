<template>
    <div>
        <label class="font-bold text-xl mb-3 block">结果分析图</label>
        <!-- <div class="flex gap-4">
            <el-select v-model="yLabel" placeholder="Select Y">
                <el-option v-for="item in yLabels" :key="item" :label="item" :value="item"/>
            </el-select>
            <el-select v-model="xLabel" placeholder="Select X">
                <el-option v-for="item in xLabels" :key="item" :label="item" :value="item"/>
            </el-select>
            <el-button type="primary" @click="drawPlot">生成图表</el-button>
        </div> -->
        <el-button type="primary" @click="drawPlot">生成图表</el-button>
        <div ref="plotContainer" class="chart-container"></div>
    </div>
</template>

<script setup>
import { ref,onMounted,getCurrentInstance,onUnmounted,watch } from 'vue';
import { useThreeInstanceStore } from '@/store';
const store=useThreeInstanceStore();
const pageInstance = getCurrentInstance();
const xLabels=ref()
const yLabels=ref(["outputPower"])
const xLabel=ref('')
const yLabel=ref('outputPower')
const data=ref([])
const parsedData=ref([])
//绘图使用的是d3库，在index.html中以CDN形式引入
onMounted(() => {
    console.log('plot','挂载')
});

function getData(){
    parsedData.value = store.simulationResult.map(item => JSON.parse(item.content));
    console.log(parsedData.value)
    // const parsedContent = JSON.parse(store.simulationResult[0].content);
    // xLabels.value=Object.keys(parsedData.value[0].selectedAttribute)
    xLabel.value=Object.keys(parsedData.value[0].selectedAttribute)[0];
    // console.log("xLabel",xLabel.value)
}

onUnmounted(() => {
  // 清理资源
  d3.select(pageInstance.refs.plotContainer).selectAll('*').remove();
});

function drawPlot(){
    getData()
    for (const item of parsedData.value) {
        if(item.isEnd){
            console.log(item.selectedAttribute)
            data.value.push({
                x:item.selectedAttribute[xLabel.value],
                y:item[yLabel.value]
            })
        }
    } 
    console.log(data.value)
    // data.value = [
    //     { x: 0, y: 10 },
    //     { x: 1, y: 20 },
    //     { x: 2, y: 30},
    //     { x: 3, y: 40 },
    //     { x: 4, y: 50 },
    //     { x: 5, y: 60 }
    // ];
    d3.select(pageInstance.refs.plotContainer).selectAll('*').remove();
    const width = 450;
    const height = 400;
    console.log("plot","绘图")
    console.log(pageInstance.refs.plotContainer)
    // 创建 SVG 元素
    const svg = d3.select(pageInstance.refs.plotContainer)
        .append('svg')
        .attr('width', width)
        .attr('height', height);

    // 设置坐标轴范围
    const xScale = d3.scaleLinear()
        .domain([d3.min(data.value, d => d.x), d3.max(data.value, d => d.x)])
        .range([50, width - 50]);

    const yScale = d3.scaleLinear()
        .domain([d3.min(data.value,d=>d.y), d3.max(data.value,d=>d.y)])
        .range([height - 50, 50]);

    // 创建折线生成器
    const line = d3.line()
        .x(d => xScale(d.x))
        .y(d => yScale(d.y));

    // 绘制折线
    svg.append('path')
        .datum(data.value)
        .attr('fill', 'none')
        .attr('stroke', 'steelblue')
        .attr('stroke-width', 2)
        .attr('d', line);

    // 添加 X 轴
    svg.append('g')
        .attr('transform', `translate(0,${height - 50})`)
        .call(d3.axisBottom(xScale))
        .append('text')//添加文本元素
        .attr('x', width / 2)
        .attr('y', 40) 
        .attr('text-anchor', 'middle') //文本居中对齐
        .attr('fill','black') //文本颜色
        .style('font-size', '16px') //文本大小
        .text(xLabel.value); //X 轴标签的文本内容

    // 添加 Y 轴
    svg.append('g')
        .attr('transform', `translate(50,0)`)
        .call(d3.axisLeft(yScale))
        .append('text')
        .attr('x', 0)
        .attr('y', 40)
        .attr('text-anchor', 'middle')
        .attr('fill','black') //文本颜色
        .style('font-size', '16px') //文本大小
        .text(yLabel.value);
}
watch(
  () => store.plotReady,
  (ready) => {
    if (ready) {
      console.log("加载曲线数据")
      loadPlot(store.plotData)
    }
  }
)
defineExpose({
    getData, // 将 getData 方法暴露给父组件
});
</script>
